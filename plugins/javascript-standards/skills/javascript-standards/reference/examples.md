# JavaScript Examples (before / after)

## ESM modules

```js
// Don't (CommonJS)
const { readFile } = require('node:fs/promises');
module.exports = { load };

// Do (ESM, named exports)
import { readFile } from 'node:fs/promises';
export { load };
```

## const / let / no var

```js
// Don't
var total = 0;
for (var i = 0; i < items.length; i++) total += items[i].price;

// Do
const total = items.reduce((sum, item) => sum + item.price, 0);
```

## Strict equality + nullish

```js
// Don't
function connect(opts) {
  const timeout = opts.timeout || 3000; // breaks when timeout === 0
  if (opts.retries == null) {}          // ok, but be explicit
}

// Do
function connect(opts) {
  const timeout = opts.timeout ?? 3000;
  const retries = opts.retries ?? 0;
}
```

## async/await over chains

```js
// Don't
function loadUser(id) {
  return fetch(`/api/users/${id}`)
    .then((r) => r.json())
    .then((u) => enrich(u))
    .catch(() => null); // swallows everything
}

// Do
async function loadUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`User ${id} failed: ${res.status}`);
  const user = await res.json();
  return enrich(user);
}
```

## Parallel independent work

```js
// Don't — serial
const a = await getA();
const b = await getB();

// Do — concurrent (a and b are independent)
const [a, b] = await Promise.all([getA(), getB()]);
```

## Error handling with cause

```js
// Don't
try {
  await save(record);
} catch (e) {
  // ...nothing
}

// Do
try {
  await save(record);
} catch (error) {
  throw new Error(`Failed to save record ${record.id}`, { cause: error });
}
```

## Immutability

```js
// Don't — mutates the caller's array
function addTag(item, tag) {
  item.tags.push(tag);
  return item;
}

// Do — returns a new object
function addTag(item, tag) {
  return { ...item, tags: [...item.tags, tag] };
}

// Sorting without mutating the source
const sorted = [...scores].sort((a, b) => b - a);
```

## Small pure functions + isolated side effects

```js
// Pure: easy to test, no I/O
function formatPrice(cents, currency = 'USD') {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency })
    .format(cents / 100);
}

// Side effect isolated at the edge
async function renderReceipt(order) {
  const line = formatPrice(order.totalCents, order.currency); // pure
  await writeToLog(line);                                     // effect
}
```
