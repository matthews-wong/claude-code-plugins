# Graceful shutdown & structured logging

## Why

On deploy or scale-down, orchestrators send `SIGTERM`. A process that exits immediately drops in-flight requests and can corrupt work mid-transaction. Drain cleanly, then exit.

## Structured logger (pino)

```js
// logger.js
import pino from "pino";
import { config } from "./config.js";

export const logger = pino({
  level: config.LOG_LEVEL,
  // Redact secrets/PII so they never reach the log sink.
  redact: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token"],
});
```

Attach a per-request child logger with a correlation id (e.g. `pino-http`, or manually):

```js
import { randomUUID } from "node:crypto";

app.use((req, res, next) => {
  req.id = req.headers["x-request-id"] ?? randomUUID();
  req.log = logger.child({ request_id: req.id });
  res.setHeader("x-request-id", req.id);
  next();
});
```

## Graceful shutdown

```js
// server.js
import { config } from "./config.js";
import { logger } from "./logger.js";
import { app } from "./app.js";
import { pool } from "./db.js"; // your DB/connection pool

const server = app.listen(config.PORT, () => {
  logger.info({ port: config.PORT }, "server listening");
});

let shuttingDown = false;

async function shutdown(signal) {
  if (shuttingDown) return;   // ignore repeated signals
  shuttingDown = true;
  logger.info({ signal }, "shutting down");

  // Force-exit if draining hangs, so a stuck connection can't block forever.
  const forceExit = setTimeout(() => {
    logger.error("drain timed out; forcing exit");
    process.exit(1);
  }, 10_000);
  forceExit.unref();

  // 1) Stop accepting new connections; wait for in-flight requests to finish.
  await new Promise((resolve) => server.close(resolve));

  // 2) Release downstream resources.
  await pool.end();

  clearTimeout(forceExit);
  logger.info("shutdown complete");
  process.exit(0);
}

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));

// Last-resort safety nets: log, then let the process restart cleanly.
process.on("unhandledRejection", (reason) => {
  logger.error({ reason }, "unhandled rejection");
  shutdown("unhandledRejection");
});
process.on("uncaughtException", (err) => {
  logger.fatal({ err }, "uncaught exception");
  process.exit(1); // state is unknown — exit and let the orchestrator restart.
});
```

## Notes

- Set `server.keepAliveTimeout`/`headersTimeout` sensibly and use `server.close()` (finishes active requests, refuses new ones) rather than `process.exit()` directly.
- For readiness probes, flip a `ready = false` flag at the start of `shutdown` so the load balancer stops routing new traffic before you close.
- `uncaughtException` leaves the process in an undefined state — log and exit; do not try to keep serving.
