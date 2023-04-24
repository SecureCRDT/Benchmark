### Register

 * For the register CRDT, we should have at least he results for the Insert and Query operations as they will have the overhead of sharing and unsharing secrets.
 * The operations of Merge and Propagate don't have much additional computation besides secret reshare in the propagate operation.
 * Expected Result: The Register CRDT MPC should have *at most* 3x more latency than the baseline due to the sharing overhead and additional network communication. However, if the implementation is efficient, this overhead will most likely be lower.
 * Benchmark file: workloads/register.py
 * Performance of operation should not decrease over time, the CRDT performance should not depend on the number of operations


| CRDT     | Operation | PLAINTEXT | CONFIDENTIAL | MPC | Workload |
| -------- |-----------| --------- | ------------ | --- |----------|
| Register | Update    | -         | -            | -   |workloads/register.py|
| Register | Query     | -         | -            | -   |workloads/register.py|
| Register | Merge     | -         | -            | -   |workloads/register.py|
| Register | Propagate | -         | -            | -   |workloads/register.py|


### GCounter

 * Expected Result: The GCounter CRDT MPC should have *at most* 3x more latency than the baseline due to the sharing overhead and additional network communication. However, if the implementation is efficient, this overhead will most likely be lower.
 * Performance of operation should not decrease over time, the CRDT performance should not depend on the number of operations
 * The gcounter workload always increments the counter by 1 to prevent the workload from overflowing the shares in the CRDT players. This may still happen but it's not a problem for the evaluation. 

| CRDT     | Operation | PLAINTEXT | CONFIDENTIAL | MPC | Workload              |
|----------|-----------| --------- | ------------ | --- |-----------------------|
| GCounter | Update    | -         | -            | -   | workloads/gcounter.py |
| GCounter | Query     | -         | -            | -   | workloads/gcounter.py |
| GCounter | Merge     | -         | -            | -   | workloads/gcounter.py |
| GCounter | Propagate | -         | -            | -   | workloads/gcounter.py |


### PNCounter

 * Expected Result: The PNCounter CRDT MPC should have *at most* 3x more latency than the baseline due to the sharing overhead and additional network communication.  Additionally, this CRDT keeps two counters, which means that each replica will have a total of 9 shares, with two shares per player.
 * Performance of operation should not decrease over time, the CRDT performance should not depend on the number of operations
 * The PNCounter workload always increments or decrements the CRDT  the counter by 1. Both operations, increment and decrement should have the same overhead and the latency of the update request should be measured together for both operations.

| CRDT      | Operation        | PLAINTEXT | CONFIDENTIAL | MPC | Workload               |
|-----------|------------------| --------- | ------------ | --- |------------------------|
| PNCounter | Update/Increment | -         | -            | -   | workloads/pncounter.py |
| PNCounter | Update/Decrement | -         | -            | -   | workloads/pncounter.py |
| PNCounter | Query            | -         | -            | -   | workloads/pncounter.py |
| PNCounter | Query            | -         | -            | -   | workloads/pncounter.py |
| PNCounter | Merge            | -         | -            | -   | workloads/pncounter.py |
| Register  | Propagate        | -         | -            | -   | workloads/pncounter.py |


### MaxValue

 * Expected Result: The MaxValue CRDT MPC should have *at most* 3x more latency than the baseline due to the sharing overhead and additional network communication.
 * This Count uses the equality and gte protocols and should have a higher overhead.
 * Performance of operation should not decrease over time, the CRDT performance should not depend on the number of operations
 * Shares should not overflow, thw workload simply generates random values and ask the CRDT to update its value.

| CRDT     | Operation | PLAINTEXT | CONFIDENTIAL | MPC | Workload              |
|----------|-----------| --------- | ------------ | --- |-----------------------|
| MaxValue | Update    | -         | -            | -   | workloads/maxvalue.py |
| MaxValue | Query     | -         | -            | -   | workloads/maxvalue.py |
| MaxValue | Merge     | -         | -            | -   | workloads/maxvalue.py |
| MaxValue | Propagate | -         | -            | -   | workloads/maxvalue.py |


