import { Pool } from "pg";
import { portalSchema, type Database } from "./portal-store";
let pool: Pool | undefined;
let ready: Promise<void> | undefined;
export async function portalDb(): Promise<Database> {
  if (!process.env.POSTGRES_URL) throw new Error("Database is not configured.");
  pool ??= new Pool({ connectionString: process.env.POSTGRES_URL, ssl: { rejectUnauthorized: false }, connectionTimeoutMillis: 8000, max: 4 });
  const db = pool;
  ready ??= (async () => {
    const connection = await db.connect();
    try {
      await connection.query("BEGIN");
      await connection.query("SELECT pg_advisory_xact_lock(84619207)");
      for (const statement of portalSchema) await connection.query(statement);
      await connection.query("COMMIT");
    } catch (error) { await connection.query("ROLLBACK"); throw error; }
    finally { connection.release(); }
  })().catch(error => { ready = undefined; throw error; });
  await ready;
  return db;
}
