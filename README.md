# 🧠 Mini-Agent IA — Boucle décisionnelle contrôlée

## 🧩 Fonctionnalités principales

### ✅ Actions supportées

- `ASK_PATH` → demander un fichier à l’utilisateur
- `READ_CODE` → lire un fichier de code en toute sécurité
- `EXPLAIN` → expliquer un fichier
- `GENERATE_CODE` → générer du code corrigé ou amélioré
- `CREATE_FILE` → créer un nouveau fichier dans un dossier sandbox
- `REFUSE` → refuser une action dangereuse ou invalide

---

## 🔁 Boucle décisionnelle contrôlée

L’agent fonctionne selon le cycle :

```
User input
   ↓
Decision (LLM)
   ↓
Action
   ↓
Update State
   ↓
(Repeat until done or max_steps)
```

---

## 🗂️ Structure du projet

```
project/
│
├── src/
│   ├── starter_code.py
│   ├── model_openai.py
│   ├── actions.py
│   └── tools.py
│
├── project/
│   └── generated/
│
└── README.md
```

---

## 🔐 Sécurité

- Lecture limitée au projet
- Écriture uniquement dans `project/generated`
- Aucun écrasement de fichier existant

---

## 🚀 Lancement

```bash
python src/starter_code.py
```


## 🧪 Exemples d’utilisation

```bash
explique le fichier buggy_code
```
```bash
Corriger et créer un nouveau fichier
```
