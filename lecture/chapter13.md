## **Chapter 13: Git Basic Commands**

Despite a flourishing ecosystem of graphical clients, **Git** remains—at its philosophical core—a *command-line* tool.  Mastering its verbs yields two dividends: you gain deterministic control over your repository’s history, and you can automate workflows in CI/CD where no GUI exists.  This chapter demystifies the everyday subset—`init`, `clone`, `add`, `commit`, `status`, `log`, `diff`, `branch`, `merge`, `push`, `pull`, `tag`, and `stash`.  We will link each command to the underlying directed acyclic graph (DAG) of commits so that you understand *why* Git behaves as it does when confronted with fast-forwards, detached HEADs, and conflict markers.  By building a miniature feature branch, resolving a merge conflict, and pushing to a remote on GitHub or GitLab, you will lay the cognitive rails for larger, team-based collaborations encountered in capstone projects and professional practice.

---

### **1. Theories**

**1.1  Git’s Data Model**
Git is not a file-based tracker but a **content-addressable object store**.  Four objects live in `.git/objects/`:

* **Blob** – file contents.
* **Tree** – directory snapshot (names → SHA1 of blobs/trees).
* **Commit** – pointer to a tree plus metadata (author, date, parent).
* **Tag** – named pointer, often to a commit.
  Because each commit stores a *full* tree, version history is a linked list (or DAG) of immutable snapshots.  A *branch* is merely a named reference (ref) to the *latest* commit in a line.

**1.2  The Three Git Areas**

1. **Working Directory** – actual files on disk.
2. **Staging Area (Index)** – files marked for the *next* commit.
3. **Repository (HEAD)** – last committed state.
   `git add` moves changes from working directory to index; `git commit` writes the index to a new commit and advances the current branch.

**1.3  Core Commands Explained**

| Command                | Action                               | Common Flags                   |
| ---------------------- | ------------------------------------ | ------------------------------ |
| `git init`             | Initialise an empty repo (`.git/`).  | `--initial-branch=<name>`      |
| `git clone <url>`      | Copy remote repo and set `origin`.   | `--depth 1` (shallow)          |
| `git status`           | Show staged/unstaged files & branch. | `-s` (short)                   |
| `git add <file>`       | Stage new/modified file.             | `-p` (interactive hunks)       |
| `git commit -m "msg"`  | Record staged snapshot.              | `--amend`, `-S`                |
| `git log`              | Inspect history.                     | `--oneline --graph --decorate` |
| `git diff`             | View line changes.                   | `--staged`, `branchA..branchB` |
| `git branch <name>`    | Create branch pointer.               | `-d` (delete), `-M` (move)     |
| `git checkout <name>`  | Switch files & HEAD.                 | `-b` (create then switch)      |
| `git merge <branch>`   | Bring changes into current branch.   | `--no-ff`, `--squash`          |
| `git push origin main` | Upload new commits to remote.        | `--set-upstream`               |
| `git pull`             | `fetch` + `merge` (or `rebase`).     | `--rebase`                     |
| `git tag v1.0`         | Mark commit for release.             | `-a -m` (annotated)            |
| `git stash`            | Shelve uncommitted work.             | `pop`, `list`, `apply`         |

**1.4  Fast-Forward vs Three-Way Merge**
If branch `main` has not diverged from `feature`, merging `feature` is a pointer move—**fast-forward (FF)**.  If both have new commits, Git performs a **three-way merge** using the latest common ancestor, produces a merge commit, and may surface conflicts (`<<<<<<<`).  Using `--no-ff` forces a merge commit even when FF is possible, preserving branch context.

**1.5  Remote Repositories**
A *remote* is a URL plus a refspec.  `origin` is conventional, but multiple remotes (e.g., GitHub + GitLab) are allowed.  `git fetch origin` downloads objects and updates remote-tracking branches (`origin/main`).  *Nothing* touches local branches until you `merge` or `rebase`.

**1.6  HEAD and Detached HEAD**
`HEAD` points to the current branch ref, which in turn points to a commit.  Checking out a specific commit (`git checkout abc123`) detaches `HEAD`; new commits create an *orphaned* line unless you `git switch -c new_branch`.

**1.7  Rebase vs Merge**
`git rebase feature main` re-writes commit *identities* so that `feature` appears to fork from the tip of `main`.  Advantages: linear history; disadvantages: rewritten SHAs break shared history—never rebase *public* branches.

**1.8  Tagging and Semantic Versioning**
Annotated tags (`git tag -a v1.2.0 -m "release note"`) create tag objects with GPG signatures if `-s`.  CI/CD pipelines often trigger on tags to build release artefacts.

**1.9  Undo Safety Nets**

* `git restore <file>` – discard *working* changes.
* `git restore --staged <file>` – unstage.
* `git reset --soft HEAD~1` – keep file changes, move branch back.
* `git revert <commit>` – make *inverse* commit, preserving history.

**1.10  Collaboration Etiquette**
Write atomic commits: *one logical change per commit with a message in imperative mood*: “Add rental fee validation.”  Use feature branches named `feature/qr-payment`.  Open Pull Requests early; leverage code review.  Run `git fetch --prune` to remove deleted remote refs.

---

### **2. Step-by-Step Workshop**

* **Initialise repo**

  ```bash
  git init bike-kiosk && cd bike-kiosk
  echo "# Bike Kiosk" > README.md
  git add README.md && git commit -m "Initial commit"
  ```
* **Create feature branch**

  ```bash
  git switch -c feature/qr-payment
  touch qr.py && git add qr.py
  git commit -m "Add QR generator scaffold"
  ```
* **Simulate conflict** in `main`:

  ```bash
  git switch main
  echo "placeholder" >> qr.py
  git add qr.py && git commit -m "Add placeholder"
  ```
* **Merge & resolve**

  ```bash
  git merge feature/qr-payment   # conflict!
  # open editor, fix markers, then:
  git add qr.py
  git commit -m "Merge feature/qr-payment"
  ```
* **Add remote & push**

  ```bash
  git remote add origin https://github.com/<user>/bike-kiosk.git
  git push -u origin main
  ```
* **Tag release**

  ```bash
  git tag -a v0.1.0 -m "Minimum viable kiosk"
  git push origin v0.1.0
  ```

---

### **3. Assignment**

* Fork the course template repository.
* Implement a **feature branch** `feature/documentation` that adds `docs/installation.md`.
* Perform **two commits**: initial doc and stylistic update.
* Rebase your feature branch onto updated `main`.
* Open a Pull Request; capture a screenshot of the PR diff and the Git log (`--oneline --graph`).
* Tag the merged commit as `v0.2.0` and push tag.

---

### **4. Conclusion**

Git’s elegance lies not in a single command but in how a handful of verbs compose to manage snapshots, collaborate safely, and automate releases.  By internalising the object model and the working-staging-HEAD triad, you can predict the outcome of each command rather than memorise recipes.  This predictive power scales from solo scripts to multi-team monorepos and underpins every modern DevOps pipeline you will encounter.
