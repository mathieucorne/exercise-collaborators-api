# 🧩 Exercise: "Collaborators" API

## 📕 Documentation

➡️ [See the complete technical documentation](./doc/doc.md)

## ⚙️ Prerequisites

**Before launching the project locally, you must have installed:**

-   an IDE (we recommend [VS Code](https://code.visualstudio.com/download))
-   [Git](https://git-scm.com/)
-   [Python](https://www.python.org/downloads/)

## 🚀 Quickstart

### The Python Virtual Environment

1. **Create a Python virtual env.**

```bash
python -m venv ./
```

_**Optionnal** : It is worth checking that pip, the Python dependency manager, is itself up to date._

```bash
python -m pip install --upgrade pip
```

2. **Activate this virtual env. newly created**

-   on Windows

```bash
./Scripts/Activate.ps1
```

-   On Linux, MacOS, or using Bash

```bash
source .venv/bin/activate
```

3. **Install the Python dependencies**

```bash
python -m pip install -r requirements.txt
```

### Start a FastAPI Dev Server

```bash
fastapi dev app/main.py
```
