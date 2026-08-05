# Communications templates

Fill only what is known. Leave `[unknown]` where you lack facts — never guess.
Always end with the next update time.

## Internal status update (channel / bridge)

```
[SEV<n>] <short title> — <status: Investigating | Identified | Monitoring | Resolved>
Time: <UTC timestamp>
Impact: <who/what is affected, since when>
Current status: <what we know and what we're doing right now>
Owner (IC): <name>
Next update: <time>
```

## External / customer status update

Investigating:
```
We are investigating <reports of / an issue affecting> <service/feature>.
Some users may experience <observable symptom>. We are working to resolve this
and will share an update by <time>.
```

Identified:
```
We have identified the cause of the issue affecting <service/feature> and are
working on a fix. <Optional: workaround.> Next update by <time>.
```

Monitoring:
```
A fix has been applied and we are monitoring the results. <Service/feature>
should now be operating normally. We will confirm full resolution by <time>.
```

Resolved:
```
This incident has been resolved as of <time>. <Service/feature> is operating
normally. We apologize for the disruption. A summary will follow <if applicable>.
```

## Guidelines

- Symptoms, not internals: say "users can't log in," not stack traces.
- No blame, no naming of individuals or vendors as at fault.
- No root cause or ETA you cannot support; "we will update by <time>" is always
  better than a guessed fix time.
- Keep external updates shorter than internal ones.
- Match cadence to severity (SEV1 ~30 min, SEV2 ~hourly).
- For security incidents, route external wording through security/legal per
  policy before publishing.
