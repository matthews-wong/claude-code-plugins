# TypeScript Typing Examples (worked)

## Ban `any` — use `unknown` + narrowing

```ts
// Don't — any silently disables all checking downstream
function parse(json: string): any {
  return JSON.parse(json);
}

// Do — return unknown and narrow at the point of use
function parse(json: string): unknown {
  return JSON.parse(json);
}

function isUser(v: unknown): v is { id: string; name: string } {
  return (
    typeof v === 'object' && v !== null &&
    'id' in v && typeof (v as Record<string, unknown>).id === 'string' &&
    'name' in v && typeof (v as Record<string, unknown>).name === 'string'
  );
}

const data = parse(raw);
if (isUser(data)) {
  data.name; // fully typed here
}
```

For real projects, prefer a schema validator (Zod, Valibot) that produces the
type and the runtime guard from one source:

```ts
import { z } from 'zod';
const User = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof User>;
const user = User.parse(data); // throws on bad input, typed on success
```

## Discriminated unions

```ts
// Don't — impossible states are representable
interface Result {
  ok: boolean;
  data?: string;
  error?: string;
}

// Do — the `status` tag makes each variant exact
type Result =
  | { status: 'success'; data: string }
  | { status: 'error'; error: string };

function render(r: Result): string {
  switch (r.status) {
    case 'success':
      return r.data;  // `error` doesn't exist here
    case 'error':
      return r.error; // `data` doesn't exist here
    default:
      return assertNever(r);
  }
}

function assertNever(x: never): never {
  throw new Error(`Unhandled variant: ${JSON.stringify(x)}`);
}
```

The `assertNever` default makes the compiler error if a new variant is added but
not handled — exhaustiveness for free.

## readonly + as const

```ts
interface Point {
  readonly x: number;
  readonly y: number;
}

function sum(nums: readonly number[]): number {
  // nums.push(1); // compile error — good
  return nums.reduce((a, b) => a + b, 0);
}

const ROLES = ['admin', 'editor', 'viewer'] as const;
type Role = (typeof ROLES)[number]; // 'admin' | 'editor' | 'viewer'
```

## Generics with constraints

```ts
// Don't — bare T behaves like any at the call boundary
function first<T>(list: T[]): T {
  return list[0];
}

// Do — constrain, and let inference do the work
function pluck<T, K extends keyof T>(items: readonly T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const names = pluck(users, 'name'); // string[] inferred, 'name' checked
```

## satisfies — validate without widening

```ts
type Config = Record<string, { url: string; retries: number }>;

// Don't — annotation widens; `services.api.url` is just string,
// and excess keys inside can slip through.
const bad: Config = { api: { url: '/api', retries: 3 } };

// Do — satisfies checks the shape but keeps precise keys/types
const services = {
  api: { url: '/api', retries: 3 },
  auth: { url: '/auth', retries: 1 },
} satisfies Config;

services.api.retries; // number, and `services.api` is known to exist
```

## Derive, don't duplicate

```ts
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

type NewUser = Omit<User, 'id' | 'createdAt'>;
type UserPreview = Pick<User, 'id' | 'name'>;
type UserPatch = Partial<Omit<User, 'id'>>;
type UsersById = Record<User['id'], User>;
```

## Narrow instead of casting

```ts
// Don't
const el = document.querySelector('.btn') as HTMLButtonElement;

// Do
const el = document.querySelector('.btn');
if (el instanceof HTMLButtonElement) {
  el.disabled = true;
}
```
