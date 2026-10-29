# Figure wishlist: Building LLM Agents

This is the source of truth for the course's 20 figures. Each entry says where the
figure goes, what it should make a learner understand, and gives a ready-to-paste
prompt for an image or diagram model (for example, on claude.ai).

## How to use this

1. Pick a figure below and copy its Prompt into claude.ai (ask for an image, or an
   SVG diagram).
2. Save the result in this folder (`notebooks/figures/`) using the exact filename
   given. A matching placeholder already sits in the notebook, so the image appears
   in the right spot as soon as the file exists.
3. PNG is the safe default. SVG works well for the diagram figures, since it is
   crisp and scalable. If you save `name.svg` instead of `name.png`, change that one
   extension in the notebook's placeholder cell.

## On style (read once)

The prompts describe what to show, not how it should look. Colour, fonts, layout,
and overall aesthetic are the model's to decide. The one shared request is
cohesion: these 20 figures belong to one course, so each prompt asks the model to
keep the set visually consistent. If you generate them in one session, you can
paste this once up front:

> I am creating 20 figures for a 10-part "Building LLM Agents" course. For each, I
> describe only what to show; you choose all visual styling (colour, type, layout),
> but keep the whole set visually coherent, like figures from the same book.

`(hero)` marks the single most important figure for that notebook. Every figure
below is present in `notebooks/figures/` and wired into its notebook.

---

## Notebook 01: Your first LLM call

### 1. `01-stateless-memory.svg` (hero)
- Location: section 5, "Multi-turn conversations (and why the model has no memory)"
- Type: before and after, conceptual
- Wish: The model has no memory of its own; a conversation is the growing message
  list you resend on every call.
- Prompt:
  > Create a clear, beautiful explanatory figure showing that a language model has
  > NO memory of its own, and that a multi-turn "conversation" is an illusion the
  > programmer maintains by resending the entire message history on every call.
  > Contrast two turns: Turn 1 sends [system, user-question-1] and gets an answer;
  > Turn 2 sends [system, user-question-1, assistant-answer-1, user-question-2], the
  > whole history plus the new question, because the model only ever sees what is in
  > the current request. Make the growing list of messages the visual centre, and
  > make it obvious the model itself holds no state between calls. This is one figure
  > in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually
  > coherent with the set. You decide all visual styling.

### 2. `01-chat-anatomy.svg`
- Location: section 2, "Your first completion", after "What came back"
- Type: anatomy and flow
- Wish: The request and response round trip, and the parts of the response object a
  developer actually uses.
- Prompt:
  > Create a clear, beautiful labelled diagram of a single chat-completion request
  > and its response. Show the flow: your code builds a list of messages (roles:
  > system and user), sends them to an API endpoint, and the model returns a
  > structured response object. Label the key parts a developer uses:
  > choices[0].message (role and content), finish_reason (why it stopped: stop,
  > length, or tool_calls), and usage (token counts). Indicate which parts the
  > developer controls (the request: model, messages, temperature) versus what the
  > API returns. This is one figure in a 20-figure set for a 10-part "Building LLM
  > Agents" course. Keep it visually coherent with the set. You decide all visual
  > styling.

---

## Notebook 02: Prompting and structured output

### 3. `02-json-tiers.svg` (hero)
- Location: section 4, "Getting JSON three ways", at "(c) Native JSON mode"
- Type: conceptual ladder
- Wish: Three reliability tiers for getting JSON, fragile to bulletproof, each with
  its failure mode.
- Prompt:
  > Create a clear, beautiful figure showing three tiers of reliability for getting
  > structured JSON out of a language model, as an ascending ladder or staircase from
  > fragile to bulletproof. Tier 1: "just ask for JSON in the prompt", fragile (the
  > model may wrap it in markdown fences or add prose, so parsing breaks). Tier 2: "a
  > strict prompt plus temperature 0", more reliable but still not guaranteed. Tier 3:
  > "native JSON mode (response_format json_object)", the reliable default that
  > guarantees valid JSON. Annotate each tier with its typical failure mode and show
  > trust increasing as you climb. This is one figure in a 20-figure set for a 10-part
  > "Building LLM Agents" course. Keep it visually coherent with the set. You decide
  > all visual styling.

