'use client';

export default function PageError() {
  return <main className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] grid place-items-center p-6"><section role="alert" className="max-w-lg rounded-2xl border border-[#0c1a2e20] bg-[#fcfaf6] p-8"><h1 className="font-serif text-3xl mb-4">This page couldn’t load.</h1><p className="text-sm leading-7 mb-6">Please reload to try again, or return to your study dashboard.</p><div className="flex flex-wrap gap-3"><button className="button-primary" onClick={()=>window.location.reload()}>Reload page</button><a className="button-outline" href="/">Back to dashboard</a></div></section></main>;
}
