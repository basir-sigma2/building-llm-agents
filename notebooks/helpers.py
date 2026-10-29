"""
Shared helpers for the "Building LLM Agents" course.

Notebook 01 builds the client by hand so you can see exactly what is going on.
From notebook 02 onward we just do:

    from helpers import client, MODEL

...so the teaching code stays focused on agents instead of connection
boilerplate.

Connection settings are read from the .env file at the repo root:

    OPENAI_API_KEY    your Sigma2 AI Gateway token
    OPENAI_BASE_URL   https://ai-gateway.sigma2.no/v1
    COURSE_MODEL      (optional) override the default model
    COURSE_CLEF_MODEL (optional) override the decision model used by decide()

A note on the model behind the gateway
--------------------------------------
The served model is a *reasoning* model: left to itself it thinks before it
answers, returning the thinking separately as `message.reasoning_content`
and the answer in `message.content`.

The course turns that off, with `reasoning_effort="none"` applied to every
request in `get_client()` below. Two reasons:

1. Thinking is charged against `max_tokens` along with the answer. With it
   on, a tight budget is spent thinking and `content` comes back as an
   empty string with `finish_reason="length"` — no error, just nothing,
   which usually surfaces much later as `json.loads("")`. `ask()` raises a
   clear error if this ever happens anyway.

2. It makes live teaching slow and non-deterministic: the same cell can
   work in rehearsal and fail in the room.

The notebooks also budget 8000 tokens per call. `max_tokens` is a ceiling,
not a reservation — you are billed for what is generated, so a high ceiling
costs nothing and removes truncation as a class of failure. To make an
answer *short*, say so in the prompt; don't squeeze `max_tokens`.

To see the model think, pass `reasoning_effort="medium"` on a single call
and read `message.reasoning_content`.

One more endpoint constraint: it accepts exactly ONE system message per
request. Sending a second fails with "System message must be at the
beginning", even when both are at the beginning. Concatenate instead.

A second model on the same key
------------------------------
The key also reaches Clef, a *decision* model: it does not chat, it scores
questions you define and returns a probability for every option. MODEL never
picks it. Call it by name, or through `decide()` below. Notebook 11 is about it.
"""

from __future__ import annotations

import json
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

# Load .env from the repo root, regardless of which folder Jupyter started in.
load_dotenv(find_dotenv())


# "none" disables the model's thinking phase; "low"/"medium"/"high" enable it.
REASONING_EFFORT = "none"


def get_client() -> OpenAI:
    """Create an OpenAI client pointed at the Sigma2 AI Gateway."""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not api_key or not base_url:
        raise RuntimeError(
            "Missing OPENAI_API_KEY / OPENAI_BASE_URL.\n"
            "On notebook.sigma2.no, your instructor sets the key: ask them, then\n"
            "restart this kernel (Kernel -> Restart Kernel).\n"
            "On your own machine, copy .env.example to .env and paste in your Sigma2 token:\n"
            "    cp .env.example .env"
        )
    client = OpenAI(api_key=api_key, base_url=base_url)

    # Turn off the model's reasoning mode for every request in the course.
    # See the note at the top of this file for why. This wraps `create` rather
    # than hiding anything: the kwarg below is exactly what you would type by
    # hand on each call, and you can override it per call at any time.
    _create = client.chat.completions.create

    def create(*args, **kwargs):
        kwargs.setdefault("reasoning_effort", REASONING_EFFORT)
        return _create(*args, **kwargs)

    client.chat.completions.create = create
    return client


# A ready-to-use client every notebook can import.
client = get_client()


def available_models() -> list:
    """The model id(s) this project has access to on the endpoint.

    Which model(s) appear here depends on what your project has been set up
    with — so we ask the endpoint rather than hard-coding a name.
    """
    return [m.id for m in client.models.list().data if m.id != "arena-model"]


def _default_model() -> str:
    # An explicit choice in .env always wins.
    chosen = os.getenv("COURSE_MODEL")
    if chosen:
        return chosen
    # Skip decision models: Clef cannot chat, and the gateway's order is not
    # guaranteed, so taking models[0] blindly could hand every notebook to it.
    models = [m for m in available_models() if not m.startswith("clef")]
    if not models:
        raise RuntimeError(
            "No chat models available on this endpoint. Check that your project has a "
            "model set up and that your token is valid."
        )
    return models[0]


# The model used throughout the course: your COURSE_MODEL if set, otherwise the
# first chat model your project has access to.
MODEL = _default_model()

# The decision model from notebook 11. It answers questions; it does not chat.
CLEF_MODEL = os.getenv("COURSE_CLEF_MODEL", "clef-flash-not-for-production")


# ----------------------------------------------------------------------
# Convenience wrappers
# ----------------------------------------------------------------------

