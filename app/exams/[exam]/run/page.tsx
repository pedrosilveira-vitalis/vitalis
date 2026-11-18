import ExamRunner from "@/components/exam/ExamRunner";

/**
 * The runner deliberately renders without the site's navigation. There is no
 * way back to the dashboard mid-section, because on test day there is no way
 * out of the room either.
 */
export default async function RunExamPage({ params }: { params: Promise<{ exam: string }> }) {
  const { exam } = await params;
  return <ExamRunner examId={exam} />;
}
