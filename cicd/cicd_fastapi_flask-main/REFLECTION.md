# Reflection

**What does each stage of the pipeline actually protect against?**
The lint stage (`black --check` + `flake8`) protects against inconsistent
formatting and basic style/quality issues (unused imports, overly long lines,
syntax smells) — it catches things a human reviewer would otherwise have to
nitpick by hand. The test stage (`pytest`) protects against actual behavioral
regressions: if a code change breaks an endpoint, changes a status code, or
removes validation, the tests fail and the change never gets a green check.
The deploy stage protects production from receiving code that hasn't been
verified at all — it's the gate that turns "code on a branch" into "code
running for users."

**Why does the order matter — what could go wrong if `deploy` ran before `test`?**
If `deploy` ran before (or independently of) `test`, a broken commit — one
that fails its tests or doesn't even import correctly — could get pushed
straight to production. The entire point of `needs: test` is to make the
deploy job *causally* dependent on the test job's success, so a red test run
blocks the release automatically, with no human having to remember to check
first. Without that ordering, CI becomes just a reporting tool instead of an
actual safety gate.

**What's one thing you'd add to make this pipeline closer to a real production setup?**
I'd add a real deployment target instead of the simulated `echo` step — for
example, building a Docker image, pushing it to a registry, and triggering a
deploy on a host like Render or Railway using a secret API token stored in
GitHub Secrets. I'd also add a test/coverage threshold step and a staging
environment so changes get verified in a near-production setting before
hitting `main` for real users.