def ask(prompt: str, system: str | None = None, model: str | None = None, **kwargs) -> str:
    """One-shot helper: send a single prompt, get back the text answer.

    Handy in the orchestration notebooks where we fire off many small
    LLM calls. For anything where the *mechanics* matter, call
    client.chat.completions.create(...) directly so you can see the parts.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model or MODEL, messages=messages, **kwargs
    )
    choice = resp.choices[0]
    # A reasoning model can spend its whole budget thinking and return an empty
    # answer. That is not an error to the API, so it would otherwise surface far
    # away from the cause -- usually as json.loads("") blowing up. Fail here, and
    # say what to do about it.
    if not (choice.message.content or "").strip() and choice.finish_reason == "length":
        budget = kwargs.get("max_tokens", "the configured")
        raise RuntimeError(
            f"The model used its entire {budget}-token budget on reasoning and "
            f"returned no answer (finish_reason='length'). Raise max_tokens."
        )
    return choice.message.content


def decide(state, questions: dict, model: str | None = None) -> dict:
    """Ask Clef, the decision model, about `state`; return its "answers" dict.

    `state` is the situation, as text or any JSON value. `questions` maps a
    name of your choosing to a noul, choice or score question. Notebook 11
    builds this function by hand and explains every part of it.
    """
    request = {"state": state, "questions": questions}
    reply = client.chat.completions.create(
        model=model or CLEF_MODEL,
        messages=[{"role": "user", "content": json.dumps(request)}],
    )
    return json.loads(reply.choices[0].message.content)["answers"]


# ----------------------------------------------------------------------
# Display helpers — keep teaching cells free of print() clutter
# ----------------------------------------------------------------------

def jprint(obj) -> None:
    """Pretty-print a dict / JSON-serializable object."""
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def _as_dict(message) -> dict:
    """Accept either a plain dict or an OpenAI SDK message object."""
    if isinstance(message, dict):
        return message
    return message.model_dump() if hasattr(message, "model_dump") else dict(message)


def show_messages(messages) -> None:
    """Render a conversation in a readable, role-labeled way.

    Understands assistant tool calls and tool-result messages, which makes
    it the go-to tool for debugging the agent loop in later notebooks.
    """
    icons = {"system": "⚙️  SYSTEM", "user": "👤 USER",
             "assistant": "🤖 ASSISTANT", "tool": "🔧 TOOL"}
    for m in messages:
        m = _as_dict(m)
        role = m.get("role", "?")
        print(f"\n{icons.get(role, role.upper())}")
        content = m.get("content")
        if content:
            print(content)
        for call in (m.get("tool_calls") or []):
            fn = call["function"] if isinstance(call, dict) else call.function
            name = fn["name"] if isinstance(fn, dict) else fn.name
            args = fn["arguments"] if isinstance(fn, dict) else fn.arguments
            print(f"  ↳ calls {name}({args})")
        if m.get("role") == "tool":
            print(f"  (result for call {m.get('tool_call_id', '?')})")


# ----------------------------------------------------------------------
# A minimal, reusable Agent (built from scratch in notebook 04)
#
# Notebooks 06-10 do `from helpers import Agent, Tool` instead of redefining
# the loop each time. This is *exactly* the class you build by hand in
# notebook 04 — nothing magic is hidden here.
# ----------------------------------------------------------------------

class Tool:
    """Wraps a plain Python function so an LLM can call it.

    The `parameters` dict is a JSON Schema describing the arguments — the
    same schema you write by hand in notebook 03.
    """

    def __init__(self, fn, description=None, parameters=None, name=None):
        self.fn = fn
        self.name = name or fn.__name__
        self.description = description or (fn.__doc__ or "").strip().split("\n")[0]
        self.parameters = parameters or {"type": "object", "properties": {}}

    @property
    def schema(self) -> dict:
        """The tool definition in the shape the API expects."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __call__(self, **kwargs):
        return self.fn(**kwargs)


class Agent:
    """An LLM in a loop: call the model, run any tools it asks for, repeat.

    This is the heart of the whole course. An "agent" is just:
        model + a role (system prompt) + tools + a loop that runs until done.
    """

    def __init__(self, name="agent", system="", tools=None, model=None,
                 max_steps=8, temperature=0, client=None):
        self.name = name
        self.system = system
        self.tools = {t.name: t for t in (tools or [])}
        self.model = model or MODEL
        self.max_steps = max_steps
        self.temperature = temperature
        self.client = client or globals()["client"]

    def run(self, task, verbose=False):
        """Run the agent on a task string and return its final text answer."""
        messages = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": task})
        return self.run_messages(messages, verbose=verbose)

    def run_messages(self, messages, verbose=False):
        """Run the loop over an existing message list (lets you keep history)."""
        tool_schemas = [t.schema for t in self.tools.values()] or None
        for step in range(1, self.max_steps + 1):
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_schemas,
                temperature=self.temperature,
            )
            msg = resp.choices[0].message
            # Record what the assistant said (verified append format).
            # Drop the provider's thinking fields: they are not part of the
            # chat protocol, they bloat every subsequent prompt, and some
            # gateways reject them on the way back in.
            record = msg.model_dump(exclude_none=True)
            for field in ("reasoning_content", "provider_specific_fields"):
                record.pop(field, None)
            messages.append(record)

            if not msg.tool_calls:
                return msg.content  # no tools requested -> we're done

            for call in msg.tool_calls:
                name = call.function.name
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                if name in self.tools:
                    try:
                        result = self.tools[name](**args)
                    except Exception as e:  # feed errors back so the model can recover
                        result = f"ERROR running {name}: {e}"
                else:
                    result = f"ERROR: no tool named {name!r}"
                if verbose:
                    print(f"  [{self.name}] step {step}: {name}({args}) -> {result}")
                messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": str(result)}
                )

        return "[stopped: reached max_steps without a final answer]"
