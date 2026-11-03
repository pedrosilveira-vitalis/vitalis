import { sections } from "@/lib/practice";
import { catalog } from "../generate/rotation";

export async function GET() {
  const {rows,connected}=await catalog();
  return Response.json({ total:rows.length, guideBankAvailable:connected, counts:Object.fromEntries(sections.map(s=>[s,rows.filter(q=>q.section===s).length])) });
}
