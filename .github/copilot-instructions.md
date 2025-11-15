<!-- Copilot / agent instructions for the CarbonFootprint repo -->
# Copilot Instructions — sustainledger (CarbonFootprint)

Purpose: quick, actionable notes for an AI coding agent to be immediately productive in this Django repo.

**Quick Start:**
- **Create env & deps:** Use a virtualenv and install Django 5.2.x. Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1;
pip install "Django==5.2.8" mysqlclient   # or PyMySQL if preferred
```

- **Run DB migrations & server:**

```powershell
python manage.py migrate
python manage.py runserver
```

Note: `sustainledger/sustainledger/settings.py` is currently configured for MySQL (host `localhost:3306`, user `root`, password `admin`). A lightweight local alternative is the checked-in `db.sqlite3` file — edit `DATABASES` in `settings.py` to use sqlite for quick testing.

**Architecture (big picture):**
- **Project root:** `manage.py`, main settings at `sustainledger/sustainledger/settings.py`.
- **Apps:** `Core` and `Emissions` are the two primary Django apps. `Core` holds facility metadata (`Core/models.py` defines `core`), `Emissions` stores activity records and emission-factors (`Emissions/models.py` defines `EmissionFactor`, `Activity`, `ConvertedEmission`).
- **Data flow:** user-submitted `Activity` (e.g., kWh, liters, km) + `EmissionFactor` -> `ConvertedEmission` (calculated CO2e). Look in `Emissions/models.py` for the model relationships.
- **Templates & static:** Templates live in top-level `TEMPLATES/` (configured in `settings.py`) and under `TEMPLATES/Core` / `TEMPLATES/Emissions`. Static assets are in `static/` (see `STATICFILES_DIRS`).

**Project-specific conventions & gotchas:**
- **Model naming:** The `Core` app uses a lowercase model class name `core` (not `Core` or `CoreModel`). When referencing the model in code use the symbol defined in `Core/models.py` — avoid renaming without migrating.
- **Templates directory:** Templates are in a top-level `TEMPLATES/` folder (not the default app template directories only). Use `'DIRS': ['TEMPLATES']` as configured.
- **Views patterns:** Views are simple function-based views that often render templates directly. Example: `Core/views.py` defines `index` and `add_core`; `index` creates `data={'core_list': core.objects.all()}` but currently does not pass `data` into `render()` — watch for missing context when editing.
- **DB mismatch:** A `db.sqlite3` exists in the repo root but `settings.py` points at MySQL. Check which DB the maintainer expects before applying DB schema changes or migrations.

**Common agent tasks and examples:**
- To add a new API or template route: update `sustainledger/urls.py` (project-level) then the app-level `urls.py` in `Core` or `Emissions` (these exist under each app). Examples of view patterns are in `Core/views.py` and `Emissions/views.py`.
- To inspect models relationships: open `Emissions/models.py` — `Activity.facility` is a `ForeignKey` to `Core.models.core` and `ConvertedEmission.activity` is a `OneToOneField` to `Activity`.

**Environment & secrets:**
- `sustainledger/sustainledger/settings.py` currently contains `SECRET_KEY` and DB credentials in plaintext. Do not commit changes that hardcode new secrets; prefer environment variables or a `.env` approach. If you add env-based code, document it in this file.

**Files to check when changing behavior:**
- `manage.py` — CLI entrypoint
- `sustainledger/sustainledger/settings.py` — env, DB, templates, static
- `Core/models.py`, `Core/views.py`, `Core/urls.py` — facility CRUD
- `Emissions/models.py`, `Emissions/views.py`, `Emissions/urls.py` — emission logic
- `TEMPLATES/` — HTML templates used by views

**Testing & debugging:**
- Run `python manage.py test` to run Django tests (apps have minimal `tests.py`).
- For quick checks, use the shell: `python manage.py shell` and import models from `Core`/`Emissions`.

**What to avoid / pay attention to:**
- Do not rename the `core` model symbol lightly — migrations and imports depend on the current lowercase name.
- Verify DB backend before running migrations. If you switch to sqlite for local dev, update `DATABASES` accordingly.
- Some views may build `data` dictionaries but forget to pass them to `render()`; validate template context when fixing UI bugs.

If anything in this guide is unclear or you want more specific examples (e.g., migrate the project to use environment variables, or add a testing harness), ask and I will update this file.
