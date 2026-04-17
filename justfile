set shell := ["bash", "-cu"]

# List recipes
default:
    @just --list

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
    echo "bumped to {{VERSION}}"

_build:
    rm -rf dist
    uv build

_commit VERSION:
    git add pyproject.toml src/sonzai/__init__.py src/sonzai/_http.py
    git commit -m "release: v{{VERSION}}"

_publish VERSION:
    twine upload --non-interactive dist/sonzai-{{VERSION}}*

_tag VERSION:
    git tag -a v{{VERSION}} -m "Release v{{VERSION}}"
    git push origin v{{VERSION}}

_release VERSION:
    gh release create v{{VERSION}} --title "v{{VERSION}}" --generate-notes
