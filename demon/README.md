# Demon

Daemon running on master nodes

## Getting started

### Install dependencies and project root

```bash
poetry install
```

### Configuration

A `demon.env` is required to configure `demon`.
It expects it be present at `$HOME/.config/orchestra/demon.env`.

Make sure to add the following environment variables:

```bash
# file: .config/orchestra/demon.env
# Replace the values with your own

GOOGLE_APPLICATION_CREDENTIALS="path/to/gcp/credentials/json"
GCP_PROJECT_ID="gcp-project-id"
```

### CLI usage

```bash
Usage: demon [OPTIONS] COMMAND [ARGS]...

  Demon console.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  sub  GCP pub/sub channel subscribe commands.
```

examples:

```bash
# Subscribe and echo msg
conductor sub echo

```
