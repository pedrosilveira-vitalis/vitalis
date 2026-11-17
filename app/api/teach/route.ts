import { randomUUID } from "node:crypto";
import { portalDb } from "@/lib/portal-db";
import { sendEmail } from "@/lib/email";

const SITE = (process.env.NEXT_PUBLIC_SITE_URL || "https://vitalis-lyart.vercel.app").replace(/\/$/, "");

function clean(value: unknown, max: number): string {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

export async function POST(request: Request) {
  let input;
  try { input = await request.json(); } catch { return Response.json({ error: "Invalid request." }, { status: 400 }); }

  const name = clean(input?.name, 120);
  const email = clean(input?.email, 200).toLowerCase();
  const experience = clean(input?.experience, 2000);
  const students = clean(input?.students, 500);
  const score = Number(input?.score);

  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return Response.json({ error: "Please give your name and a valid email." }, { status: 400 });
  }
  if (!Number.isInteger(score) || score < 472 || score > 528) {
    return Response.json({ error: "Please give your MCAT score between 472 and 528." }, { status: 400 });
  }

  // A referral code the tutor can hand straight to their students: their first
  // name plus four characters, readable enough to say out loud.
  const base = name.split(/\s+/)[0].toUpperCase().replace(/[^A-Z]/g, "").slice(0, 10) || "TUTOR";
  const code = `${base}-${randomUUID().slice(0, 4).toUpperCase()}`;

  try {
    const db = await portalDb();
    await db.query(
      `INSERT INTO vitalis_tutor_applications (id, name, email, mcat_score, experience, students, referral_code)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [randomUUID(), name, email, score, experience, students, code],
    );
  } catch {
    return Response.json({ error: "Could not save your application. Please retry." }, { status: 503 });
  }

  // Both emails are best effort: the application is already saved.
  const firstName = name.split(/\s+/)[0];
  sendEmail({
    to: email,
    subject: "Thanks for applying to tutor with Vitalis",
    html: `<p>Hi ${firstName},</p>
      <p>Thanks for applying. I read every one of these myself and I'll come back to you within two days.</p>
      <p>So you know what you're walking into: you keep <strong>100% of your own tutoring rate</strong>. We take nothing from your sessions. You earn <strong>$100</strong> every time a student of yours takes a Complete plan on your referral code, and <strong>$200</strong> for each live group review you run before a test date.</p>
      <p>Your code is reserved: <strong>${code}</strong></p>
      <p>&mdash; Pedro, Vitalis</p>`,
    text: `Hi ${firstName},\n\nThanks for applying. I'll come back to you within two days.\n\nYou keep 100% of your tutoring rate. $100 per Complete signup on your code, $200 per group review session.\n\nYour code: ${code}\n\n- Pedro, Vitalis`,
  }).catch(() => {});

  sendEmail({
    to: process.env.VITALIS_ADMIN_EMAILS?.split(",")[0]?.trim() || "pedrodocoutto@gmail.com",
    subject: `Tutor application: ${name} (${score})`,
    html: `<p><strong>${name}</strong> &mdash; ${email} &mdash; MCAT ${score}</p>
      <p><strong>Students they could bring:</strong> ${students || "not stated"}</p>
      <p><strong>Experience:</strong><br>${experience.replace(/\n/g, "<br>") || "not stated"}</p>
      <p>Code reserved: <strong>${code}</strong></p>
      <p><a href="${SITE}/admin">Open admin</a></p>`,
    text: `${name} - ${email} - MCAT ${score}\n\nStudents: ${students}\n\nExperience:\n${experience}\n\nCode: ${code}`,
  }).catch(() => {});

  return Response.json({ ok: true, code });
}
