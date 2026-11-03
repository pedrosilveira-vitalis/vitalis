import { type Question, type Section } from "@/lib/practice";

type Item = [level: string, stem: string, choices: [string, string, string, string], answer: string, explanation: string];
type Reading = { title: string; content: string; items: Item[] };

const bank: Record<Section, Reading> = {
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

const more: Record<Section, Reading> = {
  "bio-biochem": { title: "A pulse of labeled DNA", content: "Cells grow for many generations in heavy nitrogen. Researchers then switch them to light nitrogen and let them divide synchronously. After the first round of replication, all DNA molecules have intermediate density. After the second, equal numbers have intermediate and light density.", items: [
    ["easy","What makes the original DNA heavy? ",["Extra phosphate groups","An isotope incorporated into its bases","Extra strands","A longer sugar backbone"],"B","Nitrogen occurs in the bases. Substituting a heavier nitrogen isotope increases DNA density."],
    ["medium","What accounts for the intermediate band after one division?",["Each duplex contains one original and one new strand.","Every molecule has two new strands.","The heavy strands disappeared.","Only half the cells replicated."],"A","Semiconservative replication pairs each original heavy strand with a newly synthesized light strand."],
    ["hard","After a third complete round in light nitrogen, what fraction of duplexes would have intermediate density?",["One half","One eighth","Three quarters","One quarter"],"D","Each original duplex gives eight descendants after three rounds. Its two original strands persist in two of those eight duplexes."]
  ]},
  "chem-phys": { title: "Two resistors on a bench", content: "A student connects two ideal 6-ohm resistors in series across a 12-volt ideal battery. The wires have negligible resistance. She then disconnects the battery and rewires the same resistors in parallel before reconnecting it.", items: [
    ["easy","What current flows through the original series circuit?",["0.5 A","1 A","2 A","4 A"],"B","Series resistances add to 12 ohms. Dividing 12 volts by 12 ohms gives 1 ampere."],
    ["medium","After rewiring, what voltage appears across a single resistor?",["3 V","6 V","12 V","24 V"],"C","Each parallel branch connects directly across both battery terminals and has the full 12-volt potential difference."],
    ["hard","How does the total power delivered by the battery change after rewiring?",["It doubles.","It halves.","It stays the same.","It quadruples."],"D","Equivalent resistance falls from 12 to 3 ohms. With voltage fixed, total power equals voltage squared divided by resistance and increases fourfold."]
  ]},
  "psych-soc": { title: "Listening for a signal", content: "Participants press a button when they think a faint tone is present. Half the trials contain a tone. In a second block the researchers keep the sounds identical but impose a larger penalty for missing a tone. Participants then report more hits and more false alarms.", items: [
    ["easy","A participant presses the button on a silent trial. How is that response classified?",["A hit","A miss","A correct rejection","A false alarm"],"D","A false alarm occurs when a participant reports a signal on a trial where it was absent."],
    ["medium","Which change in response strategy fits the second block?",["A more liberal criterion","A more conservative criterion","Responding only to louder tones","Ignoring the penalty"],"A","A lower threshold for reporting a signal produces more reports on both signal and silent trials."],
    ["hard","Which follow-up design best separates the effect of the penalty from a practice effect?",["Make every tone louder in block two.","Give all participants more trials in block two.","Counterbalance the order of the two penalty conditions.","Remove all silent trials."],"C","Counterbalancing prevents the high penalty from always occurring later, so familiarity with the task is less likely to explain the difference."]
  ]},
  cars: { title: "The borrowed chair", content: "A museum once displayed a chair behind glass to preserve the grooves worn into its arms. The label called those grooves signs of a living tradition. The maker's granddaughter disagreed: in her workshop, a chair stayed part of a tradition because someone still knew how to mend it. She did not ask the museum to let visitors sit on the fragile chair. Instead, she offered to teach apprentices to repair another one beside it. A curator worried the new work would distract from the original. Yet what better way to see an old joint than to watch a new one being fitted?", items: [
    ["easy","What does the granddaughter propose?",["Replacing the original chair","Demonstrating a repair on another chair","Removing the label and the glass","Testing the original under load"],"B","She offers to teach apprentices by repairing a second chair beside the protected original."],
    ["medium","Why does the author close with a question about fitting a joint?",["To dismiss the skill of the original maker","To ask readers to date the chair","To suggest a demonstration can deepen observation of the original","To argue that all museum visitors must become apprentices"],"C","The question answers the curator's concern by suggesting a way that new work can draw attention to details in the old piece."],
    ["hard","Which statement would the granddaughter most likely endorse?",["Visible wear alone ensures a craft survives.","Preserving a fragile object is always a mistake.","Replicas have greater value than originals.","A museum can preserve an object and help transmit the skill behind it."],"D","She accepts the original chair's protection and offers a complementary way to keep the craft alive."]
  ]}
};

export function starterQuestions(section: Section, format: string, difficulty: string): Question[] {
  const passage = format === "passage" || section === "cars";
  return [bank[section], more[section]].flatMap(({ title, content, items }, setIndex) =>
    items.filter(([level]) => difficulty === "mixed" || level === difficulty)
      .map(([level, stem, choices, answer, explanation]) => ({
        id: `starter-${section}-${setIndex}-${level}`, section, topic: title, difficulty: level,
        question_text: passage ? stem.trim() : content + "\n\n" + stem.trim(),
        passage: passage ? { title, content } : undefined,
        choice_a: choices[0], choice_b: choices[1], choice_c: choices[2], choice_d: choices[3],
        correct_answer: answer, explanation, wrongAnswerExplanations: {}
      }))
  );
}
