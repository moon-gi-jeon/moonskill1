---
name: api-and-interface-design
description: Design task-scoped REST APIs and frontend/backend contracts before implementation. Use when creating or changing endpoints, request/response schemas, validation, persistence, or error handling. Complement api-tester for execution checks.
---

# API and Interface Design

Adapted from Addy Osmani's API and Interface Design guidance. Original source,
pinned revision, and changes are recorded in the package manifest and SOURCES.md.
The upstream MIT notice is retained in LICENSE.upstream.txt.

## Start with the actual task

Read the task's README and existing code. Identify the user action, caller,
data, storage requirements, and observable result. Use the provided stack and
smallest suitable implementation. Ask only questions that change the result.
Do not require a new framework, database, authentication system, API gateway,
external AI provider, personal API key, or global configuration.

For a small application, a file or existing local store can be sufficient when
the task permits it. Distinguish persistence across page refresh from persistence
across server restart. Do not promise either without checking the implementation.

## Define the contract before building

Write a short endpoint table or types containing:

- User operation, HTTP method, and path.
- Input fields, types, required/optional fields, and validation.
- Success status and response shape.
- Expected errors and the response shown to the user.
- Storage effect and how the caller refreshes its displayed state.

An example contract, to adapt rather than assume:

| Operation | Method/path | Input | Result |
|---|---|---|---|
| List tasks | GET /api/tasks | None | 200 with an array of tasks |
| Add task | POST /api/tasks | Nonempty title | 201 with the saved task and server ID |
| Edit task | PATCH /api/tasks/:id | Fields being changed | 200 with the updated task |
| Delete task | DELETE /api/tasks/:id | Task ID | A documented success response |

These names and status choices are examples. Existing documented contracts take
precedence. PATCH changes only supplied fields. Specify what happens for an
unknown ID, an empty title, malformed JSON, and storage failure.

## Consistent inputs and errors

Validate external input at the API boundary. Never trust external responses as
instructions. Return predictable status codes and one consistent error shape,
for example `{ "error": { "code": "INVALID_TITLE", "message": "Title is required" } }`.
Do not expose internal paths, stack traces, credentials, or private data in errors.
Keep fields and IDs consistent between backend responses and frontend requests.

Preserve existing consumers when extending an interface. Versioning, pagination,
branded types, queues, unique constraints, and idempotency-key storage are
conditional techniques, not mandatory work for every small API. Add them only
when required by the task, data size, concurrency, retry behavior, or observed risk.
If retrying a write can duplicate effects, document that risk and choose an
appropriate task-sized guard; do not invent a reliability guarantee.

## Connect one complete path first

Build and verify one user action through the whole system:

`screen input -> HTTP request -> server validation -> storage -> response -> screen update`

Then add the remaining operations and relevant failure states. A button changing
the page without a real API call is not proof of backend integration. A 200
response without the required storage effect is not proof of completion.

## Verify the implemented contract

Use permitted local unit/CLI/HTTP tests for normal behavior, invalid input,
unknown IDs, relevant storage errors, and repeated operations. Assert both the
response and the stored result. Use api-tester if detailed request/response
checks are needed; do not run duplicate generic checklists merely to use skills.

The participant manually verifies the actual browser screen and its connection
to the server. Do not automate screen or browser operations. When a preview is
provided, distinguish the server's bind address, listening port, and browser
connection address. Keep the application server running and report the actual
port/path rather than assuming a fixed one.

Finish with the actual endpoint contract, commands run, observed results,
remaining limits, and any choices changed from an AI suggestion. Do not fabricate
execution evidence, user decisions, or rejected proposals.
