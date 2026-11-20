# Anatomie d'un skill

**But de ce document** : définir ce qu'est un skill de qualité, indépendamment du contenu métier. C'est la grammaire commune que tous nos futurs skills devront respecter.

Sources principales : `writing-for-agents` (Matt Pocock), `authoring-a-skill` (pstack), `SKILL-MECHANICS.md` (Matt Pocock), et l'observation des 109 skills du corpus.

---

## 1. Définition

Un skill est un **document exécutable par un agent**, chargé à la demande, qui encode :

- **quand** il s'applique (déclencheur) ;
- **quoi** faire (étapes ou référence) ;
- **comment savoir que c'est fini** (critère de complétion) ;
- **où** trouver les ressources nécessaires (pointeurs).

Ce n'est ni une documentation utilisateur, ni un prompt one-shot, ni un script. C'est un **contrat de comportement** : si le skill est chargé, l'agent doit agir différemment.

---

## 2. Les trois couches d'un skill

```text
┌─────────────────────────────────────────────┐
│ 1. Pointeur (frontmatter.description)       │  ← chargé en permanence si model-invoked
├─────────────────────────────────────────────┤
│ 2. Corps (SKILL.md)                         │  ← chargé quand le skill fire
│    - étapes / référence                     │
│    - critères de complétion                 │
│    - pointeurs vers les ressources          │
├─────────────────────────────────────────────┤
│ 3. Ressources divulguées                    │  ← chargées seulement si nécessaires
│    references/ · playbooks/ · scripts/      │
│    assets/ · templates/                     │
└─────────────────────────────────────────────┘
```

La qualité d'un skill se joue sur les trois couches :

- un mauvais pointeur → le skill ne fire jamais, ou fire au mauvais moment ;
- un mauvais corps → l'agent exécute mal ou s'arrête trop tôt ;
- de mauvaises ressources → l'agent invente ou duplique.

---

## 3. Le frontmatter

### 3.1 Champs observés

| Champ | Obligatoire | Rôle |
|---|---:|---|
| `name` | Oui | Identifiant stable, kebab-case |
| `description` | Oui | Pointeur de déclenchement (model-invoked) ou résumé (user-invoked) |
| `disable-model-invocation` | Non | `true` → skill user-invoked, zéro charge de contexte |
| `argument-hint` | Non | Aide à l'invocation avec argument |
| `icon`, `color` | Non | Présentation (pstack) |
| `paths` | Non | Portée par chemin (rare) |
| `metadata` | Non | Métadonnées libres |

Le corpus reste minimal : 109/109 ont `name` et `description`, 84/109 ont `disable-model-invocation`.

### 3.2 Model-invoked vs user-invoked

| | Model-invoked | User-invoked |
|---|---|---|
| Description | Chargée à chaque tour | Chargée seulement pour l'humain |
| Déclenchement | Agent ou autre skill | Humain uniquement |
| Coût | Contexte permanent | Charge cognitive |
| Usage | Skill qui doit fire seul | Mode, routeur, procédure rare |

**Règle** : payer le contexte seulement quand le déclenchement autonome vaut son prix. Un skill qui ne fire que par l'humain doit être user-invoked.

### 3.3 La description comme pointeur

Une description n'est pas un résumé marketing. C'est un **pointeur qui encode les branches de déclenchement**.

**Faible** :

```yaml
description: A helpful skill for code review.
```

**Fort** (tiré de `code-review`) :

```yaml
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
```

La description forte :

- nomme l'objet (changes since a fixed point) ;
- nomme les branches (Standards / Spec) ;
- nomme les déclencheurs utilisateur (review a branch, a PR, work-in-progress, "review since X") ;
- évite l'identité et le jargon interne.

**Test** : si deux skills différents pourraient matcher la même description, elle est trop vague.

### 3.4 Le cas du routeur

Un routeur est un skill user-invoked qui **nomme les autres skills et quand les utiliser**. Il ne peut pas les déclencher (ils sont user-invoked), il peut seulement guider l'humain.

Exemples : `ask-matt` (Matt), `poteto-help` (pstack).

Un routeur peut être long (1 900–2 400 mots) parce qu'il est le seul skill que l'humain doit mémoriser. C'est un investissement de **charge cognitive**, pas de contexte.

---

## 4. Le corps

### 4.1 Étapes vs référence

Un skill contient deux types de contenu :

- **étapes** : actions ordonnées que l'agent exécute ;
- **référence** : définitions, règles, faits consultés à la demande.

Les deux peuvent coexister. La question est **où** placer chaque élément dans la hiérarchie :

1. **étape dans le fichier** — ce que l'agent fait, dans l'ordre ;
2. **référence dans le fichier** — consultée au besoin ;
3. **référence divulguée** — dans un fichier séparé, atteinte par un pointeur.

**Règle** : inline ce dont **toutes les branches** ont besoin ; divulgue ce dont **seulement certaines branches** ont besoin.

