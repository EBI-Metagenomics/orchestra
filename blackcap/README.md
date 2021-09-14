# Blackcap

Shared library for Orchestra

## Getting started

### Install dependencies and project root

```bash
poetry install
```

### Configuration

A `blackcap.env` is required to configure `blackcap`.
It expects it be present at `$HOME/.config/orchestra/blackcap.env`.

Make sure to add the following environment variables:

```bash
# file: .config/orchestra/blackcap.env
# Replace the values with your own

GOOGLE_APPLICATION_CREDENTIALS="path/to/gcp/credentials/json"
GCP_PROJECT_ID="gcp-project-id"
```

### CLI usage

```bash
Usage: blackcap [OPTIONS] COMMAND [ARGS]...

  blackcap console.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  pub  GCP pub/sub channel publish commands.
```

examples:

```bash
# Publish random msg
blackcap pub chatter

# Publish a custom msg
blackcap pub custom --data "Hello! this is a custom msg"

# Publish a job
blackcap pub job --file "job.json"

```
