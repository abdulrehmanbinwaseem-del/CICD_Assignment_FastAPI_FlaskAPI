# Task Manager API — CI/CD Assignment (FastAPI)

A tiny Task Manager API with a health check, task listing, and task creation,
wrapped in a working CI/CD pipeline (lint → test → simulated deploy) using
GitHub Actions.

## Endpoints

| Method | Path      | Description                          |
|--------|-----------|---------------------------------------|
| GET    | `/health` | Health check, returns `{"status": "ok"}` |
| GET    | `/tasks`  | List all tasks                       |
| POST   | `/tasks`  | Create a task (`{"title": "...", "done": false}`) |

## Project structure

```
.
├── main.py                      # FastAPI app (starter code, unmodified)
├── test_main.py                 # pytest suite (5 tests)
├── requirements.txt             # runtime dependencies
├── requirements-dev.txt         # lint tooling (flake8, black)
├── setup.cfg                    # flake8 config (line length, excludes)
├── REFLECTION.md                # write-up for the wrap-up section
├── .github/workflows/ci.yml     # CI/CD pipeline: test job + deploy job
└── README.md
```

## Part 0 — Run it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI, or test
with curl:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Write tests"}'
```

## Part 1 — Run the tests

```bash
pip install -r requirements.txt
pytest -v
```

Expect `5 passed` (the assignment only required 4+).

## Part 2 — Run the lint/format gate locally

```bash
pip install -r requirements-dev.txt
black --check .
flake8 .
```

Both should report no issues. If `black --check` fails, run `black .`
(without `--check`) to auto-format.

## Part 3 & 4 — CI/CD pipeline

`.github/workflows/ci.yml` defines two jobs:

- **`test`** — triggers on `push` and `pull_request` to `main`. Checks out
  the code, sets up Python 3.12, installs dependencies, runs `black --check`
  and `flake8` as a lint step, then runs `pytest -v`.
- **`deploy`** — uses `needs: test`, so it only runs if `test` succeeds, and
  is gated with `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`
  so it never runs on pull requests. Its only step echoes a simulated
  deployment message using the short commit SHA.

### To see it in action on GitHub

1. Push this repo to GitHub.
2. Go to the **Actions** tab — you should see the `CI` workflow run and pass
   (`test` green, then `deploy` green, in that order).
3. To see a failing run: comment out an assertion in `test_main.py` (or
   introduce a formatting issue), commit, and push. The `test` job will go
   red and `deploy` will be skipped entirely.
4. Revert the change, commit, push again — back to green.

## Notes on implementation choices

- The starter `main.py` is kept exactly as given (per the assignment's
  rubric: "App runs locally — Starter app works unmodified").
- `requirements-dev.txt` separates lint tooling from runtime dependencies —
  a common pattern that keeps the production dependency list lean while
  still letting CI install everything it needs.
- `setup.cfg` sets flake8's max line length to 88 to match Black's default
  formatting width, and ignores `E203`/`W503`, the two warnings that are
  known to conflict with Black's style (this is Black's own documented
  recommendation for using it alongside flake8).