### MinBoundCounter

 * Expected Result: The Minboundcounter CRDT MPC is the most complex CRDT for the evaluation.  
 * The Update operation has three options:
   * increment (Does not require smpc protocols) - Should not have significant overhead
   * decrement (requires smpc protocols) - higher overhead than increment operation
   * transfer (requires smpc protocols) - high overhead than increment, similar to decrement
 * Each Update operation should be benchmarked individual as they will have significant performance differences. We should not aggregate results of the three options as a single update operation
 * The increment benchmarks starts with CRDT at 0 and increments by 1 in each request.
 * The decrement benchmarks starts with CRDT at INT Max value and decrements by 1 in each request. 
 * The transfer benchmarks starts with CRDT at INT Max value and transfer 1 right in each request.

 * Performance of operation should not decrease over time, the CRDT performance should not depend on the number of operations
 * Shares may overfllow if there are too many increments or decrements.

| CRDT             | Operation        | PLAINTEXT | CONFIDENTIAL | MPC | Workload                              |
|------------------|------------------| --------- | ------------ | --- |---------------------------------------|
| MinBoundCounter  | Update/increment | -         | -            | -   | workloads/minboundcounterincrement.py |
| MinBoundCounter  | Update/decrement | -         | -            | -   | workloads/minboundcounterdecrement.py |
| MinBoundCounter  | Update/transfer  | -         | -            | -   | workloads/minboundcountertransfer.py  |
| MinBoundCounter  | Query            | -         | -            | -   | workloads/minboundcounter.py          |
| MinBoundCounter  | Merge            | -         | -            | -   | workloads/minboundcounter.py          |
| MinBoundCounter  | Propagate        | -         | -            | -   | workloads/minboundcounter.py          |



### Set With Leakage

For the CRDT sets with leakage we have to workloads:
 * a workloads that just adds and queries for random values during the benchmark execution. This benchmark should have a high overhead as the set grows in size and multiple equality prtocols are executed. 
 * a workloads that sets up initialy a fixed set size and than just queries for values during the benchmark. The overhead of the operations should not grow over time, and this benchmark will give us an average latency/troughput for query operations of sets of different sizes.


## Workload A - Increasing set over time
| CRDT            | Operation       | PLAINTEXT | CONFIDENTIAL | MPC | Workload                     |
|-----------------|-----------------| --------- | ------------ | --- |------------------------------|
| SetWithLeakage  | Update | -         | -            | -   | workloads/setwithleakage.py  |
| SetWithLeakage  | Query           | -         | -            | -   | workloads/setwithleakage.py |
| SetWithLeakage | Merge           | -         | -            | -   | workloads/setwithleakage.py |
| SetWithLeakage | Propagate       | -         | -            | -   | workloads/setwithleakage.py |

## Workload A - Fixed set size

Tests should be done for logarithm sizes (2^0,..., 2^N) of sets until the overhead is not practical (e.g.: throughput is 1 op/s)

| CRDT            | Operation       | PLAINTEXT | CONFIDENTIAL | MPC | Workload                         |
|-----------------|-----------------| --------- | ------------ | --- |----------------------------------|
| SetWithLeakage  | Query           | -         | -            | -   | workloads/setwithleakagequery.py |



### EverGrowingSet

For the CRDT sets with leakage we have to workloads:
 * a workloads that just adds and queries for random values during the benchmark execution. This benchmark should have a high overhead as the set grows in size and multiple equality prtocols are executed. 
 * a workloads that sets up initially a fixed set size and then just queries for values during the benchmark. The overhead of the operations should not grow over time, and this benchmark will give us an average latency/troughput for query operations of sets of different sizes.
 
 * THis set should have a higher overhead in the query operation than the set with leakage as the set size will be larger.
 * However, the update operation should be more efficient as no protocol is executed.

## Workload A - Increasing set over time

| CRDT            | Operation       | PLAINTEXT | CONFIDENTIAL | MPC | Workload                    |
|-----------------|-----------------| --------- | ------------ | --- |-----------------------------|
| EverGrowingSet  | Update | -         | -            | -   | workloads/evergrowingset.py |
| EverGrowingSet  | Query           | -         | -            | -   | workloads/evergrowingset.py |
| EverGrowingSet | Merge           | -         | -            | -   | workloads/evergrowingset.py |
| EverGrowingSet | Propagate       | -         | -            | -   | workloads/evergrowingset.py |

## Workload A - Fixed set size

Tests should be done for logarithm sizes (2^0,..., 2^N) of sets until the overhead is not practical (e.g.: throughput is 1 op/s)

| CRDT            | Operation       | PLAINTEXT | CONFIDENTIAL | MPC | Workload                         |
|-----------------|-----------------| --------- | ------------ | --- |----------------------------------|
| SetWithLeakage  | Query           | -         | -            | -   | workloads/evergrowingsetquery.py |
