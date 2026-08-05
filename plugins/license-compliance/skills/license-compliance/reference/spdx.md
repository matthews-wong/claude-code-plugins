# SPDX identifiers

SPDX (Software Package Data Exchange) is an open standard (ISO/IEC 5962:2021) for communicating software bill-of-materials information, including licensing. The **SPDX License List** assigns each recognized license a short, canonical identifier.

## Why identifiers matter

Free-text license fields are ambiguous ("BSD", "GPL", "Apache"). SPDX identifiers remove ambiguity:

- `MIT` — MIT License
- `Apache-2.0` — Apache License 2.0
- `BSD-2-Clause`, `BSD-3-Clause`
- `ISC`
- `MPL-2.0` — Mozilla Public License 2.0
- `LGPL-3.0-only`, `LGPL-3.0-or-later`
- `GPL-2.0-only`, `GPL-2.0-or-later`, `GPL-3.0-only`, `GPL-3.0-or-later`
- `AGPL-3.0-only`, `AGPL-3.0-or-later`
- `Unlicense`, `CC0-1.0`

## `-only` vs `-or-later`

Modern SPDX uses explicit suffixes instead of the ambiguous trailing `+`:
- `GPL-3.0-only` — exactly version 3.0.
- `GPL-3.0-or-later` — version 3.0 or any later version, at the licensee's option.

Legacy identifiers like `GPL-3.0` are deprecated in favor of the explicit forms.

## License expressions

SPDX supports compound expressions:
- Dual licensing / choice: `(MIT OR Apache-2.0)` — you may pick either.
- Conjunction: `(MIT AND BSD-3-Clause)` — both apply.
- Exceptions: `GPL-2.0-or-later WITH Classpath-exception-2.0`.

When a package declares an expression, evaluate every arm: a choice license lets you select the compatible option; an `AND` means all obligations apply.

## Practical notes

- `NOASSERTION` / `UNKNOWN`: the tooling could not determine a license. Resolve before shipping.
- Package metadata may differ from the actual LICENSE file — for high-risk dependencies, verify against the source repository.
- Full list: https://spdx.org/licenses/
