# Personality Shift Demo

A Streamlit app that lets you create a Sonzai agent, chat with it, and then
shift its Big5 between sessions via sliders (or one-click presets). No mem0
comparison, no judge — just the core pipeline:

```
adjust sliders → Apply → PUT Big5 → platform re-derives Dimensions
                                  → next session reflects the new personality
```

## What it demonstrates

- **End-to-end agent creation from the SDK.** The sidebar has a **Create
  new** flow that calls `client.agents.generation.generate_and_create(...)`
  with a name + short description — the LLM seeds the agent's Big5, speech
  patterns, interests, etc. Or paste an existing UUID to drive one you
  already have.
- **Between-session personality editing.** Sliders and presets are **locked
  during a session** and unlocked only after you click **End Session**. That
  makes the boundary concrete: "here's session 1 with personality A, here's
  session 2 with personality B." You can run as many sessions as you want,
  each with a different Big5.
- **Developer-friendly mutation.** Send only Big5; the platform re-derives
  Politeness / Compassion / Assertiveness / Volatility / etc. automatically.
  No need to compute DeYoung BFAS loadings client-side.
- **Live derived Dimensions readout.** The right-hand panel shows the
  current Big5 with deltas from the baseline, plus the derived Dimensions
  so you can see exactly what the prompt layer is being told.
- **One-click restore.** When you're done, restore to the baseline Big5
  captured at connect time.

## Run

```bash
cd demos/personality_shift
pip install -r requirements.txt

# Option A — use the local SDK (recommended when hacking on the SDK itself):
pip install -e ../..

# Option B — use PyPI sonzai
pip install sonzai

export SONZAI_API_KEY=sk-...

streamlit run app.py
```

The app opens at http://localhost:8501.

1. **Sidebar → Create new**: pick a name + short description, click **Create
   agent**. The SDK generates the full character and returns its UUID. (Or
   switch to **Use existing** and paste a UUID you already have.)
2. **Baseline captured.** Before session 1, you can tweak the sliders or pick
   a preset to set the starting personality. Click **Start session 1**.
3. **Chat freely.** Personality is locked while the session is live — no
   surprises mid-conversation.
4. **End session** (top of the chat panel). Sliders unlock.
5. Move a slider, click **Apply personality**, then **Start session 2**.
   The new session picks up the new Big5 and the re-derived Dimensions.
6. Repeat as many sessions as you want.
7. **Restore to baseline** when you're done.

## Presets included

| Preset | Signature |
|---|---|
| Agreeable | Warm, cooperative, eager to please. Validates feelings before advice. |
| Blunt | Direct, confrontational, willing to disagree. Short and dismissive. |
| Confident | Assertive, decisive, takes charge. Strong recommendations, no hedging. |
| Anxious | Reactive, worried, second-guesses. Asks for reassurance. |
| Curious | Inquisitive, exploratory, lots of follow-up questions. |
| Reserved | Quiet, thoughtful, minimal words. |
| Volatile | Emotionally reactive, mood shifts fast. |

Or drop into the manual Big5 sliders for fine-grained control.

## Under the hood

`app.py` talks to the platform exclusively through `sonzai-python`:

- `client.agents.generation.generate_and_create(name=, description=, gender=)` — create a new agent in one call.
- `client.agents.personality.get(agent_id)` — snapshot on connect, re-read after every mutation.
- `client.agents.personality.update(agent_id, big5={...})` — write the full Big5 block.
- `client.agents.sessions.end(agent_id, user_id=, session_id=, messages=[...])` — commit a session to the agent's memory before moving on.
- `client.agents.chat(..., stream=True)` — stream turn responses chunk-by-chunk.

The platform auto-re-derives Dimensions on every Big5 PUT — the demo relies on
that, so you can change a single trait and see the downstream effect without
having to send the Dimensions block yourself.

## Caveats

- If you close the browser without clicking **Restore baseline**, the agent
  stays in whatever state the last preset put it in. Use a dedicated demo
  agent, or always click Restore before you leave.
- The demo uses a fresh `user_id` + `session_id` per Streamlit session, so
  the memory/relationship layer won't pollute future runs. If you want
  persistence, swap in a fixed user/session ID in `init_state`.
