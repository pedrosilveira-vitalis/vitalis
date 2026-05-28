import { auth } from "@/auth";

export async function GET() {
  const session = await auth();
  if (!session?.user) {
    return Response.json({ user: null });
  }
  return Response.json({
    user: {
      name: session.user.name || null,
      email: session.user.email || null,
      image: session.user.image || null,
    },
  });
}