### 4.2 Critères de complétion

Chaque étape doit se terminer sur une **condition vérifiable**. Deux propriétés :

- **clarté** : l'agent peut distinguer « fini » de « pas fini » ;
- **exigence** : la condition force le travail nécessaire.

**Faible** : « comprends le problème »  
**Fort** : « chaque modèle modifié est accounted for »  
**Fort** : « la commande de repro passe au vert, sortie collée »

Un critère vague invite la **complétion prématurée** : l'agent s'arrête avant d'avoir fini parce que l'étape suivante l'attire. La défense est de rendre le critère plus précis, pas d'ajouter des mots.

### 4.3 Leading words

Un **leading word** est un token pré-entraîné qui ancre un comportement :

- _tracer bullet_ : une tranche verticale complète ;
- _fog of war_ : l'incertitude qu'on réduit par des décisions ;
- _red_ : un test qui échoue, un état binaire observable ;
- _frontier_ : l'ensemble des tickets prêts.

Au lieu d'écrire « fais une tranche verticale complète qui traverse toutes les couches », on écrit « tracer bullet ». Le modèle recrute ses priors et le comportement est plus stable.

**Règle** : préférer un mot existant et bien connu à un néologisme. Un mot inventé coûte sa définition en tokens et ne recrute aucun prior.

### 4.4 Formulation positive

La négation est un piège : « ne pense pas à un éléphant » active l'éléphant. Une interdiction drague le comportement interdit dans le contexte.

**Faible** : « n'utilise pas de commentaires »  
**Fort** : « écris le pourquoi non évident que le code ne peut pas montrer »

Une interdiction n'est légitime que comme **garde-fou dur** impossible à formuler positivement. Dans ce cas, pair-la avec la cible positive.

### 4.5 Single source of truth

Chaque règle doit vivre à **un seul endroit**. La duplication :

- coûte de la maintenance ;
- gonfle l'importance d'une règle au-delà de son rang ;
- crée des contradictions quand une copie est mise à jour et pas l'autre.

**Règle** : si deux skills ont besoin de la même référence, elle vit dans un fichier externe que les deux pointent, ou dans un skill de référence model-invoked.

### 4.6 Pas de no-ops

Une instruction que le modèle suit déjà par défaut est un **no-op** : elle coûte du contexte pour ne rien changer.

**Test** : « est-ce que cette phrase change le comportement par rapport au défaut ? » C'est un test **relatif au modèle**, pas au lecteur. Deux personnes qui ne sont pas d'accord sur le défaut doivent trancher en exécutant le skill, pas en débattant.

Quand une phrase échoue, supprimer la phrase entière, pas la raccourcir.

---

## 5. La divulgation progressive

### 5.1 La hiérarchie

```text
SKILL.md
├── Étape 1
├── Étape 2  ── pointeur ──→ references/architecture.md
├── Étape 3  ── pointeur ──→ playbooks/bug-fix.md
└── Étape 4  ── pointeur ──→ scripts/verify.sh
```

Le corps reste lisible ; les détails vivent derrière des pointeurs.

### 5.2 Les dossiers de support observés

| Dossier | Usage | Exemple |
|---|---|---|
| `references/` | Référence consultée à la demande | `poteto-mode/references/bugbot-triage.md` |
| `playbooks/` | Procédures situationnelles | 23 playbooks de `poteto-mode` |
| `scripts/` | Outils exécutables | scripts de vérification, de benchmark |
| `assets/` | Images, diagrammes | documentation |
| `templates/` | Squelettes de sortie | PR, ticket |

**Règle** : un dossier de support n'existe que s'il est pointé par le corps. Un dossier orphelin est du sédiment.

### 5.3 La taille

Statistiques du corpus :

| Repo | Skills | Médiane (mots) | Moyenne | Max |
|---|---:|---:|---:|---:|
| Matt Pocock | 39 | 549 | 682 | 2 034 (`wayfinder`) |
| pstack | 61 | 383 | 630 | 3 450 (`poteto-mode`) |
| tstack | 9 | 429 | 549 | 916 (`full-send`) |

**Lecture** : un skill normal fait **400–700 mots**. Les exceptions sont :

- des routeurs (`ask-matt`, `poteto-mode`, `poteto-help`) ;
- des skills de référence dense (`writing-for-agents`, `statechart`) ;
- des procédures complexes (`full-send`, `babysit-pr`).

Un skill de plus de 1 000 mots doit justifier sa taille : est-ce un routeur, une référence, ou une procédure qui ne peut pas être divulguée ?

---

## 6. Template de skill (à adapter, pas à copier)

