# Contributing to GSOC-REVIEW-PLATFORM

Thanks for your interest in contributing! This document explains how to get the project running locally, our conventions for code style and commits, and how to open a good pull request.

## Table of contents
- Getting started
- Code style and quality
- Branching & commits
- Creating a pull request
- Reporting bugs & feature requests
- Code of Conduct

## Getting started

1. **Fork the repository** on GitHub by clicking the "Fork" button.

2. **Clone your fork**:
```bash
git clone https://github.com/<your-username>/GSOC-REVIEW-PLATFORM.git
cd GSOC-REVIEW-PLATFORM
```

3. **Add the upstream remote** (to sync with the original repo):
```bash
git remote add upstream https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM.git
git fetch upstream
```

4. **Create a virtual environment / install dependencies** if the project requires them. The repository currently doesn't include explicit language-specific setup files; check the README for language-specific instructions. If unsure, open an issue.

5. **Run tests** (if available):
```bash
# example (replace with project's test command)
npm test
# or
pytest
```

## Code style and quality

- Follow existing project formatting and idioms.
- Add tests for new features and bug fixes when applicable.
- Lint and format your code before opening a PR.

## Branching & commits

**Important: Never commit directly to `main`!** All contributions must come from feature branches.

### Branch naming conventions

Create a descriptive branch from `main` for each change. Use one of these prefixes:

- `feat/` — for new features (e.g., `feat/add-user-authentication`)
- `fix/` — for bug fixes (e.g., `fix/login-redirect-issue`)
- `docs/` — for documentation updates (e.g., `docs/update-api-guide`)
- `refactor/` — for code refactoring (e.g., `refactor/simplify-auth-logic`)
- `test/` — for adding or updating tests (e.g., `test/add-login-tests`)
- `chore/` — for maintenance tasks (e.g., `chore/update-dependencies`)

### Creating your feature branch

```bash
# Make sure you're on main and it's up to date
git checkout main
git pull upstream main

# Create your feature branch
git checkout -b feat/your-feature-name
```

### Commit guidelines

- Keep commits small and focused on a single change.
- Use present-tense, imperative commit messages:
  - ✅ Good: `Add user authentication`, `Fix login redirect bug`
  - ❌ Bad: `Added stuff`, `Fixed things`, `WIP`
- Reference issue numbers when applicable: `Fix #123: Correct edge-case in validation`
- Make atomic commits — each commit should be a working state.

## Creating a pull request

### Before you submit

1. **Ensure you're on a feature branch** (not `main`). Check with:
   ```bash
   git branch --show-current
   ```
   If you're on `main`, create a new branch first!

2. **Test your changes locally** — run tests, lint, and verify functionality.

3. **Update your branch** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Submitting your PR

1. **Push your feature branch** to your fork:
   ```bash
   git push origin feat/your-feature-name
   ```

2. **Open a pull request** on GitHub:
   - Go to the original repository: `https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM`
   - Click "Pull requests" → "New pull request"
   - Click "compare across forks"
   - Set base repository: `nst-sdc/GSOC-REVIEW-PLATFORM` base: `main`
   - Set head repository: `<your-username>/GSOC-REVIEW-PLATFORM` compare: `feat/your-feature-name`

3. **Fill out the PR template** completely:
   - Write a clear title and description
   - Link related issues (e.g., `Closes #123`)
   - Add screenshots/videos if you changed UI
   - Describe how to test your changes

4. **Wait for review**:
   - Ensure all CI checks pass (tests, linting, etc.)
   - Respond to reviewer comments promptly
   - Push additional commits to your branch if changes are requested
   - **Do not force-push** after review has started unless explicitly asked

### PR acceptance criteria

Your PR will be merged when:
- ✅ It comes from a feature branch (not `main`)
- ✅ All CI/tests pass
- ✅ Code follows project style guidelines
- ✅ Changes are well-documented
- ✅ At least one maintainer approves
- ✅ All review comments are addressed

## Reporting bugs & feature requests

- Use GitHub Issues. Provide a clear title and steps to reproduce, expected vs actual behavior, and environment details.

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. Please be kind, respectful, and collaborative. Violations may be reported to the maintainers.

---

If anything in this document is unclear or missing, open an issue or a draft PR and we can iterate.
