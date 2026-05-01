# Conversion Report

| Field | Value |
|---|---|
| **Source** | `.data\input\1\Jenkinsfile` |
| **Output** | `.data\output\1\ci.yml` |
| **Status** | ✅ APPROVED |
| **Iterations** | 1 / 5 |
| **Confidence** | HIGH |
| **Generated** | 2026-03-09 01:32:50 |

## Iteration History

| # | Action | Result | Comment |
|---|---|---|---|
| 1 | Convert | Generated YAML |  |
| 1 | Review | APPROVED |  |

## Manual Verification Checklist

> Items below are common Jenkins→GHA conversion issues that
> automated tools frequently miss. Review each relevant item.

- [ ] **Secrets & Credentials** — Verify all `credentials()` / `withCredentials` blocks are replaced with GitHub Secrets (`${{ secrets.NAME }}`)
- [ ] **Custom Plugins** — Check for Jenkins plugin steps (SonarQube, Artifactory, etc.) that may need equivalent GitHub Actions
- [ ] **Shared Libraries** — Verify `@Library` imports are replaced with equivalent actions or composite workflows
- [ ] **Self-Hosted Runners** — Confirm `runs-on` labels match your GitHub runner infrastructure
- [ ] **Environment Variables** — Check dynamic `environment {}` blocks are correctly mapped to `env:` or `${{ vars.NAME }}`
- [ ] **Post-Build Actions** — Verify notifications (email, Slack, Jira) are handled via appropriate actions
- [ ] **Triggers** — Confirm `on:` triggers match original Jenkins trigger behavior (cron, pollSCM, upstream)
- [ ] **Artifacts & Workspace** — Verify `stash`/`unstash` replaced with `actions/upload-artifact` / `actions/download-artifact`
- [ ] **Parallel Execution** — Confirm parallel stages map to concurrent GHA jobs with correct `needs` dependencies
- [ ] **YAML Validity** — Run the generated workflow through a YAML linter or `actionlint`
- [ ] **Other** — Check for any other Jenkins-specific constructs not covered above

## Generated Workflow

```yaml
name: Jenkins to GitHub Actions Conversion

on:
  push:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Build
      run: echo "build"

    - name: Test
      run: echo "test"
```
