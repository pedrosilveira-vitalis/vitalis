# Vitalis update — October 31, 2026

## Included
- Rebuilt overview page with immediate practice/lesson actions, subject cards and a five-question starting session.
- Desktop sidebar and accessible native mobile menu in the shared navigation; study landing now uses it too. Existing pages with their own custom navigation are not all migrated yet.
- Preserved cream/navy/burgundy palette; visible keyboard focus and reduced-motion support; real page metadata.
- Practice: shared validated response format, exact requested count, requested difficulty, balanced mixed sections, passage support, explanations for chosen distractors, tutor available after correct or incorrect answers.
- Practice tutor now receives question, answer and passage context. New-session button resets the session.
- Explicit AI timeouts and bounded client requests; practice requests cancel on navigation.
- Flashcard generator returns the expected cards array and honors requested count.
- Study landing shows a retryable error instead of silently treating failed responses as content.
- Removed the unverified human-review claim from the practice landing.

## Verification
Production `npm run build` passed. TypeScript check passed.
`npm test`: 12 passing tests, including mocked AI responses through the actual practice and explanation route handlers. No paid AI requests were made.
Browser visual QA was blocked: the managed preview service supplies --host and --strictPort flags unsupported by Next.js. A successful build does not verify appearance on actual devices.
Live generation, authentication and database connectivity still require testing in the existing host's preview environment with its environment variables. The production loading delay cannot be conclusively diagnosed without logs.

## Deploy on your existing host
1. Back up or commit the current repository.
2. Copy the files from this folder into the corresponding repository root. Preserve your host's environment variables and any local secrets; none are included in this archive. Do not place this entire folder inside another copy of the app.
3. Run `npm ci`, `npm test`, then `npm run build`.
4. Create a preview deployment using the existing hosting provider/repository workflow. Do not change the domain.
5. Keep ANTHROPIC_API_KEY, POSTGRES_URL, Google sign-in credentials and Auth.js configuration as configured on the current host. Check server logs if a service is unavailable. Generation routes allow up to 120 seconds; confirm the host supports that execution duration.
6. In preview, verify practice with 5 and 20 questions, every section, hard difficulty, mixed mode, CARS passages, correct/incorrect grading, tutor follow-up, new session, and flashcards. Test mobile navigation at 375 px and desktop at 1440 px, including keyboard navigation.
7. Promote the preview after these checks. Keep the previous deployment available for rollback.

## Next work
- Persistent practice sessions, resume/history and a real review queue.
- Database-backed progress on the homepage; current overview intentionally contains no invented activity or scores.
- Finish migrating custom navigation on remaining pages.
- Content review and issue reporting, dated sources for score calculator.
- Usage limits, subscription enforcement, billing and cost monitoring before paid launch.
- Broader accessibility and device testing. The practice setup/tutor dialogs still need a complete focus-management audit.

No database migrations, billing, subscriptions or live-site deployment are included in this update.
