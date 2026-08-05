# Coverage tooling reference

## Python — pytest-cov (coverage.py)

Install: `pip install pytest-cov`

Run:
```sh
pytest --cov --cov-report=term-missing
pytest --cov=my_package --cov-report=xml   # for CI upload
```

Threshold enforced by the tool itself:
```sh
pytest --cov --cov-fail-under=80
```

Config in `pyproject.toml`:
```toml
[tool.coverage.run]
branch = true
source = ["my_package"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

The `TOTAL` line of `term-missing` output ends with the aggregate percent.

## JavaScript / TypeScript — nyc or c8

nyc (Istanbul):
```sh
npx nyc --reporter=text-summary npm test
```
`.nycrc.json`:
```json
{ "branches": 80, "lines": 80, "functions": 80, "statements": 80,
  "check-coverage": true }
```
With `check-coverage`, nyc exits non-zero below threshold.

c8 (V8 native, good for ESM):
```sh
npx c8 --lines 80 --branches 80 --check-coverage npm test
```

Jest has built-in coverage:
```sh
jest --coverage --coverageThreshold='{"global":{"lines":80}}'
```

## Go — go test -cover

Per-package quick check:
```sh
go test -cover ./...
```

Aggregate profile + total:
```sh
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | tail -n1   # "total:" line has the percent
```

Go has no built-in fail-under flag; gate in CI by parsing the `total:` line.

## CI wiring pattern

1. Run coverage, produce a machine-readable total (XML/lcov/func output).
2. Compare to the threshold in the CI step and set exit code.
3. Optionally upload to Codecov / Coveralls for diff coverage on pull requests,
   which reports coverage of the changed lines only.