---

## Notebook 03: Tool calling

### 4. `03-round-trip.svg` (hero)
- Location: sections 3 to 5, "Round 1, Round 2, Round 3" (place before section 3)
- Type: sequence diagram
- Wish: The four-message tool round trip; the model only requests, your code executes.
- Prompt:
  > Create a clear, beautiful explanatory sequence diagram of how an LLM "tool call"
  > works as a four-message round trip: (1) the user asks something that needs a tool;
  > (2) the model replies NOT with an answer but with a structured request to call a
  > function. Label this "tool_calls", finish_reason = tool_calls. (3) Our code runs
  > the real function and appends the result back as a "tool" message. (4) The model
  > returns the final natural-language answer grounded in that result, finish_reason =
  > stop. Show the message list growing across the four steps, label the roles (user,
  > assistant, tool, assistant), and make it unmistakable that the model never executes
  > anything: it only requests, and our code decides. This is one figure in a 20-figure
  > set for a 10-part "Building LLM Agents" course. Keep it visually coherent with the
  > set. You decide all visual styling.

### 5. `03-why-tools.svg`
- Location: section 1, "Why the model needs tools"
- Type: before and after
- Wish: Without a tool the model guesses arithmetic wrong; with a tool it is right.
- Prompt:
  > Create a clear, beautiful before-and-after figure motivating why a language model
  > needs tools. LEFT ("without a tool"): the model is asked a precise arithmetic
  > question (for example, 1234 times 5678) and confidently returns a WRONG number,
  > because it is guessing token by token. RIGHT ("with a tool"): the model instead
  > calls a calculator function, the real computation runs, and the correct answer
  > comes back. Make the contrast vivid: a confident wrong guess versus a grounded
  > correct result, to show tools give the model abilities it genuinely lacks. This is
  > one figure in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it
  > visually coherent with the set. You decide all visual styling.

---

## Notebook 04: Your first agent (the loop)

### 6. `04-agent-loop.svg` (hero)
- Location: sections 2 to 3, "The reason, act, observe cycle" (place before section 2)
- Type: cycle or loop diagram
- Wish: The agent loop with its exit condition and a step cap.
- Prompt:
  > Create a clear, beautiful cycle or loop diagram of "the agent loop", the heart of
  > an AI agent. Show a repeating cycle: REASON (the model decides what to do next) ->
  > ACT (it calls a tool) -> OBSERVE (the tool result is added back to the
  > conversation) -> and around again. Show the message list growing with each pass
  > round the loop. Mark the EXIT CONDITION clearly: when the model replies with no
  > tool call, the loop ends and returns the final answer. Also show a safety cap (a
  > maximum number of steps) so the loop cannot run forever. Make it obvious this is
  > the SAME chat model in a while-loop, not a new kind of model. This is one figure in
  > a 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually
  > coherent with the set. You decide all visual styling.

### 7. `04-roundtrip-to-loop.svg`
- Location: section 1, "Recap: the manual round-trip from notebook 03"
- Type: before and after
- Wish: A manual round trip wrapped in a while-loop becomes an agent.
- Prompt:
  > Create a clear, beautiful before-and-after figure showing how a single manual tool
  > round trip becomes an agent. LEFT: hand-written code that calls the model, runs one
  > tool, then calls the model once more, a FIXED number of steps written out by hand.
  > RIGHT: the same logic wrapped in a while-loop that repeats until the model is done,
  > so it handles a task needing two, five, or any number of tool calls without knowing
  > the count in advance. The takeaway: an agent is just the round trip from the
  > previous lesson, put in a loop. This is one figure in a 20-figure set for a 10-part
  > "Building LLM Agents" course. Keep it visually coherent with the set. You decide all
  > visual styling.

