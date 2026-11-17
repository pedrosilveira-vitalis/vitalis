# Switching on checkout

Three things only you can do. Nothing here needs a developer.

## 1. Create the Stripe account

Go to stripe.com, create a business account, and finish the activation form
(legal entity, EIN or SSN, bank account for payouts). Until activation is
complete Stripe will run in test mode, which is fine for checking the flow but
will not take real money.

## 2. Turn on the payment methods

Stripe Dashboard -> Settings -> Payment methods. Switch on:

- Cards (on by default)
- Apple Pay
- Google Pay
- Cash App Pay
- Link

The checkout page is hosted by Stripe, so Apple Pay needs no domain
verification from us. Whatever you enable here is what students see.

## 3. Add three environment variables in Vercel

Vercel -> the Vitalis project -> Settings -> Environment Variables. Add these
yourself; do not paste the secret key into a chat window, including this one.

| Name | Where it comes from |
|---|---|
| `STRIPE_SECRET_KEY` | Stripe -> Developers -> API keys -> Secret key (`sk_live_...`) |
| `STRIPE_WEBHOOK_SECRET` | Created in step 4 below (`whsec_...`) |
| `NEXT_PUBLIC_SITE_URL` | `https://vitalis-lyart.vercel.app` (no trailing slash) |
| `FREE_ACCESS_EMAILS` | Your own email, plus any tutor or beta student, comma separated |

### About `FREE_ACCESS_EMAILS`

Lessons and the question bank are now behind the paywall, which includes being
behind it for you. Anyone listed here gets everything without paying, so put
your own address in before you look at the site again, along with your tutors
and any beta students you have promised access to.

Example: `pedro@example.com,tutor@example.com`

## 4. Create the webhook

Stripe -> Developers -> Webhooks -> Add endpoint.

- Endpoint URL: `https://vitalis-lyart.vercel.app/api/stripe/webhook`
- Event to send: `checkout.session.completed` (that one only)

Stripe shows you a signing secret starting `whsec_`. That is
`STRIPE_WEBHOOK_SECRET`.

This step is not optional. Access is granted by the webhook and nowhere else,
because the success page is just a redirect that anyone could type into their
address bar. No webhook secret means no access is ever granted, even after a
successful payment.

## 5. Redeploy

Environment variables only take effect on a new deployment. Vercel -> 
Deployments -> Redeploy.

## Testing before you go live

Use the test-mode keys first. Stripe's test card is `4242 4242 4242 4242`, any
future expiry, any CVC. Walk the whole path: pick a plan, pay, confirm access
appears, then check the row landed in `vitalis_entitlements`.

## Referral codes

A code is any string of 3 to 24 letters, digits or hyphens, for example
`SARAH-K`. Codes are not pre-registered anywhere: whatever the student types is
stored with the purchase, so you can count them at the end of the month and pay
the tutor on the same number the student was discounted by.

The discount only applies where a plan genuinely lists higher than it sells, so
a code takes $100 off Complete and nothing off Core. That is deliberate. Core's
list price and its real price are the same number, and discounting from a price
that was never charged is a fictitious reference price under FTC guidance.
