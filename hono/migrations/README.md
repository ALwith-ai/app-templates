# Database migrations

The schema is defined by standard SQL migration files for node-pg-migrate. Write them from the product definition and commit them to Git. Never change a migration that has been applied.

The service role and the migration role are separate. Business tables enable row-level security, with policies based on the verified request identity. Independent QA verifies permission isolation, rollback, concurrency and connection reuse on a real PostgreSQL.
