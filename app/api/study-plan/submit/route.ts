import { auth } from "@/auth";
import Anthropic from "@anthropic-ai/sdk";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: { rejectUnauthorized: false },
});

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function getUserId(email: string): Promise<number | null> {
  const res = await pool.query("SELECT id FROM users WHERE email = $1", [email]);
  return res.rows.length > 0 ? res.rows[0].id : null;
}

type TopicRatings = Record<string, "Strong" | "OK" | "Weak">;

export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const userId = await getUserId(session.user.email);
  if (!userId) {
    return Response.json({ error: "User not found" }, { status: 404 });
  }

  try {
    const body = await request.json();
    const { bio, chem, psych, cars, topicRatings, testDate, weeksUntilTest } = body as {
      bio: number;
      chem: number;
      psych: number;
      cars: number;
      topicRatings: TopicRatings;
      testDate: string | null;
      weeksUntilTest: number;
    };

    // Validate
    for (const score of [bio, chem, psych, cars]) {
      if (typeof score !== "number" || score < 118 || score > 132) {
        return Response.json({ error: "Section scores must be between 118 and 132" }, { status: 400 });
      }
    }
    if (typeof weeksUntilTest !== "number" || weeksUntilTest < 1 || weeksUntilTest > 26) {
      return Response.json({ error: "Weeks until test must be 1-26" }, { status: 400 });
    }
    if (!topicRatings || typeof topicRatings !== "object") {
      return Response.json({ error: "Topic ratings required" }, { status: 400 });
    }

    const total = bio + chem + psych + cars;

    // Mark old submissions/plans as not current
    await pool.query(`UPDATE score_submissions SET is_current = FALSE WHERE "userId" = $1 AND is_current = TRUE`, [userId]);
    await pool.query(`UPDATE study_plans SET is_current = FALSE WHERE "userId" = $1 AND is_current = TRUE`, [userId]);

    // Insert new submission
    const submissionRes = await pool.query(
      `INSERT INTO score_submissions ("userId", bio_score, chem_score, psych_score, cars_score, total_score, topic_ratings, test_date, weeks_until_test, is_current)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, TRUE)
       RETURNING id`,
      [userId, bio, chem, psych, cars, total, JSON.stringify(topicRatings), testDate || null, weeksUntilTest]
    );
    const submissionId = submissionRes.rows[0].id;

    // Pull unit catalog from database to give Claude context
    const unitsRes = await pool.query(
      `SELECT id, section, unit_number, title FROM study_units ORDER BY section, unit_number`
    );
    const unitsCatalog = unitsRes.rows.map((u) => ({
      unitId: u.id,
      section: u.section,
      unitNumber: u.unit_number,
      title: u.title,
    }));

    // Build prompt for Claude
    const weakTopics = Object.entries(topicRatings).filter(([, v]) => v === "Weak").map(([k]) => k);
    const okTopics = Object.entries(topicRatings).filter(([, v]) => v === "OK").map(([k]) => k);
    const strongTopics = Object.entries(topicRatings).filter(([, v]) => v === "Strong").map(([k]) => k);

    const systemPrompt = [
      "You are an expert MCAT study plan designer.",
      "You will produce a structured weekly study plan based on a student's current scores, topic strengths/weaknesses, and time until their MCAT.",
      "",
      "PLAN PRINCIPLES:",
      "- Prioritize WEAK topics first, then OK, then Strong (light review only).",
      "- Each week has a clear theme (e.g. 'Foundation: Biochemistry' or 'Review and Practice').",
      "- Each week has 3-7 actionable items. Items reference specific units from the catalog provided.",
      "- Items must be ONE of these types: 'read_unit' (read lessons in a unit), 'practice_questions' (do a set of practice questions in a section), 'unit_test' (take the unit's 15-question test), 'review' (review weak areas), 'aamc_test' (recommend they take an AAMC practice test).",
      "- For 'read_unit' items, reference unitId from the catalog.",
      "- Plan length matches weeksUntilTest exactly.",
      "- Final 1-2 weeks should focus on AAMC practice tests + review, not new content.",
      "- Estimate hours per week realistically: 10-20 hrs for serious prep.",
      "",
      "Return ONLY valid JSON. No prose before or after, no markdown fences.",
      "Structure:",
      "{",
      '  "summary": "1-2 sentence overview of strategy",',
      '  "weeks": [',
      "    {",
      '      "weekNumber": 1,',
      '      "theme": "Foundation: Biochemistry",',
      '      "rationale": "Why this week focuses on this",',
      '      "estimatedHours": 12,',
      '      "items": [',
      "        {",
      '          "id": "w1-i1",',
      '          "type": "read_unit",',
      '          "unitId": 1,',
      '          "title": "Read all lessons in Biochemistry Foundations",',
      '          "description": "Focus on amino acid structures, especially pKa values"',
      "        },",
      "        {",
      '          "id": "w1-i2",',
      '          "type": "practice_questions",',
      '          "section": "bio-biochem",',
      '          "title": "Do 20 Bio/Biochem practice questions",',
      '          "description": "Focus on biochemistry topic"',
      "        }",
      "      ]",
      "    }",
      "  ]",
      "}",
    ].join("\n");

    const userPrompt = [
      `Student's MCAT scores:`,
      `- Bio/Biochem: ${bio}`,
      `- Chem/Phys: ${chem}`,
      `- Psych/Soc: ${psych}`,
      `- CARS: ${cars}`,
      `- Total: ${total}`,
      ``,
      `Weeks until test: ${weeksUntilTest}`,
      ``,
      `Topic self-assessment:`,
      `- WEAK areas (prioritize): ${weakTopics.join(", ") || "(none)"}`,
      `- OK areas: ${okTopics.join(", ") || "(none)"}`,
      `- STRONG areas (light review only): ${strongTopics.join(", ") || "(none)"}`,
      ``,
      `Available units catalog (use unitId in your plan):`,
      JSON.stringify(unitsCatalog, null, 2),
      ``,
      `Generate a ${weeksUntilTest}-week structured study plan as valid JSON.`,
    ].join("\n");

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 8000,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }],
      temperature: 0.5,
    });

    const text = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n").trim();

    // Extract JSON
    const firstBrace = text.indexOf("{");
    const lastBrace = text.lastIndexOf("}");
    const jsonStr = firstBrace !== -1 && lastBrace > firstBrace
      ? text.substring(firstBrace, lastBrace + 1)
      : text;

    let planData;
    try {
      planData = JSON.parse(jsonStr);
    } catch {
      return Response.json({ error: "Couldn't generate a valid plan. Try submitting again." }, { status: 500 });
    }

    if (!planData.weeks || !Array.isArray(planData.weeks) || planData.weeks.length === 0) {
      return Response.json({ error: "Plan structure invalid. Try again." }, { status: 500 });
    }

    // Save plan to DB
    const planRes = await pool.query(
      `INSERT INTO study_plans ("userId", "submissionId", weeks_count, plan_data, completed_items, is_current)
       VALUES ($1, $2, $3, $4, '[]'::jsonb, TRUE)
       RETURNING id`,
      [userId, submissionId, planData.weeks.length, JSON.stringify(planData)]
    );

    return Response.json({
      success: true,
      planId: planRes.rows[0].id,
      submissionId,
    });
  } catch (error) {
    console.error("Submit plan error:", error);
    return Response.json({ error: "Failed to generate plan" }, { status: 500 });
  }
}