---

## Notebook 05: Memory and context

### 8. `05-context-window.svg` (hero)
- Location: section 1, "The context window: a finite budget"
- Type: data chart
- Wish: Tokens climb each turn (history is resent) and eventually hit the ceiling.
- Prompt:
  > Create a clear, beautiful chart illustrating why long conversations overflow a
  > model's context window. Show a line or stacked-bar chart where the x-axis is
  > conversation turns (1, 2, 3, and so on) and the y-axis is tokens in the request.
  > Because the entire history is resent every turn, the token count climbs steadily
  > turn after turn. Draw a horizontal ceiling line labelled "context window limit",
  > and show the rising usage eventually crossing it: the overflow point where memory
  > management becomes necessary. This is one figure in a 20-figure set for a 10-part
  > "Building LLM Agents" course. Keep it visually coherent with the set. You decide all
  > visual styling.

### 9. `05-summarisation-loop.svg`
- Location: section 3, "Summarisation memory (the key technique)"
- Type: cycle or loop diagram
- Wish: Old turns, then an LLM summary, then keep the summary plus recent turns, then
  repeat.
- Prompt:
  > Create a clear, beautiful cycle diagram of "summarisation memory". Show the rule
  > that repeats as a conversation grows: (1) older turns accumulate in a buffer; (2)
  > when it gets long, the LLM compresses those old turns into a short running summary;
  > (3) the next request is built from the summary plus only the few most recent turns
  > kept verbatim; then repeat. Make clear the summary persists and gets updated while
  > old verbatim turns are dropped, so the prompt stays small without losing the gist.
  > This is one figure in a 20-figure set for a 10-part "Building LLM Agents" course.
  > Keep it visually coherent with the set. You decide all visual styling.

---

## Notebook 06: A useful single agent

### 10. `06-error-recovery.svg` (hero)
- Location: section 3, "Error handling: recovering from a failing tool"
- Type: sequence or loop diagram
- Wish: A tool fails, the error is fed back as an observation, and the agent retries
  differently.
- Prompt:
  > Create a clear, beautiful flow diagram showing how an agent recovers from a failing
  > tool instead of crashing. Steps: (1) the agent calls a tool (for example, read a
  > file that does not exist); (2) the tool raises an error; (3) the agent loop CATCHES
  > the error and feeds it back into the conversation as an observation (for example, a
  > tool message "ERROR: file not found"); (4) the agent reads that error and makes a
  > different decision (for example, list the available files, then proceed). The key
  > idea: errors are data the agent can react to, not exceptions that end the run. This
  > is one figure in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it
  > visually coherent with the set. You decide all visual styling.

### 11. `06-guardrails.svg`
- Location: section 4, "Guardrails"
- Type: anatomy or labelled-parts diagram
- Wish: Four stackable safety boundaries around the agent.
- Prompt:
  > Create a clear, beautiful labelled diagram of the guardrails around an agent, shown
  > as independent, stackable safety layers surrounding the model in the centre. The
  > four layers: (1) a step budget or max-steps cap (stops runaway loops); (2) a
  > restricted toolset (the agent only has the tools you give it); (3) argument
  > validation (for example, a sandbox that rejects file paths escaping an allowed
  > folder); (4) human-in-the-loop approval for risky actions. Show them as separate,
  > complementary defences you can stack, not optional extras. This is one figure in a
  > 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually coherent
  > with the set. You decide all visual styling.

---

## Notebook 07: Multi-agent basics

