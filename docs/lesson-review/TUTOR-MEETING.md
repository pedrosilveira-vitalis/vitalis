# Vitalis: tutor meeting brief

## Current checkpoint

Vitalis combines MCAT practice, study lessons, flashcards, a study planner, an on-page AI helper (Nori), flagged questions, a resume tool and a medical-news section.

**61 of 250 lessons and their 305 quiz questions have received source-backed targeted reviews and diagrams. 189 lessons remain.** The current batch adds 20 lessons, 100 quiz questions and 20 diagrams covering inheritance, mutation and repair, population genetics, membranes, signaling, cell division and cardiac physiology. This is not a claim that every scientific statement is certified or that the app has undergone independent expert review.

## Demonstrate in Preview

1. Homepage: blue glossy actions, Nori, practice streak and upcoming calls.
2. Answer a practice question while signed in. A celebration appears only after today's progress is saved. Refresh/repeat to confirm the day is not counted twice.
3. Open Nori while staying on the lesson. Ask a question; minimize and reopen.
4. Open a newly reviewed lesson: chromosomal linkage, passive transport or cardiac electrical conduction. Diagrams sit within the explanations and have a full-size link.
5. Generate flashcards. If the AI provider fails, the interface identifies the core fallback deck rather than pretending those cards were newly generated.

## A concrete role for a tutor

- Review scientific explanations and ambiguous questions independently.
- Assess whether diagrams improve understanding and identify missing worked examples.
- Prioritize remaining lessons based on student needs.
- Pilot the platform with a small group and gather feedback on misconceptions, pacing and usability.
- Discuss the tutor's availability, compensation, content responsibilities and the scope of any student calls before promising a service.

## Verification and limits

67 automated tests and the production build passed for this checkpoint. New scientific diagrams were rendered and inspected. Browser interaction, live AI and signed-in production flows still need checks in Vercel Preview. The earlier dependency audit findings have not been resolved in this feature update. The installer creates a Preview branch; it does not merge main or publish production.

The learning feedback supports consistency and reflection; it is not a claim to measure or guarantee dopamine release, retention, test scores or admissions outcomes.
