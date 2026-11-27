# Nectar — All Code Is Slop (Except Mine)

> **Thèse en une phrase** : la vitesse des agents ne se gagne pas en ajoutant des règles, mais en investissant dans un environnement où le bon comportement est le comportement par défaut — codebase, types, lint, architecture, vérification — la prose n'étant que la dernière couche.

**Source** : Lauren Tan (poteto), AI Engineer, 2026-11-14 · [vidéo](https://www.youtube.com/watch?v=O_zcc6Xl12g) · [transcript](transcript.md)

---

## 1. Le problème n'est pas la vitesse, c'est la confiance

Le point de départ est un constat culturel : tout le monde trouve que le code des autres est du slop. Avec les agents, chacun peut devenir une « coding machine ». La question devient donc :

> « the job of the software engineer, the meta of being a software engineer is figuring out how to maintain or even improve the quality of your code while massively increasing your productivity. » — 00:44

La réponse n'est pas la confiance aveugle. C'est un **investissement dans l'environnement de l'agent** pour pouvoir lui faire confiance. Il a fallu six mois pour atteindre le point où des milliers de PR peuvent être livrées, dont beaucoup pendant le sommeil.

**Idée force** : un agent fiable est un agent dont l'environnement rend les erreurs coûteuses ou impossibles.

---

## 2. La pyramide inversée de l'environnement

La conférence propose une hiérarchie d'investissement, des couches les plus déterministes aux plus interprétatives (01:59) :

```text
        ▲  moins déterministe, plus de jugement
        │
   ┌────┴─────────────────────────────┐
   │  Prose : rules, skills, AGENTS.md │   ← petite couche finale
   ├──────────────────────────────────┤
   │  Vérification : runtime, formelle │   ← trouve les bugs, prouve les invariants
   ├──────────────────────────────────┤
   │  Checks statiques : lint, types   │   ← contraint par défaut
   ├──────────────────────────────────┤
   │  Code & architecture              │   ← le plus gros levier
   └──────────────────────────────────┘
        ▼  plus déterministe, plus reproductible
```

Deux principes en découlent :

1. **Le code et l'architecture sont les premiers leviers.** Un bon design d'API, un bon découpage, un type system expressif, des lint rules : tout cela contraint ce que l'agent peut faire.
2. **La prose est le dernier recours.** Une règle dans `AGENTS.md` n'est pas reproductible ; un check dans le code l'est.

> « whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules or your agents.md » — 02:44

**Pour notre framework** : un skill qui se contente d'écrire « fais attention à X » est un skill faible. Un skill qui déclenche un lint, un type, un test ou une vérification runtime est un skill fort. La valeur d'un skill dépend de sa capacité à **changer l'environnement**, pas seulement à ajouter du texte au contexte.

---

## 3. Le codebase est un jardin, pas un dépôt

Analogie centrale (03:27) : le code arrive désormais en flux continu, presque organique. Les contraintes et les guardrails sont les fondations concrètes autour desquelles le nouveau code pousse.

Conséquence : **tout ce qui existe sera copié**. Les workarounds, les anti-patterns, la dette technique et le code déprécié deviennent le « pattern établi » que le prochain agent imitera. Comme des mauvaises herbes, ils se propagent.

> Le travail de l'ingénieur devient un travail de jardinier : garder le codebase assez propre pour que les agents copient le bon stuff.

**Pour notre framework** : les skills de revue et de refactoring ne sont pas de la maintenance cosmétique. Ce sont des **skills de protection du corpus d'entraînement local**. Un codebase sale est un prompt sale.

---

## 4. Contraindre au lieu de corriger : quatre exemples

### 4.1 Bannir ce qui exige trop de nuance

> « anything that requires nuance to use well often leads to slop » — 05:33

Exemple : `useEffect` en React. Il a des usages légitimes, mais il est souvent mal utilisé et demande une expertise considérable. Décision : l'interdire dans le code produit, l'autoriser uniquement dans certaines API internes. Le problème est **éliminé catégoriquement**, plus jamais revu en review.

### 4.2 La structure de répertoires comme contexte

Dans une app Electron, les agents importaient du code du main thread dans le renderer, causant des long tasks et du jank. Solution : deux répertoires top-level explicites (`electron-main`, `electron-renderer`) et une règle de dépendance qui interdit les imports croisés.

Le nom du répertoire **encode la règle** : l'agent n'a pas besoin de lire une consigne pour comprendre la frontière.

### 4.3 Les commentaires comme échappatoire

Les agents écrivaient des commentaires pour **justifier** un contournement, ou sur-généralisaient une petite correction en règle absolue. Pire : les commentaires ne sont pas exécutables, donc ils ne peuvent pas être vérifiés.

Décision : bannir 99 % des commentaires. À la place, des lint rules avec des messages d'erreur utiles qui disent à l'agent de corriger la cause racine.

### 4.4 Les timers comme symptôme d'un clash d'architecture

Les agents utilisaient `setTimeout`, `requestAnimationFrame`, `requestIdleCallback` pour masquer un conflit entre le style impératif de VS Code et le style déclaratif de React. Résultat : des timers partout, du garbage collection, du lag. La correction n'est pas une règle « ne pas utiliser de timers » ; c'est un **changement d'architecture**.

**Pattern général** : à chaque correction répétée, se demander si le problème peut être éliminé par la structure plutôt que par une consigne.

> « every time we correct our agents, it turns into one of these deterministic checks or we think about how to categorically eliminate that problem in the code through better API design, through better architecture. » — 08:54

---

## 5. La revue devient une revue de preuves

La code review humaine se réduit progressivement à examiner des **artefacts de vérification** (09:32) :

- vidéos et captures d'écran ;
- diagrammes ;
- vérification formelle ;
- sorties de tests et de profils.

### Vérification runtime

Donner à l'agent les outils qu'un humain utilise : lancer l'app, CDP, debugger, captures. Deux techniques concrètes :

1. **Feature map** : une carte de toutes les fonctionnalités du point de vue utilisateur. Elle donne un vocabulaire partagé — « le truc dans la sidebar » devient une entité nommée — et évite que l'agent devine.
2. **CLIs custom** : des pilotes réutilisables, consommables par l'agent, qui réduisent les tokens et sont testables.

### Vérification formelle

TLA+ pour model-checker des flux majeurs (notifications multi-appareils, multi-plateformes). Lean pour prouver des algorithmes (une lib de virtualisation, pour éviter le flicker). Ce n'est pas une baguette magique : c'est une couche de plus.

### Property-based testing

Bombadil pour les UIs : générer des interactions et vérifier des propriétés. A déjà trouvé des bugs.

> « we are entering a golden age of software testing and verification because agents let us test everything to a much greater degree than used to be economical » — 12:13

**Pour notre framework** : la vérification doit être un **nœud de première classe** du graphe, pas une étape optionnelle à la fin. Un skill de livraison sans skill de preuve est incomplet.

---

## 6. Les chiffres cités

| Métrique | Valeur | Contexte |
|---|---:|---|
| PR livrées personnellement | 3 000 / mois | avant la conférence |
| PR livrées par l'équipe | 11 000 / mois | mois précédent |
| Contributeurs ayant au moins une PR | 227 | octobre |
| Taux de revert | ~0,5 % | stable, en baisse relative |
| Releases stables | ~1 / jour | rythme de release |
| Tokens en vérification | ~70 % | citation d'une autre ingénieure, corroborée par l'autrice |

La performance de l'app s'est améliorée sur plusieurs dimensions (startup, frappe, ouverture et changement de chat), malgré une app Electron et une vélocité élevée.

**Lecture** : le volume n'est pas obtenu en baissant les standards. Il est obtenu en rendant les standards **exécutables**.

---

## 7. L'ordre d'investissement

La conclusion est prescriptive (14:49) :

1. **Améliorer le codebase d'abord.** Ajouter un lint rule pour empêcher les nouvelles occurrences d'un anti-pattern, puis nettoyer les anciennes.
2. **Rendre la vérification solide.** Runtime, puis formelle quand c'est justifié.
3. **Automatiser seulement ensuite.** Une boucle interne qui produit du slop produit plus de slop quand on l'automatise.

> « if your inner coding loop produces slop, then automating that loop just produces more slop » — 15:29

C'est un principe d'ordonnancement pour notre graphe : **les nœuds de qualité précèdent les nœuds d'automatisation**. On ne branche pas un swarm sur une boucle non vérifiée.

---

## 8. La boucle externe

Une fois les fondations posées, l'automatisation devient possible (16:11) :

- à chaque release, une routine lance un projet qui **fuzz** toute l'application ;
- elle trouve des bugs en utilisant l'app comme un utilisateur ;
- elle ouvre une PR de fix par bug ;
- elle auto-merge.

> « our codebase is good enough that pull requests tend to just be good by default » — 16:44

C'est le stade final : l'outer loop peut faire confiance à l'inner loop parce que l'environnement rend les PR bonnes par défaut.

---

## 9. Implications pour notre framework de skills

### À reprendre

- **La pyramide inversée comme critère de qualité d'un skill.** Un skill doit être classé par la couche qu'il renforce : code/architecture, checks statiques, vérification, prose.
- **Le concept de correction qui devient structure.** Chaque skill de rétrospective doit produire un lint, un test, un type ou un script — pas seulement une note.
- **La vérification comme nœud du graphe.** Preuve runtime, feature map, CLIs de pilotage, propriétés formelles.
- **L'ordre d'investissement.** Ne pas automatiser avant d'avoir une boucle interne fiable.
- **Le codebase comme input.** Les skills doivent lire et protéger les conventions existantes.

### À adapter

- **Le bannissement comme technique.** Très efficace pour les anti-patterns à fort usage, mais dangereux si le skill ne distingue pas l'usage légitime. Toujours prévoir une exception localisée et documentée par la structure.
- **La revue par artefacts.** Excellente pour l'UI et les flux, insuffisante pour la sécurité, les migrations de données et les invariants métier.
- **Les métriques de volume.** 11 000 PR n'est pas un objectif en soi ; le vrai signal est le taux de revert, la performance et la stabilité.

### À rejeter

- **Copier les outils d'une équipe sans son contexte.** TLA+, Lean, Bombadil ne sont pas des prérequis ; ce sont des réponses à des problèmes précis.
- **Faire de la prose la couche principale.** C'est précisément ce que la conférence démontre comme inefficace.

### Question ouverte pour la suite

Quel est l'équivalent, pour un **skill**, d'un lint rule ? Autrement dit : comment rendre un skill **exécutable et vérifiable** plutôt que déclaratif ? C'est la question centrale de notre phase de construction.

---

## 10. Citations à garder

> « the job of the software engineer, the meta of being a software engineer is figuring out how to maintain or even improve the quality of your code while massively increasing your productivity. » — 00:44

> « whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules or your agents.md » — 02:44

> « anything that requires nuance to use well often leads to slop » — 05:33

> « every time we correct our agents, it turns into one of these deterministic checks or we think about how to categorically eliminate that problem in the code » — 08:54

> « if your inner coding loop produces slop, then automating that loop just produces more slop » — 15:29

> « our codebase is good enough that pull requests tend to just be good by default » — 16:44
