# Conductor

Backend for orchestra

## Getting started

### Install dependencies and project root

```bash
poetry install
```

### Configuration

A `conductor.env` is required to configure `conductor`.
It expects it be present at `$HOME/.config/orchestra/conductor.env`.

Make sure to add the following environment variables:

```bash
# file: .config/orchestra/conductor.env
# Replace the values with your own

GOOGLE_APPLICATION_CREDENTIALS="path/to/gcp/credentials/json"
GCP_PROJECT_ID="gcp-project-id"
```

### CLI usage

```bash
Usage: conductor [OPTIONS] COMMAND [ARGS]...

  Conductor console.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  pub  GCP pub/sub channel publish commands.
```

examples:

```bash
# Publish random msg
conductor pub chatter

# Publish a custom msg
conductor pub custom --data "Hello! this is a custom msg"

# Publish a job
conductor pub job --file "job.json"

```
