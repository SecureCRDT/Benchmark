#!/bin/bash

# Constants
RUN_TIME=1m # minutes

# CRDTs to test
CRDT_SET=('register' 'gcounter' 'pncounter' 'maxvalue' 'minboundedcounter')

# CRDT operations to test
CRDT_OPERATION_SET=('update' 'query')

# Systems to test
SYSTEMS=(SMPC)

# Number of concurrent users
NUMBER_OF_USERS=(6)


start_cluster() {
  local crdt=$1
  
  ssh bportela@cop02.dcc.fc.up.pt "cd SecureCRDT; java -cp target/SecureCRDT-1.0.jar pt.uporto.dcc.securecrdt.crdt.CrdtPlayer 0 local" &
  ssh bportela@cop03.dcc.fc.up.pt "cd SecureCRDT; java -cp target/SecureCRDT-1.0.jar pt.uporto.dcc.securecrdt.crdt.CrdtPlayer 1 local" &
  ssh bportela@cop04.dcc.fc.up.pt "cd SecureCRDT; java -cp target/SecureCRDT-1.0.jar pt.uporto.dcc.securecrdt.crdt.CrdtPlayer 2 local" &
  
  java -cp SecureCRDT/target/SecureCRDT-1.0.jar pt.uporto.dcc.securecrdt.client.Client $crdt &
}

run_tests() {
  local system=$1
  local crdt=$2
  local crdt_operation=$3
  local user_count=$4
  local run_number=$5

  # Start the cluster
  start_cluster "$crdt"

  # Wait for the cluster to start
  sleep 20

  # Calculate the number of users
  local users=$((2 ** $user_count))

  # Create results directory
  local results_path="results/$system/$crdt/$crdt_operation/$users/$run_number/"
  mkdir -p benchmark/"$results_path"

  # Run the benchmark
  cd benchmark
  locust -f workloads/"$crdt".py --headless --users $users --spawn-rate 1 -H http://192.168.70.17:8000 --tags "$crdt_operation" --run-time $RUN_TIME --stop-timeout 99 --csv="$results_path/run" > locust_log.txt
  cd ..

  # Close the cluster
  curl -X GET http://192.168.70.17:8000/api/exit
  sleep 10
  ssh bportela@cop02.dcc.fc.up.pt "pkill java; pkill java"
  ssh bportela@cop03.dcc.fc.up.pt "pkill java; pkill java"
  ssh bportela@cop04.dcc.fc.up.pt "pkill java; pkill java"

  sleep 60
}

for SYSTEM in "${SYSTEMS[@]}"
do
  for CRDT in "${CRDT_SET[@]}"
  do
    for CRDT_OPERATION in "${CRDT_OPERATION_SET[@]}"
    do
      for USER_COUNT in "${NUMBER_OF_USERS[@]}"
      do
        for RUN_NUMBER in {1..3}
        do
        
          run_tests "$SYSTEM" "$CRDT" "$CRDT_OPERATION" "$USER_COUNT" "$RUN_NUMBER"
        
        done
      done
    done
  done
done
