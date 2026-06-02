# Add User Rate-Limiting to the API Gateway

## Problem Description

Your team has a REST API gateway that is starting to see abuse from a small number of high-volume callers. The product manager has raised a ticket asking you to add per-user rate limiting so that individual API keys cannot exceed 100 requests per minute. The existing codebase already has a test suite, so the engineering culture expects all new code to be accompanied by passing tests.

Your job is to implement the rate-limiting feature and get it merged via the standard pull-request process. You do not need to actually run the scripts — instead, produce a `workflow_plan.md` file that documents the exact sequence of commands you would run (in order), with brief reasoning for each step, so a team-mate could follow it precisely.

## Output Specification

Produce a single file called `workflow_plan.md` in the working directory.

The file must contain, in order:
- A numbered list of every command you would run (use real command syntax)
- A one-sentence explanation of why you run each command at that point in the workflow
- Any decision points where the outcome of a command changes what you do next
