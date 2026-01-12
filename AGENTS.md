# Repository Guidelines

## Project Structure & Module Organization
- `efscape/` holds the primary Python package. Entry points and service logic live here (e.g., `efscape/arrowserver.py`).
- `arrowice/` is a companion package for Arrow-related Ice interfaces.
- `slice/` contains ZeroC Ice Slice definitions. Expect service contracts under `slice/efscape/` and `slice/arrowice/`.
- `tests/` is reserved for pytest tests (currently empty).
- `dist/` is a build artifact directory and should not be edited by hand.

## Build, Test, and Development Commands
- `uv sync` sets up the virtual environment with runtime and dev dependencies.
- `uv run python efscape/arrowserver.py` starts the Arrow Ice server (example runtime entry point).
- `uv run pytest` runs the test suite (add tests under `tests/`).
- `uv run ruff check .` runs linting.
- `uv run black .` formats the codebase.
- `uv build` produces distributable artifacts in `dist/`.

## Coding Style & Naming Conventions
- Follow Black formatting and Ruff linting defaults; keep line length consistent with Black.
- Use PEP 8 naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Keep Ice Slice files in `slice/**` and name them with clear service nouns (e.g., `ModelHome.ice`).

## Testing Guidelines
- Use pytest with files named `tests/test_*.py`.
- Prefer unit tests for service logic and integration tests for Ice interfaces.
- No coverage threshold is enforced yet; document any new test requirements in this file.

## Commit & Pull Request Guidelines
- Git history is minimal (initial commit only), so no strict commit convention exists yet. Use short, imperative subjects (e.g., "Add Arrow server logging").
- Pull requests should include: a concise description, how to test (commands + expected result), and any relevant issue links.

## Architecture Notes
- Ice Slice definitions are loaded at runtime via `Ice.loadSlice(...)`, so keep Slice paths stable and update imports if files move.
