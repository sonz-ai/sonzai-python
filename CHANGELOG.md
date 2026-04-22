# Changelog

All notable changes to `sonzai` are documented here. The project follows
[Semantic Versioning](https://semver.org/). Dates are `YYYY-MM-DD`.

## [Unreleased]

This unreleased range bundles the "spec-driven SDK" migration: the entire
public type surface is now generated from the committed OpenAPI spec via
`datamodel-code-generator`, with thin hand-written customization subclasses
only where computed properties, renames, or client-side extensions are
genuinely needed.

### Added

- `src/sonzai/_customizations/` package for hand-written subclasses of
  spec-generated pydantic models. Houses `StoredFact`, `AgentCapabilities`,
  `ChatStreamEvent`, and `EvalRun` — the four classes that need more than
  a plain re-export.
- `.githooks/pre-commit` blocks manual edits to `src/sonzai/_generated/`
  unless `openapi.json` is also staged. The generated tree is a build
  artifact; hand edits would be wiped on the next regen.
- `.githooks/pre-push` now regenerates the SDK against the committed
  `openapi.json` and fails the push if the output diverges from the
  committed `_generated/models.py`. Drift is impossible by construction.
- `ChatChoice` and `ExternalToolCall` are now exported at the top level
  (`from sonzai import ChatChoice, ExternalToolCall`). They previously
  lived only in `sonzai.types`.
- `MemoryNode` now carries its full spec shape: `depth`, `child_count`,
  `content_count`, `content_refs`, `cross_refs`, `importance`,
  `is_deleted`, `is_prunable`, `last_accessed_at`, `memory_type`,
  `access_count`, `recency`, `user_id` — fields the server has always
  sent but the hand-rolled class silently dropped.
- `AtomicFact` surfaces ~20 additional spec fields (e.g., `cluster_id`,
  `character_salience`, `retention_strength`, `emotional_intensity`,
  `temporal_relevance`, `polarity_group_id`, `topic_tags`).
- `StoredFact` now includes `session_id` and `source_id` (previously
  silently dropped due to spec drift — this is the latent bug that
  motivated the whole migration).

### Changed (breaking)

- `MemoryNode` fields renamed:
  - `title` → `name`
  - `summary` → `description`
  - The server has sent `name`/`description` all along; the hand-rolled
    `title`/`summary` fields defaulted to empty strings in practice. Any
    consumer reading them was already getting blanks.
- `AgentCapabilities` Python attributes renamed from camelCase to
  snake_case to match the rest of the SDK:
  - `customTools` → `custom_tools`
  - `imageGeneration` → `image_generation`
  - `musicGeneration` → `music_generation`
  - `videoGeneration` → `video_generation`
  - `voiceGeneration` → `voice_generation`
  - `memoryMode` → `memory_mode`
  - `knowledgeBase` → `knowledge_base`
  - `knowledgeBaseProjectId` → `knowledge_base_project_id`
  - `knowledgeBaseScopeMode` → `knowledge_base_scope_mode`
  - `webSearch` → `web_search`
  - `imageUnlockedAt` → `image_unlocked_at`
  - Dict-style construction is unaffected: `populate_by_name=True` means
    `AgentCapabilities.model_validate({"customTools": True})` still works.
    Only direct attribute access (`caps.customTools`) changed.
- `Big5` is now a mapping of dimension → `float`, not dimension →
  `Big5Trait`. The spec emits raw scores per dimension; per-facet detail
  moved to the optional `Big5Trait.facets` nested type.
- `PersonalityDelta` gained its real shape (Bayesian trait update
  record) — `trait_category`, `trait_name`, `delta`, `trigger_type`,
  `timestamp`, plus optional `prior_precision`/`posterior_precision`/
  `proposed_delta`/`applied_delta`/etc. The legacy `delta_id`, `change`,
  and `reason` fields never existed server-side.
- `PersonalityProfile` now uses the spec's nested types:
  - `big5: Big5Assessment` (was `Big5`)
  - `behaviors: BehavioralTraits` (was `PersonalityBehaviors`)
  - `preferences: InteractionPreferences` (was `PersonalityPreferences`)
- `KBSearchResult.type` (was `node_type`), adds required `version: int`.
- `KBRecommendationScore` fields renamed: `source_id`/`target_id` →
  `source_node_id`/`target_node_id`, plus new `target_label`,
  `target_type`, `reasoning`, `computed_at`.
- `KBTrendAggregation` / `KBTrendRanking` / `KBConversionStats` gained
  their full spec shapes (several new required fields per class).
- `UserPersona` is now the API-spec persona resource (`name`,
  `description`, `style`, required). The previous shape was a simulation
  artifact; the server never returned it.
- `UsersResponse.users` is now `list[UserEntry] | None` with a required
  `total: int` (was `list[dict]` with no total).
- **All migrated models** (i.e., every class this release moved off
  `types.py`) now set `model_config = {"extra": "forbid"}` instead of the
  previous permissive/default behavior. Any unexpected field in a server
  response raises `ValidationError` rather than being silently dropped.
  This is the loud-drift-detection behavior the migration was designed
  for — spec updates MUST ship before the server can emit new fields.
- `ChatStreamEvent.is_finished` now matches any non-empty `finish_reason`
  (not just `"stop"`). Terminal frames with `finish_reason` of `"length"`,
  `"content_filter"`, `"tool_calls"`, or `"function_call"` will now end
  streams correctly; previously readers would spin past them.
- `$schema` fields on response envelopes (e.g., `MemoryResponse`,
  `GoalsResponse`) are exposed in Python as `field_schema` with an
  `alias="$schema"` — required by pydantic since `$` is not a valid
  Python identifier. Wire-format compatibility is preserved via the alias.

### Removed

- `ChatUsage` no longer lives in `src/sonzai/_customizations/`; restored
  to `src/sonzai/types.py` where client-side aggregation types belong.
  (No effect on public imports.)
- The 454-file `src/sonzai/_generated/` tree emitted by
  `openapi-python-client` (attrs + `UNSET` sentinels) is gone; replaced
  by a single pydantic v2 `src/sonzai/_generated/models.py`.
- `openapi-python-client`, `attrs`, and `python-dateutil` dropped from
  dependencies; `datamodel-code-generator` added as a dev dep for
  regeneration.

### Migration guide

For most users, no code changes are needed — server responses deserialize
through `model_validate` exactly as before, and wire-format keys
(camelCase) still work. The breaking changes above bite only callers who:

1. Access renamed Python attributes directly
   (`caps.customTools`, `node.title`, `node.summary`).
   **Fix**: rename to snake_case equivalents.
2. Construct models with `Model()` (positional-like kwargs) and relied
   on now-required fields having defaults.
   **Fix**: provide the newly required fields, or use
   `Model.model_validate(dict)` with only the keys you have (pydantic
   will raise `ValidationError` listing what's missing).
3. Expected unknown fields on server responses to be silently dropped.
   **Fix**: regenerate the SDK (`just regenerate-sdk`) before the server
   ships new optional fields. The pre-push hook enforces this.
