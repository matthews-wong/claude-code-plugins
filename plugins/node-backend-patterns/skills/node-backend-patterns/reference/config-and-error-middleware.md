# Config & error middleware

Reference implementations (Express + zod). The same ideas map directly to Fastify.

## Env config — validate once at startup, fail fast

```js
// config.js
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

const parsed = EnvSchema.safeParse(process.env);
if (!parsed.success) {
  // Crash on boot — a misconfigured process must never serve traffic.
  console.error("Invalid environment:", parsed.error.flatten().fieldErrors);
  process.exit(1);
}

// Single typed config object — the only place process.env is read.
export const config = Object.freeze(parsed.data);
```

## Typed domain error

```js
// errors.js
export class AppError extends Error {
  constructor(message, { status = 500, code = "INTERNAL_ERROR", details } = {}) {
    super(message);
    this.name = "AppError";
    this.status = status;
    this.code = code;       // stable machine-readable code
    this.details = details; // optional field-level info
    this.expose = status < 500; // safe to show the client?
  }
}
```

## Boundary validation middleware

```js
// validate.js
export const validate = (schema) => (req, res, next) => {
  const result = schema.safeParse({ body: req.body, params: req.params, query: req.query });
  if (!result.success) {
    return next(new AppError("Request validation failed", {
      status: 422,
      code: "VALIDATION_ERROR",
      details: result.error.issues.map((i) => ({ field: i.path.join("."), issue: i.message })),
    }));
  }
  req.valid = result.data; // trusted, typed input for the handler
  next();
};
```

## Async handler wrapper (Express 4)

```js
// async-handler.js — forwards rejected promises to the error middleware.
export const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

Usage keeps handlers free of try/catch:

```js
router.post("/orders", validate(CreateOrderSchema), asyncHandler(async (req, res) => {
  const order = await orderService.create(req.valid.body); // service: no req/res inside
  res.status(201).location(`/v1/orders/${order.id}`).json({ data: order });
}));
```

## Centralized error handler (mounted last)

```js
// error-middleware.js
import { config } from "./config.js";

// Express identifies error middleware by its 4 args — keep all four.
export function errorHandler(err, req, res, _next) {
  const status = err.status ?? 500;
  const payload = {
    error: {
      code: err.code ?? "INTERNAL_ERROR",
      message: err.expose ? err.message : "Something went wrong.",
      request_id: req.id,
    },
  };
  if (err.details) payload.error.details = err.details;

  // Log the full error server-side; never leak internals/stack to the client.
  req.log?.error({ err, request_id: req.id }, "request failed");
  if (config.NODE_ENV !== "production" && status >= 500) payload.error.stack = err.stack;

  res.status(status).json(payload);
}
```

Mount order: routes → 404 fallthrough → `errorHandler` last.