```markdown
---
name: <kebab-case>
description: "<objet>. <branches>. Use when <déclencheurs>."
# disable-model-invocation: true  # si user-invoked
---

# <Titre>

<Une phrase : quel problème ce skill résout, pour qui.>

## Quand l'utiliser

- <branche 1>
- <branche 2>
- <contre-indication explicite>

## Étapes

1. **<Verbe> <objet>.**
   - Faire X.
   - Critère de fin : <condition vérifiable>.
2. **<Verbe> <objet>.**
   - Faire Y.
   - Critère de fin : <condition vérifiable>.

## Preuve

<Ce qui doit être observé pour déclarer le travail terminé.>

## Ressources

- [`references/<fichier>.md`](references/<fichier>.md) — <quand la lire>.
- [`scripts/<script>`](scripts/<script>) — <ce qu'il fait>.

## Échec et escalade

- Si <condition>, alors <action>.
- Si <condition irréversible>, demander <approbation>.
```

**Note** : ce template n'est pas un skill. C'est un contrat de structure. Le contenu doit être adapté à chaque skill ; les sections vides doivent être supprimées.

---

## 7. Checklist de validation

### Structure

- [ ] `name` et `description` présents.
- [ ] Le nom est en kebab-case et unique.
- [ ] La description nomme l'objet, les branches et les déclencheurs.
- [ ] Le mode d'invocation est explicite (`disable-model-invocation` si user-invoked).
- [ ] Chaque pointeur du corps pointe vers un fichier existant.
- [ ] Aucun dossier de support orphelin.

### Contenu

- [ ] Le skill change le comportement par rapport au défaut.
- [ ] Chaque étape a un critère de complétion vérifiable.
- [ ] Les règles sont formulées positivement quand c'est possible.
- [ ] Chaque règle a une source de vérité unique.
- [ ] Les leading words sont utilisés à bon escient.
- [ ] Aucun no-op évident.
- [ ] La prose est vérifiable ou clairement marquée comme du jugement.

### Robustesse

- [ ] Le skill peut être interrompu et repris (si le travail est long).
- [ ] Les actions irréversibles sont identifiées.
- [ ] Les gates humaines sont explicites.
- [ ] Le skill déclare ce qu'il fait en cas d'échec.
- [ ] Le skill peut être supprimé quand le modèle acquiert la capacité.

### Test

- [ ] Un cas nominal passe.
- [ ] Un cas d'échecKnown est géré.
- [ ] Un eval aveugle compare le skill à une variante ou à l'absence de skill.
- [ ] Les transcripts montrent que l'agent a réellement lu les fichiers pointés.

---

## 8. Anti-patterns observés

| Anti-pattern | Symptôme | Correctif |
|---|---|---|
| **Sprawl** | Skill trop long, attention diluée | Divulguer la référence, splitter par branche |
| **Duplication** | Même règle à deux endroits | Source de vérité unique + pointeur |
| **No-op** | « Sois rigoureux » | Supprimer ou remplacer par un critère vérifiable |
| **Négation** | « Ne fais pas X » | Formuler la cible positive |
| **Cache stale** | Recopie de `package.json` | Pointer vers l'environnement |
| **Commentaire-échappatoire** | L'agent justifie un contournement | Lint rule + message qui demande la cause racine |
| **Persona** | « Tu es un architecte senior » | Décrire la méthode, pas le personnage |
| **Routeur monolithe** | Toutes les règles dans un fichier | Playbooks + principes séparés |
| **Skill orphelin** | Personne ne sait quand l'utiliser | Routeur ou description plus précise |
| **Skill immortel** | Encode une limite de modèle dépassée | Déclarer l'hypothèse, réévaluer, supprimer |

---

## 9. Ce que cela implique pour nos skills

1. **Écrire petit d'abord.** Un skill doit tenir en 400–700 mots. Si ce n'est pas possible, c'est un routeur ou un playbook.
2. **Déclarer le mode d'invocation.** Chaque skill doit savoir s'il est un mode, un routeur, une brique autonome ou une référence.
3. **Un critère de fin par étape.** Pas de « comprendre », pas de « améliorer ».
4. **Une preuve par skill.** Chaque skill doit dire quel artefact prouve qu'il a réussi.
5. **Un pointeur, pas une copie.** Les ressources partagées vivent à un seul endroit.
6. **Une hypothèse de suppression.** Chaque skill doit pouvoir répondre : « quand le modèle saura faire X, ce skill disparaît ».

---

## 10. Questions ouvertes

- **Quel est l'équivalent d'un lint pour un skill ?** Comment valider automatiquement qu'un skill est bien formé, sans l'exécuter ?
- **Comment mesurer la qualité d'un skill ?** Taux de succès, coût en tokens, nombre de corrections humaines, temps jusqu'à preuve ?
- **Comment gérer les skills qui dépendent du modèle ?** Un skill calibré pour Opus 5.5 est-il encore valide pour Opus 7 ?
- **Comment représenter le couplage dans le frontmatter ?** `requires`, `blocks`, `verifies`, `informs` ?
- **Quel est le niveau de granularité minimal ?** Un skill par action, par phase, par rôle, ou par artefact ?
