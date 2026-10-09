# Windmill Workspace

## Purpose

This repository is the source of truth for Windmill job definitions and deployment configuration. It separates orchestration from reusable pipeline implementation.

Windmill is responsible for job execution, scheduling, logs, and monitoring. Pipeline logic lives in independent Python repositories.

## Ecosystem

| Component | Responsibility |
|---|---|
| `windmill-workspace` | Windmill scripts, flows, metadata, and deployment configuration |
| `data-ingest-*` repositories | Reusable data ingestion and transformation logic, tests, and dependencies |
| `openbao_client` | Python client for retrieving secrets from OpenBao |
| OpenBao | Centralized secret storage |
| Windmill | Job execution, scheduling, and monitoring |
| GitHub Actions + self-hosted runner | Automated testing and deployment (planned) |

## Job Architecture

Each pipeline is developed and tested independently. A small Windmill wrapper imports the published pipeline package and `openbao_client`, retrieves the required secrets, and invokes the pipeline entry point.

```text
GitHub: pipeline repository
        |
        v
Published Python package
        |
        v
windmill-workspace
  └── f/
      └── <folder>/
          ├── <job>.py
          ├── <job>.script.yaml
          └── folder.meta.yaml
        |
        v
Windmill executes the wrapper
        |
        v
Pipeline package + OpenBao secrets
```

## Day-to-Day Workflow

### Create or update a job

1. Develop and test reusable logic in its own Python repository.
2. Publish or otherwise make the package available to Windmill.
3. Create or update the wrapper and metadata in `windmill-workspace`.
4. Test the wrapper and its inputs.
5. Review the deployment plan.
6. Deploy the changes and verify execution.

### Deploy with the Windmill CLI

From the repository root:

```bash
# Review local changes
git status
git diff

# Preview deployment changes
wmill sync push --dry-run

# Deploy only after reviewing the plan
wmill sync push
```

The CLI uses `wmill.yaml` to determine which local files are in scope. Review the planned changes before every deployment: synchronization can modify or delete remote items within that scope.

### Git workflow

Commit job definitions and configuration to Git so changes are auditable and reversible.

```bash
git add f/ wmill.yaml wmill-lock.yaml
git commit -m "Add or update ingestion job"
git push
```

Pushing to GitHub does **not** deploy to Windmill automatically in the current setup. Deployment is performed manually with the CLI until CI/CD is configured.

## Configuration and Secrets

- Keep secrets out of Git. Store them in OpenBao or Windmill variables.
- Keep Windmill-specific configuration in this repository.
- Keep reusable business and data-processing logic in the pipeline repositories.
- Use `wmill.yaml` to control the sync scope.
- Review changes to scripts, metadata, schedules, flows, and other resources before deploying them.

## Planned Improvements

- Set up a self-hosted GitHub Actions runner.
- Automate validation and deployment from trusted GitHub changes.
- Pin pipeline dependencies to known versions or commits.
- Version-control schedules and flows where appropriate.
- Add deployment safeguards and a documented rollback procedure.

## Guiding Principle

**Pipeline repositories define what the data jobs do. `windmill-workspace` defines how Windmill runs them.**