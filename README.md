<img src="assets/icon.svg" width="64" height="64" alt="">

# software-ai-skills-framework

Created in [T3 Code](https://t3.codes).

## Contenu

- [`knowledge/`](knowledge/README.md) : base de connaissance (repos de skills, transcripts vidéo, articles, synthèses) qui sert d'inspiration au futur graphe de skills.
- **Tu ne sais pas quel skill lancer ? Lance `/choose-skill` et décris ta situation.**
- [`skills/`](skills/) : les skills du framework, en anglais. Version 0, écrits mais pas encore prouvés sur un vrai repo : [`constitution`](skills/constitution/README.md) (règles communes, lues par tous ; ce n'est pas un skill), [`choose-skill`](skills/choose-skill/SKILL.md) (le routeur), [`setup-repo`](skills/setup-repo/SKILL.md) (à lancer en premier dans un repo), [`create-app-driver`](skills/create-app-driver/SKILL.md), [`add-guardrail`](skills/add-guardrail/SKILL.md), [`shape-spec`](skills/shape-spec/SKILL.md), [`investigate`](skills/investigate/SKILL.md), [`learn-from-mistakes`](skills/learn-from-mistakes/SKILL.md), [`ship`](skills/ship/SKILL.md), [`analyze-impact`](skills/analyze-impact/SKILL.md), [`verify-pr`](skills/verify-pr/SKILL.md), [`babysit-pr`](skills/babysit-pr/SKILL.md).
- [`tools/`](tools/) : les vérifications du framework.
  - [`lint_skills.py`](tools/lint_skills.py) vérifie chaque skill : frontmatter, étapes et critères de fin, liens, arêtes du graphe, vocabulaire.
  - [`check_refs.py`](tools/check_refs.py) vérifie que chaque référence existe : liens et ancres, chemins entre backticks, noms de skills, de principes et de playbooks, anciens noms retirés.
  - **Une seule commande lance tout, tests compris : `python -I tools/check.py`.** La CI lance la même.
- [`design/`](design/) : conception de notre framework. D'abord le [brainstorm 01](design/01-brainstorm-pr-sereines.md), puis l'[architecture 02](design/02-architecture.md) (v3, centrée sur la vérification), et sa [revue face aux principes](design/03-revue-principes.md). Objectif : livrer beaucoup de PR, sereinement.
