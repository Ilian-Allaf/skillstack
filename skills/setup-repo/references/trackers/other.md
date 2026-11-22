# Any other tracker

For Linear, Jira, Azure DevOps, or any tracker the agent can reach: a CLI, an MCP server, or an API.

1. **Ask the user how they work**, in one question: which tool, which project or team, and how the agent reaches it. Recommend the tool's official MCP server or CLI when the harness has it.
2. **Find the real commands.** List the tools or commands the harness actually offers for this tracker, and map each operation of [README.md](README.md#the-operations) to one of them. An operation with no match is written as "not available: <what to do instead>", never invented.
3. **Write `issue-tracker.md` in the project folder**, or in the repo when the user shares it, with one heading per operation, in the order of the README, each with the exact tool or command and its arguments. Use the tracker's own words where they differ: Linear has teams, sub-issues, and "blocked by" relations; Jira has projects, sub-tasks, and issue links.
4. **Prove it** with the read-only operations: read one issue, list open issues by label. Run a write only when the user agrees, on an issue they name.

The user owns this file. When the tracker or the workflow changes, they edit it, or run `setup-repo` again.
