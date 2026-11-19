# Index des skills — tstack

- **Repo** : [https://github.com/t3dotgg/tstack](https://github.com/t3dotgg/tstack)
- **Auteur** : Theo Browne (t3dotgg)
- **Révision** : `11e37a74d0a6868c121cd0910ab2b3bd9873b92a` (2026-11-11)
- **Importé le** : 2026-11-16
- **Licence** : MIT
- **Skills** : 9
- **Invocation** : 9 modèle, 0 utilisateur
- **Avec scripts** : 1 · **avec références** : 0 · **avec playbooks** : 0

> Catalogue complet : [`catalog.json`](catalog.json). Les descriptions sont celles du frontmatter, tronquées ici.

## skills (9)

| Skill | Invocation | Description | Mots | Support |
|---|---|---|---:|---|
| [`babysit-pr`](repo/skills/babysit-pr/SKILL.md) | model | Monitor a pull request through review and CI. Use when the user asks to monitor, watch, or babysit a PR. | 865 | scripts |
| [`council`](repo/skills/council/SKILL.md) | model | Trigger this if the user says 'council'. | 429 | — |
| [`file-pr`](repo/skills/file-pr/SKILL.md) | model | File a concise pull request. Use when the user asks to file, open, or create a PR. | 325 | — |
| [`full-send`](repo/skills/full-send/SKILL.md) | model | Trigger this if the user says 'full send'. | 916 | — |
| [`full-stop`](repo/skills/full-stop/SKILL.md) | model | Trigger this if the user says 'full stop', even as a closing "Full stop." that reads like emphasis. | 327 | — |
| [`leaving-pr-comments`](repo/skills/leaving-pr-comments/SKILL.md) | model | Use whenever leaving comments on GitHub. | 241 | — |
| [`modernize`](repo/skills/modernize/SKILL.md) | model | For getting old prs up to date. Use when asked to rebase a pr or "modernize". | 697 | — |
| [`sol-loop`](repo/skills/sol-loop/SKILL.md) | model | Use when the user says "sol loop". | 855 | — |
| [`takeover`](repo/skills/takeover/SKILL.md) | model | Take over existing work. Use when the user asks to take over a PR, branch, or agent thread, or requests a takeover. | 284 | — |

## Références explicites entre skills

| Depuis | Vers | Mentions |
|---|---|---:|
| `full-stop` | `full-send` | 3 |
| `full-send` | `babysit-pr` | 2 |
| `babysit-pr` | `leaving-pr-comments` | 1 |
| `file-pr` | `babysit-pr` | 1 |
| `file-pr` | `leaving-pr-comments` | 1 |
| `full-send` | `file-pr` | 1 |
| `full-send` | `sol-loop` | 1 |
| `modernize` | `leaving-pr-comments` | 1 |
| `takeover` | `babysit-pr` | 1 |
| `takeover` | `file-pr` | 1 |
| `takeover` | `leaving-pr-comments` | 1 |
| `takeover` | `modernize` | 1 |

12 arêtes explicites au total. Elles surestiment les dépendances réelles : un skill peut citer un autre skill sans en dépendre.
