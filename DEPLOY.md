# DEPLOY — sonzai-python

## The rule

**Never release manually. Always use `just patch`.**

```bash
just patch              # bump patch, test, build, commit, push, pypi publish, tag, gh release
just deploy 1.4.3       # same, for an explicit version
```

That runs the complete pipeline in order:

1. Preflight (version format, clean tree, on `main`, tag free)
2. `uv run pytest`
3. Bump `pyproject.toml` version + `src/sonzai/__init__.py`'s `__version__`
4. Clean + build (`uv build`)
5. Commit `release: vX.Y.Z`
6. `git push origin main`
7. Publish to PyPI (`uv publish` / `twine upload`)
8. Annotated tag `vX.Y.Z` + push
9. `gh release create vX.Y.Z --generate-notes`

Skip any step and the release is incomplete.

## Don't

- Don't manually edit `pyproject.toml`'s `version = ` and commit. `_bump`
  also updates `src/sonzai/__init__.py`'s `__version__`.
- Don't publish to PyPI without tagging + running `gh release create`.
- Don't `git tag` manually — let `_tag` do it so the tag message matches.
- Don't bump minor/major without explicit user approval (patch is the
  default discipline on this tree).

## Recovering a half-manual release

If someone already bumped + committed + pushed + tagged but skipped PyPI /
gh release (this happened on v1.4.1 and v1.4.2), run the missing steps:

```bash
just _publish 1.4.2
just _release 1.4.2
```

Or — cleaner — skip ahead with `just patch` to `1.4.3` and let the full
pipeline run.

## Spec regeneration

`just regenerate-sdk` is a separate concern from release — it pulls the
latest `openapi.json`, regenerates `src/sonzai/_generated/`, and refreshes
`SDK_PARITY_AUDIT.md`. Run it when the backend ships a spec change. It
does NOT bump the version or publish.

## See also

[`../DEPLOY.md`](../DEPLOY.md) — canonical guide covering all four repos.
