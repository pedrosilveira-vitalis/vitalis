/**
 * Transactional email over Resend's REST API.
 *
 * No SDK: this workspace cannot install packages, and the whole surface is one
 * POST. Every send is best effort — an email that fails must never break the
 * thing that triggered it, because losing a signup to a mail outage would be a
 * far worse bug than a missing welcome note.
 */
const ENDPOINT = "https://api.resend.com/emails";

export function emailConfigured(): boolean {
  return Boolean(process.env.RESEND_API_KEY);
}

function sender(): string {
  // Resend lets you send from onboarding@resend.dev before a domain is
  // verified, which is enough to test the whole path.
  return process.env.EMAIL_FROM || "Vitalis <onboarding@resend.dev>";
}

function siteUrl(): string {
  return (process.env.NEXT_PUBLIC_SITE_URL || "https://vitalis-lyart.vercel.app").replace(/\/$/, "");
}

export async function sendEmail(input: { to: string; subject: string; html: string; text: string }): Promise<boolean> {
  if (!emailConfigured()) return false;
  try {
    const response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ from: sender(), to: [input.to], subject: input.subject, html: input.html, text: input.text }),
    });
    if (!response.ok) {
      console.error("Email send failed", response.status, await response.text().catch(() => ""));
      return false;
    }
    return true;
  } catch (error) {
    console.error("Email send threw", error);
    return false;
  }
}

/** House style: the same warm palette as the site, and no images to be blocked. */
function wrap(heading: string, body: string, cta?: { label: string; href: string }): string {
  return `<!doctype html><html><body style="margin:0;padding:0;background:#f5f1ea;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f1ea;padding:32px 16px;">
<tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#fcfaf6;border:1px solid #e0d9ce;border-radius:14px;padding:36px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#0c1a2e;">
<tr><td>
<div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#8d6b59;font-weight:600;margin-bottom:18px;">Vitalis &middot; MCAT preparation</div>
<h1 style="margin:0 0 16px;font-size:26px;line-height:1.25;font-weight:500;">${heading}</h1>
${body}
${cta ? `<div style="margin-top:28px;"><a href="${cta.href}" style="display:inline-block;background:#245574;color:#f5f1ea;text-decoration:none;padding:14px 26px;border-radius:10px;font-size:14px;font-weight:600;">${cta.label}</a></div>` : ""}
<p style="margin:30px 0 0;padding-top:20px;border-top:1px solid #e9e3d9;font-size:12px;color:#8b8b83;line-height:1.6;">
You're receiving this because you have a Vitalis account.
</p>
</td></tr></table></td></tr></table></body></html>`;
}

const P = `margin:0 0 14px;font-size:15px;line-height:1.7;color:#3d4a56;`;

export async function sendWelcome(to: string, name?: string | null): Promise<boolean> {
  const first = (name || "").trim().split(" ")[0];
  const hello = first ? `Welcome, ${first}.` : "Welcome to Vitalis.";
  return sendEmail({
    to,
    subject: "Welcome to Vitalis",
    html: wrap(
      hello,
      `<p style="${P}">Your account is ready. Everything here was built one concept at a time &mdash; 250 lessons, each one checked line by line against published sources, and 1,250 practice questions with a full written explanation on every answer.</p>
       <p style="${P}">If you're not sure where to begin, the study planner will build you a schedule around your test date. If you'd rather just start, try five questions and see what sticks.</p>`,
      { label: "Start studying", href: `${siteUrl()}/study-plan` },
    ),
    text: `${hello}\n\nYour account is ready. 250 lessons, all source-checked, and 1,250 practice questions with full explanations.\n\nStart here: ${siteUrl()}/study-plan`,
  });
}

export async function sendPurchase(to: string, plan: string, days: number, expiresAt: Date): Promise<boolean> {
  const until = expiresAt.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
  return sendEmail({
    to,
    subject: `Your Vitalis ${plan} access is live`,
    html: wrap(
      `${plan} is live.`,
      `<p style="${P}">You have ${days} days of access, through <strong>${until}</strong>. Stripe has emailed your receipt separately.</p>
       <p style="${P}">A good first move is the study planner &mdash; give it your test date and it will lay the units out across the time you actually have.</p>`,
      { label: "Open Vitalis", href: `${siteUrl()}/study` },
    ),
    text: `${plan} is live. ${days} days of access, through ${until}.\n\n${siteUrl()}/study`,
  });
}

export async function sendRenewalWarning(to: string, plan: string, daysLeft: number): Promise<boolean> {
  return sendEmail({
    to,
    subject: `Your Vitalis access ends in ${daysLeft} days`,
    html: wrap(
      `${daysLeft} days left.`,
      `<p style="${P}">Your ${plan} window closes in ${daysLeft} days. Your progress, flashcards and flagged questions all stay exactly where they are &mdash; extending just reopens them.</p>
       <p style="${P}">If your test has moved, a longer window is usually better value than renewing twice.</p>`,
      { label: "Extend your access", href: `${siteUrl()}/plans` },
    ),
    text: `Your ${plan} window closes in ${daysLeft} days. Your progress is kept.\n\nExtend: ${siteUrl()}/plans`,
  });
}
