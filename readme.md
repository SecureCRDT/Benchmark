 # CRDT Benchmark

<img src="https://img.shields.io/badge/status-research%20prototype-green.svg" />

CRDT Benchmark is a performance tool that measures the latency and throughput of conflict-free replicated data types (CRDT) operations.  It provides a set of workloads to assess the performance of the following CRDTs:

- Last Writer Wins Register
- Max Value
- Positive Negative Counter
- Bounded Counter
- Grow only Counter
- Grow only Set

# How it works

CRDT Benchmark is built on top of [Locust](https://locust.io/), a widely-used industry-standard tool to measure the performance of large-scale HTTP services. Locust offers two main advantages: first, it provides a clear separation between workload and benchmark framework, making it easy to extend the benchmark with new workloads; secondly, its designed to be independent of the system being tested. This enables our benchmark to be reused and measure the performance of different CRDT implementations.

## Dependencies

CRDT Benchmark is implemented and tested in Python 3.9 and has the following dependencies:

- Python 3.9
- [Poetry](https://python-poetry.org/)
- [Locust](https://locust.io/)

## Installation

To run the benchmark, you must first install its dependencies by using the following command:

```sh
$ poetry install
```

## Running a Workload

> :warning: **Evaluating the SecureCRDT prototype**: To evaluate the performance of our research prototype [SecureCRDT](https://github.com/SecureCRDT/SecureCRDT), you must first initiate the CRDT client according to the instructions in the project README.

You can measure the performance of a CRDT system by running a workload with the Locust engine. The following example command has placeholder variables that need to be replaced:

- `$CRDT`: The CRDT workload that the locust engine will use
- `$CRDT_SERVER_IP`: The IP of the CRDT Replica that will handle the benchmark requests
- `$CRDT_OPERATION`: The CRDT operation that will be evaluated (e.g.: `update` or `query`)
- `$RUN_TIME`: Duration of the benchmark (e.g.: 30 mins)


```sh
$ poetry shell

$ locust -f workloads/"$CRDT".py --headless --users $users --spawn-rate 1 -H http://$CRDT_SERVER_IP:8000 --tags "$CRDT_OPERATION" --run-time $RUN_TIME --stop-timeout 99
```

# Contacts

If you are interested in this project or need support to deploy it, please feel free to reach out to [Rogério Pontes](mailto:rogerio.a.pontes@inesctec.pt).
