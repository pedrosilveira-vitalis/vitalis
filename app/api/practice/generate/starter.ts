import { allocateSections, type Question, type Section, type sessionSettings } from "@/lib/practice";

type Item = [level: string, stem: string, choices: [string, string, string, string], answer: string, explanation: string];
type Set = { title: string; content: string; items: Item[] };

const bank: Record<Section, Set> = {
  "bio-biochem": {
    title: "Following a membrane transporter",
    content: "A team places identical cells in solutions containing different amounts of glucose. Glucose initially moves into the cells down its concentration gradient. At high external concentrations, increasing the glucose concentration barely changes the initial uptake rate. Cells expressing twice as many copies of transporter T show twice the maximum rate. In a separate experiment, compound X increases the glucose concentration needed for half-maximal uptake without changing the maximum.",
    items: [
      ["easy", "Which observation most directly supports a limited number of transport sites?", ["Glucose enters cells.", "Uptake approaches a maximum.", "Glucose is dissolved in water.", "The cells have membranes."], "B", "A plateau means that additional substrate produces little extra flux. This fits saturation of the available transport sites."],
      ["medium", "If the transporter operates by facilitated diffusion, what would reversing the glucose gradient do to net transport?", ["Reverse its direction", "Require ATP hydrolysis", "Destroy the transporter", "Double the number of sites"], "A", "Facilitated diffusion follows the concentration gradient. Reversing that gradient reverses net movement through the carrier."],
      ["hard", "Which mechanism best accounts for compound X's effect?", ["Irreversible loss of half the transporters", "Increased transporter expression", "Competition with glucose for binding", "A lower turnover rate at every occupied site"], "C", "Reaching the same maximum requires intact transport capacity. The need for more glucose at half maximum is consistent with competition that high glucose can overcome."]
    ]
  },
  "chem-phys": {
    title: "Flow through a model vessel",
    content: "A pump drives a liquid through a rigid cylindrical tube. Flow is steady and laminar. The reference tube carries 4 mL/s at a pressure difference of 8 kPa. For these conditions, volume flow is proportional to pressure difference and to the fourth power of radius, and inversely proportional to viscosity and tube length.",
    items: [
      ["easy", "The pressure difference doubles while all other conditions stay fixed. What is the new flow?", ["2 mL/s", "4 mL/s", "8 mL/s", "16 mL/s"], "C", "Flow scales directly with pressure difference. Doubling the pressure difference doubles 4 mL/s to 8 mL/s."],
      ["medium", "At the reference flow rate, how long would it take to collect 60 mL?", ["0.067 s", "15 s", "60 s", "240 s"], "B", "Time equals volume divided by volume flow. Dividing 60 mL by 4 mL/s gives 15 s."],
      ["hard", "The radius is halved and the viscosity is doubled. What pressure difference restores the reference flow?", ["16 kPa", "64 kPa", "128 kPa", "256 kPa"], "D", "Halving radius reduces flow by a factor of 16. Doubling viscosity contributes another factor of two. The pump must supply 32 times 8 kPa, or 256 kPa."]
    ]
  },
  "psych-soc": {
    title: "Testing retrieval practice",
    content: "Researchers randomly assign volunteers to reread a list or to practice recalling it. Both groups study for ten minutes. A week later, everyone takes the same recall test. The recall-practice group scores higher on average. The volunteers were recruited only from one university psychology club.",
    items: [
      ["easy", "Which variable did the researchers manipulate?", ["University membership", "Time until testing", "Recall test score", "Study method"], "D", "Assignment determined whether students reread or practiced recall. The later score was the measured outcome."],
      ["medium", "Which feature most directly limits generalization to all college students?", ["Random assignment", "Recruitment from one club", "Using the same test", "Equal study time"], "B", "One club may differ from the broader student population. Random assignment helps compare the recruited groups but does not make the sample representative."],
      ["hard", "Suppose only the recall-practice group received a reminder to sleep well before testing. What would this change?", ["It would introduce a possible alternative explanation for the score difference.", "It would make recruitment random.", "It would eliminate individual differences in sleep.", "It would guarantee that the reminder caused the difference."], "A", "The reminder would vary systematically with study method. Its possible effect could no longer be separated from the study method using this comparison alone."]
    ]
  },
  cars: {
    title: "What a map leaves out",
    content: "The first map in our town archive shows every bend of the river but no footpaths. A critic calls it incomplete. Yet its maker collected tolls from boats, and a footpath would have told her little about the cargo rounding the bend. A walker might prefer a sketch that makes the river nearly straight but marks every crossing. Neither map earns our trust by including everything. Each earns it by making its omissions intelligible. The danger begins when the toll collector's map is hung in the town hall without a caption, and the absence of footpaths becomes evidence that nobody walked.",
    items: [
      ["easy", "Which claim best captures the author's main point?", ["Old maps are more trustworthy.", "A useful map must depict all travelers.", "A map should be interpreted in light of its purpose.", "Officials should draw only rivers."], "C", "The author defends different omissions for different purposes. The warning concerns readers who no longer know why something was left out."],
      ["medium", "Why does the author introduce the walker's sketch?", ["To establish that the river changed course", "To show how a different purpose changes which details matter", "To challenge the legality of tolls", "To show that walkers ignored rivers"], "B", "The walker values crossings more than exact bends. That comparison shows why maps serving different users can reasonably omit different details."],
      ["hard", "Which example most closely parallels the author's final warning?", ["A guide explains that its route avoids stairs.", "A traveler compares two timetables.", "A catalog lists its selection rules.", "A historian uses a tax roll to conclude that no untaxed residents lived in a town."], "D", "The historian treats omission from a purpose-specific record as proof of absence, just as the captionless map might make walkers seem nonexistent."]
    ]
  }
};

export function starterResponse(settings: ReturnType<typeof sessionSettings>) {
  const questions: Question[] = [];
  for (const group of allocateSections(settings.section, settings.count)) {
    const { title, content, items } = bank[group.section];
    const passage = settings.format === "passage" || group.section === "cars";
    const eligible = items.filter(([level]) => settings.difficulty === "mixed" || level === settings.difficulty);
    for (const [level, stem, choices, answer, explanation] of eligible.slice(0, group.count)) {
      questions.push({
        id: "starter-" + group.section + "-" + level, section: group.section, topic: title,
        difficulty: level, question_text: passage ? stem : content + "\n\n" + stem,
        passage: passage ? { title, content } : undefined,
        choice_a: choices[0], choice_b: choices[1], choice_c: choices[2], choice_d: choices[3],
        correct_answer: answer, explanation, wrongAnswerExplanations: {}
      });
    }
  }
  return Response.json({ source: "starter", section: settings.section, questions });
}
