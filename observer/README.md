# Observer

Welcome to Observer.

## Getting Started with Observer

### Requirements

- [Golang](https://golang.org/dl/) 1.6 or higher
- [Mage](https://github.com/magefile/mage/releases) (tested with v1.11.0)

### Init Project

To get running with Observer and also install the
dependencies, run the following command:

```bash
go mod vendor
```

For further development, check out the [beat developer guide](https://www.elastic.co/guide/en/beats/libbeat/current/new-beat.html).

### Build

To build the binary for Observer run the command below. This will generate a binary
in the same directory with the name observer.

```bash
mage build
```

### Run

To run Observer with debugging output enabled, run:

```bash
./observer -c observer.yml -e -d "*"
```

### Test

To test Observer, run the following command:

```bash
mage test
```

The test coverage is reported in the folder `./build/coverage/`

### Cleanup

To clean up the build directory and generated artifacts, run:

```bash
mage clean
```

## Packaging

The beat frameworks provides tools to crosscompile and package your beat for different platforms. This requires [docker](https://www.docker.com/) and vendoring as described above. To build packages of your beat, run the following command:

```bash
mage package
```

This will fetch and create all images required for the build process. The whole process to finish can take several minutes.
