# Two Incoming Tickets — Plan the Right Workflow for Each

## Problem Description

Your team uses a ticket-driven development process, and two new tickets have just arrived in the queue. Your job is to plan the workflow for each ticket and document that plan — you will NOT execute the workflows, just document what you would do and in what order.

**Ticket A — "Fix README example for authentication"**  
The current README has an outdated curl example under the "Authentication" section. The example uses the old API key header format (`X-API-Key`) instead of the current Bearer token format. The ticket asks you to correct the example. No source code needs to change — only the README.

**Ticket B — "Add config loader support for YAML files"**  
The application currently reads its configuration from JSON files only. This ticket asks you to extend the config loader module so it can also read YAML files. It is unclear from the ticket description whether this requires any documentation update, but source code changes are definitely involved.

Produce a file called `ticket_plans.md` that documents, for each ticket separately:
1. Which workflow type you chose (and why, in one sentence)
2. Every command you would run in order, using real script syntax with placeholder values where needed
3. Which reviewer type handles the PR and why
