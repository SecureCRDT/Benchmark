import csv
import statistics as stats
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class RunStatsParser(BaseModel):
    Name: str
    Request_Count: Optional[int] = Field(alias="Request Count")
    Failure_Count: Optional[int] = Field(alias="Failure Count")
    Median_Response_Time: Optional[float] = Field(alias="Median Response Time")
    Average_Response_Time: Optional[float] = Field(alias="Average Response Time")
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
    numberofclients: int
    samples: List[RunStats]



class CRDT(BaseModel):
    query: List[Sample]
    update: List[Sample]

    def get_query_troughput(self, nclients:int):
        all_samples = [sample.samples for sample in self.query if sample.numberofclients == nclients][0]
        query_samples = [sample.Throughoput for sample in all_samples if sample.Name == '/api/query']
        return (stats.mean(query_samples), stats.stdev(query_samples))
    
    def get_update_troughput(self, nclients: int):
        all_samples = [
            sample.samples for sample in self.update if sample.numberofclients == nclients][0]

        query_samples = [
            sample.Throughoput for sample in all_samples if 'update' in sample.Name]
        return (stats.mean(query_samples), stats.stdev(query_samples))


class PNCRDT(BaseModel):
    query: List[Sample]
    update: List[Sample]

    def get_query_troughput(self, nclients: int):
        all_samples = [
            sample.samples for sample in self.query if sample.numberofclients == nclients][0]
        query_samples = [
            sample.Throughoput for sample in all_samples if sample.Name == '/api/query']
        return (stats.mean(query_samples), stats.stdev(query_samples))

    def get_update_troughput(self, nclients: int):
        all_samples = [
            sample.samples for sample in self.update if sample.numberofclients == nclients][0]

        query_samples = [
            sample.Throughoput for sample in all_samples if 'update' in sample.Name]
        result = [sum(query_samples[i:i+2])
                  for i in range(0, len(query_samples), 2)]
        return (stats.mean(result), stats.stdev(result))


class BNCRDT(BaseModel):
    query: List[Sample]
    update: List[Sample]

    def get_query_troughput(self, nclients: int):
        all_samples = [
            sample.samples for sample in self.query if sample.numberofclients == nclients][0]
        query_samples = [
            sample.Throughoput for sample in all_samples if sample.Name == '/api/query']
        return (stats.mean(query_samples), stats.stdev(query_samples))

    def get_update_troughput(self, nclients: int):
        all_samples = [
            sample.samples for sample in self.update if sample.numberofclients == nclients][0]

        query_samples = [
            sample.Throughoput for sample in all_samples if 'dec' in sample.Name]
        return (stats.mean(query_samples), stats.stdev(query_samples))
    
class BaselineSystem(BaseModel):
    Register: CRDT = Field(alias="register")
    gcounter: CRDT
    maxvalue: CRDT
    minboundedcounter: BNCRDT
    pncounter: PNCRDT
    

class ConfidentialSystem(BaseModel):
    Register: CRDT = Field(alias="register") 
    gcounter: CRDT
    pncounter: PNCRDT

class SmpcSystem(BaseModel):
    Register: CRDT = Field(alias="register") 
    gcounter: CRDT
    pncounter: PNCRDT
    maxvalue: CRDT
    minboundedcounter: BNCRDT

class Benchmark(BaseModel):
    Baseline: BaselineSystem = Field(alias="BASELINE")
    Confidential: ConfidentialSystem = Field(alias="CONFIDENTIAL")
    Smpc: SmpcSystem = Field(alias="SMPC")

def parse_run_stats(run_stats_file:str):
    sampele_measures = []
    with open(run_stats_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sampele_measures.append(RunStatsParser(**row).dict())
    return sampele_measures



def collect_benchmark_resultsr():
    results_directory_path = Path('results')
    benchmark_results = list(results_directory_path.glob("**/run_stats.csv"))
    result = defaultdict(lambda: defaultdict(lambda:defaultdict(list)))

    for run_stats_file in benchmark_results:
        if "set" in run_stats_file.parts:
            continue
        (_, system, crdt, operation, nclients, _, _) = run_stats_file.parts
        run_stats = parse_run_stats(run_stats_file=run_stats_file)
        sample = {'numberofclients': nclients, "samples": run_stats}
        operation_samples = result[system][crdt][operation]

        if not operation_samples:
            result[system][crdt][operation].append(sample)
            continue
        else:
            for operation_sample in operation_samples:
                if operation_sample['numberofclients'] == nclients:
                    operation_sample['samples'] += run_stats
        
    return result




def calculate_overhead(baseline_value, confidential_value):
    return ((confidential_value-baseline_value)/baseline_value)*100

def print_results(benchmark: Benchmark):
    nclients = 64

    print("CRDT,Operation,Baseline,Stdev,Confidential,Stdev,Smpc, Stdev, Confidential Overhead(%), Confidential Overhead(x), Smpc Overhead(%), Smpc Overhead(x)")

    operations = [("Register", "Query"), ("Register", "Update"),
                  ("gcounter", "Query"), ("gcounter", "Update"),
                  ("pncounter", "Query"), ("pncounter", "Update")
                  ]

    for operation in operations:
        crdt, op = operation

        baseline_thr, baseline_thr_stdev = getattr(getattr(benchmark.Baseline, crdt), f"get_{op.lower()}_troughput")(nclients)
        confidential_thr, confidential_thr_stdev = getattr(getattr(benchmark.Confidential, crdt), f"get_{op.lower()}_troughput")(nclients)
        smpc_thr, smpc_thr_stdev = getattr(
            getattr(benchmark.Smpc, crdt), f"get_{op.lower()}_troughput")(nclients)

        query_overhead = abs(calculate_overhead(baseline_thr, confidential_thr)) # The implementation has x% less troughput than the baseline
        query_overhead_smpc = abs(calculate_overhead(baseline_thr, smpc_thr))

        query_overhead_ntimes = confidential_thr/baseline_thr
        query_overhead_smpc_ntimes = smpc_thr/baseline_thr

        print(f"{crdt},{op},{baseline_thr},{baseline_thr_stdev},{confidential_thr},{confidential_thr_stdev},{smpc_thr},{smpc_thr_stdev},{query_overhead},{query_overhead_ntimes},{query_overhead_smpc},{query_overhead_smpc_ntimes}")
        #print(f"The Confidential {crdt} {op} operation has {query_overhead:.2f}% less troughput than the Baseline.")
        #print(f"The Confidential {crdt} {op} operation has {query_overhead_ntimes:.2f} X less troughput than the Baseline.")

    operations = [("maxvalue", "Query"), ("maxvalue", "Update"),
                  ("minboundedcounter", "Query"), ("minboundedcounter", "Update"),
                  ]
    
    for operation in operations:
        crdt, op = operation
        baseline_query_thr, baseline_query_thr_stdev = getattr(
            getattr(benchmark.Baseline, crdt), f"get_{op.lower()}_troughput")(nclients)
        smpc_thr, smpc_thr_stdev = getattr(
            getattr(benchmark.Smpc, crdt), f"get_{op.lower()}_troughput")(nclients)
        query_overhead_smpc = abs(calculate_overhead(baseline_thr, smpc_thr))
        query_overhead_smpc_ntimes = smpc_thr/baseline_thr

        print(f"{crdt},{op},{baseline_query_thr},{baseline_query_thr_stdev},{smpc_thr},{smpc_thr_stdev},{query_overhead_smpc},{query_overhead_smpc_ntimes}")


if __name__ == '__main__':
    results = collect_benchmark_resultsr()
    benchmark = Benchmark(**results)
    print_results(benchmark)