### 12. `07-handoff.svg` (hero)
- Location: section 3, "Pattern 1: sequential handoff (two specialists)"
- Type: sequence or flow diagram
- Wish: One agent's text output becomes another's input, just Python wiring.
- Prompt:
  > Create a clear, beautiful flow diagram of a sequential two-agent handoff. LEFT box:
  > a "Researcher" agent (it has a search tool) that gathers notes. An arrow carrying
  > PLAIN TEXT (labelled "notes") flows to the RIGHT box: a "Writer" agent (no tools)
  > that turns the notes into prose. Emphasise that the two agents are separate
  > (different roles, separate contexts, no shared memory) and that "multi-agent" simply
  > means one agent's text OUTPUT becomes the next agent's INPUT, wired together in
  > ordinary code. This is one figure in a 20-figure set for a 10-part "Building LLM
  > Agents" course. Keep it visually coherent with the set. You decide all visual
  > styling.

### 13. `07-generator-critic.svg`
- Location: section 4, "Pattern 2: the generator and critic pair"
- Type: cycle or loop diagram
- Wish: Draft, then critique, then revise, over a bounded number of rounds, quality
  climbing.
- Prompt:
  > Create a clear, beautiful cycle diagram of a generator and critic pair improving an
  > output. A "Writer" agent produces a draft, a "Critic" agent (different role, high
  > standards) reviews it and returns concrete feedback, and the Writer revises using
  > that feedback, then repeat. Include a round counter (round 1, 2, and so on) and show
  > a hard cap on the number of rounds. Convey that quality climbs each round and that
  > the loop must be bounded, not an endless back-and-forth. This is one figure in a
  > 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually coherent
  > with the set. You decide all visual styling.

---

## Notebook 08: Orchestration patterns

### 14. `08-four-patterns.svg` (hero)
- Location: intro, before section 1 "Sequential pipeline"
- Type: flow comparison (four patterns side by side)
- Wish: The four orchestration shapes at a glance: it is just who runs when.
- Prompt:
  > Create a clear, beautiful comparison figure showing the four core
  > agent-orchestration patterns side by side as simple data-flow diagrams, so a learner
  > sees they are just different shapes of "who runs when". (1) SEQUENTIAL PIPELINE:
  > agents in a chain, each output feeding the next. (2) ROUTER: one classifier directs
  > a request to exactly one of several specialists. (3) ORCHESTRATOR-WORKER: a manager
  > splits a task into subtasks, hands them to workers, then merges the results. (4)
  > PARALLEL FAN-OUT or MAP-REDUCE: several workers run at the same time and their
  > results are aggregated. Label each pattern and keep the four visually parallel for
  > easy comparison. This is one figure in a 20-figure set for a 10-part "Building LLM
  > Agents" course. Keep it visually coherent with the set. You decide all visual
  > styling.

### 15. `08-parallel-speedup.svg`
- Location: section 4, "Parallel fan-out or map-reduce"
- Type: timeline, before and after
- Wish: Sequential versus parallel on a time axis: why threading wins.
- Prompt:
  > Create a clear, beautiful figure contrasting sequential versus parallel execution on
  > a time axis to show why parallelism speeds things up. TOP ("sequential"): several
  > worker tasks (for example, 5) drawn one after another along time, so total time is
  > the sum. BOTTOM ("parallel"): the same workers drawn stacked at the same start,
  > running concurrently, finishing in roughly the time of one, then a short "aggregate
  > results" step. Make the wall-clock saving obvious at a glance. This is one figure in
  > a 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually coherent
  > with the set. You decide all visual styling.

---

## Notebook 09: Advanced orchestration

### 16. `09-reflection-gate.svg` (hero)
- Location: section 2, "Reflection and self-critique"
- Type: cycle plus decision gate
- Wish: Generate, then critique, then a gate (good?), then return or revise; bounded.
- Prompt:
  > Create a clear, beautiful loop diagram of a reflection or self-critique cycle with a
  > quality gate. Flow: a producer GENERATES a draft, a critic CRITIQUES it, then a
  > DECISION GATE asks "good enough?": if YES, return the result; if NO, REVISE and loop
  > back to critique. Show the loop is bounded by a maximum number of rounds (a second
  > exit) so it cannot run forever. Convey that this is a loop with an explicit
  > termination condition: the gate is what makes it safe and useful. This is one figure
  > in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually
  > coherent with the set. You decide all visual styling.

