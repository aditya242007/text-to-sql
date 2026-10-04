# Rule 03 — SQL Safety (Always On, highest priority after the core principle)

The system is **read-only**. These rules are non-negotiable and must be enforced in CODE and in the DATABASE, not only in prompts.

## Never
- Execute any statement that is not a single `SELECT` / `WITH … SELECT`.
- Allow INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, COPY, SET, CALL, DO, `SELECT … INTO`, `FOR UPDATE`, stacked statements (`;`).
- Allow `pg_*` catalog access, `information_schema` from user SQL, or functions such as `pg_sleep`, `pg_read_file`, `lo_*`, `dblink`.
- Pass database credentials, connection strings, or secrets to an LLM or into logs.
- Execute SQL that has not passed BOTH Pydantic validation and the AST safety validator.
- Show raw database errors or stack traces to end users.

## Always
- Parse SQL with `sqlglot` (dialect `postgres`) and validate the AST; do not rely on regex/keyword blacklists alone.
- Check every table/column against the live introspected schema allow-list.
- Enforce a row limit (append `LIMIT` when missing; cap at 1000).
- Run via a dedicated read-only role (`analytics_ro`) with `default_transaction_read_only=on` and `statement_timeout`.
- Use a separate DB connection/engine for execution vs. admin/seeding.
- Treat user text and DB values as untrusted data (prompt-injection safe).
- Limit SQL repair retries to **2**; every repaired SQL goes through full validation again.
- Log: question, intent, SQL, verdict, duration, row count — never secrets.

## Tests required
Every blocked construct above needs a unit test proving it is rejected, plus an integration test proving the DB role cannot write.
