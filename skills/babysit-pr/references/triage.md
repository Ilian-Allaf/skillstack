# Triage

How to sort a review comment, from a bot or a person. Check each finding against the source before acting: bots are often right and sometimes wrong, and a confident tone proves nothing.

| Group | When | What you do |
|---|---|---|
| fix | a real bug in the task's scope | fix it at its cause, then reprove it in step 5 |
| decline | the finding is wrong, or the change would not help | reply with a written reason, then resolve the thread |
| ask | a product choice the user owns | put it in the summary for the user; leave the thread open |
| follow-up | real, but outside the task | open an issue, link it in the thread, resolve |

The verifier's verdict comment is not a review thread: its notes stay notes, and become issues only when the user asks (rule 4 of the constitution).

Unneeded tests, guards for cases that do not matter, and extra compatibility are follow-ups, not fixes. Between two fixes, take the one that deletes or narrows code: review loops grow a PR one cheap-looking fix at a time.
