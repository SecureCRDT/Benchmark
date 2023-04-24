import csv
import statistics as stats
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
import json

class RunStatsParser(BaseModel):
    Name: str
    Request_Count: Optional[int] = Field(alias="Request Count")
    Failure_Count: Optional[int] = Field(alias="Failure Count")
    Median_Response_Time: Optional[float] = Field(alias="Median Response Time")
    Average_Response_Time: Optional[float] = Field(
        alias="Average Response Time")
    Min_Response_Time: Optional[float] = Field(alias="Min Response Time")
    Max_Response_time: Optional[float] = Field(alias="Max Response Time")
    Throughoput: Optional[float] = Field(alias="Requests/s")
    Failures: Optional[float] = Field(alias="Failures/s")


class RunStats(BaseModel):
    Name: str
    Request_Count: Optional[int]
    Failure_Count: Optional[int]
    Median_Response_Time: Optional[float]
    Average_Response_Time: Optional[float]
    Min_Response_Time: Optional[float]
    Max_Response_time: Optional[float]
    Throughoput: Optional[float]
    Failures: Optional[float]


class Sample(BaseModel):
    setsize: int
    samples: List[RunStats]


class CRDT(BaseModel):
    query: List[Sample]
    update: List[Sample]

    def get_query_troughput(self, setsize: int):
        all_samples = [
            sample.samples for sample in self.query if sample.setsize == setsize][0]
        query_samples = [
            sample.Throughoput for sample in all_samples if '/api/query' in sample.Name]
        return (stats.mean(query_samples), stats.stdev(query_samples))

    def get_update_troughput(self, setsize: int):
        all_samples = [
            sample.samples for sample in self.update if sample.setsize == setsize][0]

        query_samples = [
            sample.Throughoput for sample in all_samples if 'update' in sample.Name]
        return (stats.mean(query_samples), stats.stdev(query_samples))


class BaselineSystem(BaseModel):
    set: CRDT

class ConfidentialSystem(BaseModel):
    set: CRDT

class Benchmark(BaseModel):
    Baseline: BaselineSystem = Field(alias="BASELINE")
    Confidential: ConfidentialSystem = Field(alias="CONFIDENTIAL")


def parse_run_stats(run_stats_file: str):
    sampele_measures = []
    with open(run_stats_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sampele_measures.append(RunStatsParser(**row).dict())
    return sampele_measures


def collect_benchmark_resultsr():
    results_directory_path = Path('results')
    benchmark_results = list(results_directory_path.glob("*/set/**/run_stats.csv"))
    result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for run_stats_file in benchmark_results:
        (_, system, crdt, operation, set_size, _, _, _) = run_stats_file.parts
        run_stats = parse_run_stats(run_stats_file=run_stats_file)
        sample = {'setsize': set_size, "samples": run_stats}
        operation_samples = result[system][crdt][operation]

        exists = False
        for operation_sample in operation_samples:
            if operation_sample['setsize'] == set_size:
                operation_sample['samples'] += run_stats
                exists == True
        
        if not exists:
            result[system][crdt][operation].append(sample)

    return result


def calculate_overhead(baseline_value, confidential_value):
    return ((confidential_value-baseline_value)/baseline_value)*100


def print_results(benchmark: Benchmark):

    print("CRDT,Operation,Set Size,Baseline,Stdev,Confidential,Stdev,Overhead(%),Overhead(x)")

    operations = [("set", "query"), ("set", "update"),
                 ]
    set_sizes = [8,16,32,64]

    for operation in operations:
        for set_size in set_sizes:
            crdt, op = operation

            baseline_thr, baseline_thr_stdev = getattr(
                getattr(benchmark.Baseline, crdt), f"get_{op}_troughput")(set_size)
            confidential_thr, confidential_thr_stdev = getattr(
                getattr(benchmark.Confidential, crdt), f"get_{op}_troughput")(set_size)

            # The implementation has x% less troughput than the baseline
            query_overhead = abs(calculate_overhead(
                baseline_thr, confidential_thr))
            query_overhead_ntimes = confidential_thr/baseline_thr

            print(f"{crdt},{op},{set_size},{baseline_thr},{baseline_thr_stdev},{confidential_thr},{confidential_thr_stdev},{query_overhead},{query_overhead_ntimes}")
            #print(
            #    f"The Confidential {crdt} {op} operation has {query_overhead:.2f}% less troughput than the Baseline.")
            #print(
            #    f"The Confidential {crdt} {op} operation has {query_overhead_ntimes:.2f} X less troughput than the Baseline.")



if __name__ == '__main__':
    results = collect_benchmark_resultsr()
    #print(json.dumps(results,indent=2))
    benchmark = Benchmark(**results)
    #print(benchmark)
    print_results(benchmark)
