# Windmill Workspace

## Purpose

This repository is the source of truth for Windmill job definitions and deployment configuration. It separates orchestration from reusable pipeline implementation.

Windmill handles job execution, scheduling, logs, and monitoring. Reusable pipeline logic lives in independent Python repositories.

## Ecosystem Overview

Imagine three independent data projects: A, B, and C. Each has its own GitHub repository, code, tests, and dependencies. Windmill runs them through lightweight wrapper scripts stored in this repository.

| Repository / Component | Responsibility |
|---|---|
| `data-ingest-a` | Pipeline A: data collection, transformation, and output |
| `data-ingest-b` | Pipeline B: a separate ingestion pipeline |
| `data-ingest-c` | Pipeline C: another independent ingestion pipeline |
| `openbao_client` | Shared Python client for retrieving secrets from OpenBao |
| `windmill-workspace` | Windmill wrappers, job metadata, and deployment configuration |
| OpenBao | Centralized secret storage |
| Windmill | Executes jobs and manages schedules, logs, and failures |
| GitHub Actions + self-hosted runner | Planned automation for testing and deployment |

## How the Repositories Integrate

Each pipeline is developed and maintained independently. The Windmill workspace does not contain the implementation of every pipeline; it contains the small scripts that connect those implementations to Windmill.

```text
GitHub repositories
│
├── data-ingest-a
│   └── Pipeline A implementation
│
├── data-ingest-b
│   └── Pipeline B implementation
│
├── data-ingest-c
│   └── Pipeline C implementation
│
├── openbao_client
│   └── Shared secret-access library
│
└── windmill-workspace
    └── f/
        ├── pipeline_a/
        │   ├── run_a.py
        │   └── run_a.script.yaml
        ├── pipeline_b/
        │   ├── run_b.py
        │   └── run_b.script.yaml
        └── pipeline_c/
            ├── run_c.py
            └── run_c.script.yaml
                    │
                    ▼
              Windmill server
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Pipeline A Pipeline B Pipeline C
          │         │         │
          └─────────┼─────────┘
                    ▼
               OpenBao
          (secrets as needed)
```

The diagram represents logical relationships, not the exact runtime call sequence: each wrapper invokes its own pipeline and retrieves secrets when required.

## What a Wrapper Does

A typical wrapper is intentionally small. It:

1. Retrieves an OpenBao token from a Windmill variable.
2. Creates an `OpenBaoClient`.
3. Imports the relevant pipeline package.
4. Invokes the pipeline's entry point.
5. Returns the result to Windmill.

Conceptual example:

```python
import wmill
from openbao_client import OpenBaoClient
from data_ingest_a import run_pipeline

def main():
    token = wmill.get_variable("f/infrastructure/openbao_token")
    bao = OpenBaoClient(
        address="http://openbao:8200",
        token=token,
    )
    return run_pipeline(bao)
```

The exact package imports and function signatures depend on each pipeline's implementation.

## Day-to-Day Workflow

### Develop a pipeline

1. Work in the pipeline's own repository, such as `data-ingest-a`.
2. Implement and test the reusable Python logic.
3. Commit and publish the package so Windmill can install it.
4. Keep pipeline-specific tests and dependencies in that repository.

### Integrate it with Windmill

1. Add a wrapper script and metadata under `f/` in `windmill-workspace`.
2. Declare the required Python packages in the Windmill script's dependency metadata.
3. Configure inputs and other Windmill-specific settings.
4. Test the wrapper in Windmill.

### Deploy with the Windmill CLI

From the `windmill-workspace` repository root:

```bash
# Review local changes
git status
git diff

# Preview the deployment
wmill sync push --dry-run

# Deploy after reviewing the plan
wmill sync push
```

The `wmill.yaml` file controls which local files are included in synchronization. Review every dry run: synchronization can modify or delete remote items within the configured scope.

### Commit and publish changes

```bash
git add f/ wmill.yaml wmill-lock.yaml
git commit -m "Add or update Windmill job"
git push
```

Pushing to GitHub does not deploy to Windmill automatically in the current setup. Deployment is manual until CI/CD is configured.

## Responsibilities and Boundaries

- **Pipeline repositories:** own reusable business logic, transformations, tests, and package dependencies.
- **`openbao_client`:** owns the shared Python interface for accessing secrets.
- **`windmill-workspace`:** owns Windmill-specific wrappers, metadata, and deployment configuration.
- **OpenBao:** stores secrets; credentials should not be committed to Git.
- **Windmill:** runs jobs and manages schedules, execution history, and logs.
- **GitHub Actions:** will eventually automate validation and deployment.

## Important Considerations

- **Package versions:** pin pipeline dependencies to known versions or commits for predictable deployments.
- **Independent deployment:** publishing a new pipeline package does not automatically update a Windmill job.
- **Secrets:** keep secrets in OpenBao or Windmill variables, never in Git.
- **Sync scope:** keep `wmill.yaml` narrowly scoped and review dry runs before deployment.
- **Additional configuration:** schedules, flows, resources, and other Windmill objects may also need version control.

## Planned Improvements

- Configure a self-hosted GitHub Actions runner.
- Automate validation and deployment from trusted GitHub changes.
- Establish package versioning and dependency update procedures.
- Version-control schedules and flows where appropriate.
- Document deployment safeguards and rollback procedures.

## Guiding Principle

**Pipeline repositories define what the data jobs do. `windmill-workspace` defines how Windmill runs them.**