### 17. `09-planner-executor.svg`
- Location: section 1, "Planner to executor"
- Type: flow diagram
- Wish: The planner emits a plan as inspectable data; the executor consumes it step by
  step.
- Prompt:
  > Create a clear, beautiful two-phase diagram of the planner and executor pattern.
  > PHASE 1, PLANNER: a model takes a goal and outputs a PLAN as inspectable data (an
  > ordered list of steps, for example JSON [step1, step2, step3]). PHASE 2, EXECUTOR: it
  > works through the plan one step at a time, running each step (possibly with tools)
  > and carrying each result forward into the next. Emphasise the separation: planning
  > produces a checkable artefact; execution consumes it step by step. This is one figure
  > in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually
  > coherent with the set. You decide all visual styling.

### 18. `09-supervisor.svg`
- Location: section 3, "Supervisor and manager"
- Type: cycle with labelled transitions
- Wish: A supervisor dynamically routes among specialists in a loop, with two exits.
- Prompt:
  > Create a clear, beautiful diagram of a supervisor or manager agent dynamically
  > coordinating specialists. A central SUPERVISOR repeatedly looks at the current state
  > and decides who acts NEXT, choosing among specialists (for example, "researcher",
  > "writer") or "done". Show it as a loop: supervisor, then the chosen specialist runs,
  > then state updates, then back to supervisor, until it decides "done" (with a
  > max-steps hard stop as a safety exit). Convey that this is the agent loop from
  > earlier, but the "tools" it chooses between are other agents. This is one figure in a
  > 20-figure set for a 10-part "Building LLM Agents" course. Keep it visually coherent
  > with the set. You decide all visual styling.

---

## Notebook 10: Capstone

### 19. `10-capstone-arch.svg` (hero)
- Location: "Part A: Build the system" intro
- Type: flow and architecture diagram
- Wish: The full system, annotated with which earlier pattern each piece uses.
- Prompt:
  > Create a clear, beautiful architecture diagram of a complete multi-agent research
  > assistant, showing how the course's pieces fit together. Flow: a PLANNER breaks a
  > question into subtopics, several RESEARCHER agents run IN PARALLEL (each with a
  > search tool) to gather notes, a WRITER synthesises the notes into a report, and a
  > CRITIC reviews it and triggers at most ONE revision. Annotate each part with the
  > pattern it uses (planner-executor, parallel fan-out, reflection). This is the payoff
  > figure: it should make clear why the course built exactly these building blocks. This
  > is one figure in a 20-figure set for a 10-part "Building LLM Agents" course. Keep it
  > visually coherent with the set. You decide all visual styling.

### 20. `10-course-map.svg`
- Location: "Part C: Where to go next"
- Type: flow or map
- Wish: The whole-course arc, 01 to 10, with dependencies.
- Prompt:
  > Create a clear, beautiful "map" of a 10-part "Building LLM Agents" course as a
  > journey, showing how the topics build on each other. Nodes 01 to 10 with short
  > labels: 01 first LLM call, 02 prompting and structured output, 03 tool calling, 04
  > the agent loop, 05 memory, 06 a robust single agent, 07 multi-agent basics, 08
  > orchestration patterns, 09 advanced orchestration, 10 capstone. Show the narrative
  > arc (single call, then reliable output, then tools, then agent, then memory, then
  > robust agent, then multiple agents, then static patterns, then dynamic patterns, then
  > assembled capstone) with arrows for dependencies (for example, 08 and 09 both feed
  > the capstone). This is one figure in a 20-figure set for a 10-part "Building LLM
  > Agents" course. Keep it visually coherent with the set. You decide all visual
  > styling.
