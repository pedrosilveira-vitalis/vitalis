import MainNav from "@/components/MainNav";
import UpcomingCalls from "@/components/UpcomingCalls";
export default function CallsPage() {
  return <><MainNav contentId="calls-content" badge="Your calls"/><main id="calls-content" className="portal-page"><p className="eyebrow">YOUR SUPPORT TEAM</p><h1>Let’s talk about your next step.</h1><p>Appointments scheduled for your account, with times shown in your local timezone.</p><UpcomingCalls/></main></>;
}
