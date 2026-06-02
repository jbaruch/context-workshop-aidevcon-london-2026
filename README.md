# Context Workshop — AI Native DevCon London 2026

**Don't Write Prompts, Write Software** — Baruch Sadogursky & Macey Baker.

A live, build-it-with-the-room session on treating context as software: take a
working but bloated "uber-prompt", decompose it by determinism into **skills**
(conditional behaviour), **scripts** (the deterministic parts, with real tests),
and **rules** (the mandatory checks), then package the whole thing as a
distributable plugin — and apply the same discipline to the context artifacts
themselves, with **evals** as their tests.

The artifacts get built live during the session; this repo is where they land,
so you can follow along or take them home.

**Slides & resources:** https://speaking.jbaru.ch/aidevcon-london-2026-dont-write-prompts

## Prerequisites

To follow along live (or reproduce the build later) you'll need:

- **[Claude Code](https://claude.com/claude-code)** — installed and on a recent
  version.
- **A GitHub account** and the **[`gh` CLI](https://cli.github.com/)** —
  authenticated, for the issue → PR flow we drive from the terminal.

## Repo structure

The artifacts are built live, so the layout fills in as the session
progresses. Where to look:

- **`skills/`** — the conditional behaviour, decomposed from the uber-prompt
  into discrete skills.
- **`scripts/`** — the deterministic parts, pulled out as real code with tests.
- **`rules/`** — the mandatory checks the workflow must enforce.
- **the packaged plugin** — everything above bundled into a single
  distributable you can take home.
