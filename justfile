set shell := ["bash", "-cu"]

# List recipes
default:
    @just --list

# Fetch the live OpenAPI spec and overwrite the committed snapshot.
sync-spec:
    @echo "Fetching OpenAPI spec from https://api.sonz.ai/docs/openapi.json ..."
    @curl -sfL https://api.sonz.ai/docs/openapi.json -o openapi.json
    @echo "✓ Spec updated. Review diff:"
    @git diff --stat openapi.json || true

# Point git at .githooks/ for this repo. Run once per clone.
install-hooks:
    git config core.hooksPath .githooks
    @echo "✓ Hooks enabled: .githooks/pre-push will run on git push."

# Regenerate src/sonzai/_generated/models.py from the committed OpenAPI spec.
#
# Outputs a single pydantic v2 models file — no API clients, no per-class
# modules. The hand-written resources/* layer consumes these models by
# subclassing them in src/sonzai/_customizations/ (see that package for the
# migration pattern).
#
# Requires `datamodel-code-generator` (installed via `uv sync --extra dev`).
regenerate-sdk:
    @echo "Step 1/4: sync OpenAPI spec from production..."
    @just sync-spec
    @echo "Step 2/4: regenerate src/sonzai/_generated/models.py ..."
    @rm -rf src/sonzai/_generated
    @mkdir -p src/sonzai/_generated
    uv run --extra dev datamodel-codegen \
        --input openapi.json \
        --input-file-type openapi \
        --output src/sonzai/_generated/models.py \
        --output-model-type pydantic_v2.BaseModel \
        --target-python-version 3.11 \
        --snake-case-field \
        --use-annotated \
        --use-standard-collections \
        --use-union-operator \
        --use-field-description \
        --allow-population-by-field-name \
        --enum-field-as-literal all \
        --collapse-root-models \
        --use-schema-description \
        --disable-timestamp
    @printf '"""Spec-derived pydantic models. Do not edit by hand.\n\nRegenerate with `just regenerate-sdk`. Hand-written customizations live in\n`src/sonzai/_customizations/`.\n"""\n\nfrom .models import *  # noqa: F401,F403\n' > src/sonzai/_generated/__init__.py
    @echo "Step 3/4: regenerate src/sonzai/_generated/resources/ ..."
    uv run --extra dev python -m scripts.codegen.generate_resources openapi.json src/sonzai/_generated/resources/
    @uv run --extra dev ruff format src/sonzai/_generated/resources/ 2>/dev/null || true
    @echo "Step 4/4: refreshing parity audit..."
    @uv run --extra dev python scripts/parity_audit.py
    @echo "✓ SDK regenerated."

# Bump patch (x.y.Z+1) from pyproject.toml and deploy.
patch:
    just deploy $(just _next patch)

# Bump minor (x.Y+1.0) from pyproject.toml and deploy.
minor:
    just deploy $(just _next minor)

# Bump major (X+1.0.0) from pyproject.toml and deploy.
major:
    just deploy $(just _next major)

# Full release: bump versions, test, build, commit, publish to PyPI, tag, gh release.
# Requires: uv (build), twine (publish — reads ~/.pypirc), gh (authenticated).
# Usage: just deploy 1.2.3
deploy VERSION:
    @just _preflight {{VERSION}}
    @just _test
    @just _bump {{VERSION}}
    @just _build
    @just _commit {{VERSION}}
    git push origin main
    @just _publish {{VERSION}}
    @just _tag {{VERSION}}
    @just _release {{VERSION}}
    @echo "✓ Released v{{VERSION}}"

_preflight VERSION:
    @just _validate-version {{VERSION}}
    @just _check-clean
    @just _check-main
    @just _check-tag-free {{VERSION}}

_validate-version VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! [[ "{{VERSION}}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo "error: VERSION must match X.Y.Z (got: {{VERSION}})" >&2
      exit 1
    fi

_check-clean:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "$(git status --porcelain)" ]]; then
      echo "error: working tree is dirty; commit or stash first" >&2
      git status --short
      exit 1
    fi

_check-main:
    #!/usr/bin/env bash
    set -euo pipefail
    branch="$(git rev-parse --abbrev-ref HEAD)"
    if [[ "$branch" != "main" ]]; then
      echo "error: must be on main (current: $branch)" >&2
      exit 1
    fi

_check-tag-free VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    if git rev-parse --verify --quiet "v{{VERSION}}" >/dev/null; then
      echo "error: local tag v{{VERSION}} already exists" >&2
      exit 1
    fi
    git fetch origin --tags --quiet
    if git ls-remote --tags origin "refs/tags/v{{VERSION}}" | grep -q .; then
      echo "error: remote tag v{{VERSION}} already exists on origin" >&2
      exit 1
    fi

_test:
    uv run --extra dev pytest

_bump VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    perl -pi -e 's/^version = "[^"]+"/version = "{{VERSION}}"/' pyproject.toml
    perl -pi -e 's/^__version__ = "[^"]+"/__version__ = "{{VERSION}}"/' src/sonzai/__init__.py
    perl -pi -e 's{"User-Agent": "sonzai-python/[0-9]+\.[0-9]+\.[0-9]+"}{"User-Agent": "sonzai-python/{{VERSION}}"}g' src/sonzai/_http.py
    uv lock --quiet
    echo "bumped to {{VERSION}}"

_build:
    rm -rf dist
    uv build

_commit VERSION:
    git add pyproject.toml uv.lock src/sonzai/__init__.py src/sonzai/_http.py
    git commit -m "release: v{{VERSION}}"

_publish VERSION:
    twine upload --non-interactive dist/sonzai-{{VERSION}}*

_tag VERSION:
    git tag -a v{{VERSION}} -m "Release v{{VERSION}}"
    git push origin v{{VERSION}}

_release VERSION:
    gh release create v{{VERSION}} --title "v{{VERSION}}" --generate-notes

# Print current version from pyproject.toml.
_current:
    #!/usr/bin/env bash
    set -euo pipefail
    grep -E '^version = ' pyproject.toml | head -1 | sed -E 's/^version = "([^"]+)"/\1/'

# Compute next version from current by bumping patch|minor|major.
_next LEVEL:
    #!/usr/bin/env bash
    set -euo pipefail
    current=$(just _current)
    IFS=. read -r MAJ MIN PAT <<< "$current"
    case "{{LEVEL}}" in
      patch) PAT=$((PAT+1)) ;;
      minor) MIN=$((MIN+1)); PAT=0 ;;
      major) MAJ=$((MAJ+1)); MIN=0; PAT=0 ;;
      *) echo "error: LEVEL must be patch|minor|major (got {{LEVEL}})" >&2; exit 1 ;;
    esac
    echo "${MAJ}.${MIN}.${PAT}"
