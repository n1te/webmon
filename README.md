# Architecture Overview

## Scheduler Application

The Scheduler Application schedules website checks by fetching configurations from PostgreSQL and producing tasks for Kafka.

### Components

- **PostgreSQL Service**: Fetches website configurations.
- **Kafka Producer Service**: Produces tasks for Kafka.

## Checker Application

The Checker Application monitors website availability by consuming tasks from Kafka, checking websites via HTTP requests, and storing metrics in PostgreSQL.

### Components

- **Kafka Consumer Service**: Consumes tasks from Kafka.
- **HTTP Service**: Performs website checks.
- **PostgreSQL Service**: Stores metrics.

# Installation

*python 3.10 or higher required*

## Venv
```shell
python -m venv .venv
source .venv/bin/activate
```
Or
```shell
pip install virtualenvwrapper
mkvirtualenv webmon
```
Then
```shell
pip install -r requirements_dev.txt
```

## Configs

```shell
cp scheduler/config-example.yaml scheduler/config.yaml
cp checker/config-example.yaml checker/config.yaml
```

Adjust apps' configs according to your postgres and kafka settings

## Database
```shell
make scheduler-db-init
make checker-db-init
```

## Kafka
Put `ca.pem`, `service.cert`, and `service.key` files to the `./certs/kafka/` folder. It's also possible to use Kafka without ssl - just delete the `ssl` section from `config.yaml`.

# Running

Run the scheduler app:
```shell
make run-scheduler
```

And, in a separate shell - checker app:
```shell
make run-checker
```

# Tests

```shell
make test-scheduler
make test-checker
```

# Notes

## Architecture

There are a few alternative options for the scheduler architecture, such as the use of a sorted in-memory queue of sites. But unlike the current implementation, those are not scalable and take O(n) memory.

## Possible improvements

### Performance

A single instance of the scheduler can create a few tens of thousands of tasks every 5 seconds. It can be optimized to handle more by implementing batch processing.

To check millions of sites we need to implement some orchestrator for schedulers or use db shards with one scheduler instance per shard.   

Checker can be scaled as much as Kafka allows.

### Other

- separate venv and build configs for checker and scheduler
- divide checker to 2 parts - one checks sites, another saves data
- use milliseconds for more precision
- better monorepo-like setup
- integration tests
