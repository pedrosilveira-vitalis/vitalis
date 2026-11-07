# Vitalis: Nori, streaks and calls

## What's included

- Responsive vector Nori beside the sidebar wordmark, on the homepage and beside the separate lesson wordmark.
- Floating, keyboard-accessible Nori links to the existing /tutor chat. The tutor introduces itself as Nori.
- Glossy burgundy buttons, dimensional cream cards and navy panels. Reduced-motion preferences respected.
- Homepage streak, seven-day history, best streak, total days visited and practice goal progress.
- A signed-in student's first submitted practice, lesson or homepage warm-up answer completes the day. Repeated answers/tabs do not increment it twice. A missed practice day breaks the current streak; best streak and visit totals persist.
- Upcoming calls on the dashboard and /calls. Admin /admin/calls creates, edits and cancels appointments assigned to a student's Google sign-in email. Students see only their own calls. Zoom links are supplied by the admin, not created through Zoom's API; no invitations or reminder emails are sent.
- Fixed the existing practice-explanation API mismatch with the actual question screen payload.

## Production configuration

Keep the existing POSTGRES_URL, AUTH_SECRET (or NEXTAUTH_SECRET), Google sign-in configuration and ANTHROPIC_API_KEY in the appropriate Vercel environment. No secret values are included in this update.

The admin defaults to pedrodocoutto@gmail.com. To change this, set server-only VITALIS_ADMIN_EMAILS to a comma-separated list of permitted sign-in emails.

On the first signed-in request, the PostgreSQL role needs permission to create vitalis_profiles, vitalis_days, vitalis_calls and their index. No existing tables are deleted or altered. If your database role cannot create tables, have the database administrator apply the statements in lib/portal-store.ts before enabling the feature.

Visit and streak history starts when this update is installed. Earlier login dates cannot be reconstructed from data that was never recorded. The timezone is fixed on the account's first tracked visit; midnight in that zone starts a new day. The progress bar tracks practice consistency, not a predicted or guaranteed MCAT score.

## Verification

Production Next.js build and TypeScript check passed. All 18 tests passed, including actual embedded PostgreSQL tests for concurrent activity updates, retries, date boundaries, student isolation, reassignment and cancellation. Question token tampering, expiry and invalid Zoom hosts are tested.

Browser visual testing is unverified: this environment's managed launcher supplied unsupported arguments to Next.js. Live Google sign-in, production database permissions, Anthropic responses and actual Zoom meetings require a preview check with your configuration. Nothing has been deployed to your Vercel project by this update.

## Preview acceptance check

1. Open the new Vercel Preview and sign in as a student. The dashboard should display Nori, a streak card and upcoming calls.
2. Submit one question. Confirm today's check and a one-day streak; refresh and submit again to confirm it remains one day. Days visited should remain one for that date.
3. Click floating Nori and ask a question in the tutor.
4. Sign in as the administrator at /admin/calls. Create a future call using a student email and a Zoom meeting URL. Sign in as that student and verify it appears under /calls; another student should not see it.
5. Edit and cancel the appointment, and verify the student portal updates. Check the pages on a phone-sized screen.
6. After preview acceptance, merge the feature branch into main to deploy through the existing Vercel integration.
