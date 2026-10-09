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