#!/bin/bash

# Constants
RUN_TIME=30m # minutes

# CRDT operations to test
CRDT_OPERATION_SET=('update' 'query')

# Systems to test
SYSTEMS=(BASELINE CONFIDENTIAL)

# Number of concurrent users
NUMBER_OF_USERS=(6)

SET_SIZE=(8 16 32 6)


start_cluster() {
  local system=$1
  local crdt=$2

  if [ "$system" == "BASELINE" ]; then
    ssh bportela@cop02.dcc.fc.up.pt "cd UnsecureCRDT; java -cp target/UnsecureCRDT-1.0.jar pt.uporto.dcc.unsecurecrdt.crdt.CrdtPlayer local" &
    ssh bportela@cop02.dcc.fc.up.pt "cd UnsecureCRDT; java -cp target/UnsecureCRDT-1.0.jar pt.uporto.dcc.unsecurecrdt.proxy.ProxyServer $crdt local" &
  elif [ "$system" == "CONFIDENTIAL" ]; then
    ssh bportela@cop02.dcc.fc.up.pt "cd ConfidentialCRDT; java -cp target/UnsecureCRDT-1.0.jar pt.uporto.dcc.unsecurecrdt.crdt.CrdtPlayer local" &
    ssh bportela@cop02.dcc.fc.up.pt "cd ConfidentialCRDT; java -cp target/UnsecureCRDT-1.0.jar pt.uporto.dcc.unsecurecrdt.proxy.ProxyServer $crdt local" &
  fi
}

run_tests() {
  local system=$1
  local size=$2
  local crdt_operation=$3
  local user_count=$4
  local run_number=$5

  # Start the cluster
  start_cluster "$system" "set"

  # Wait for the cluster to start
  sleep 10

  # Calculate the number of users
  local users=$((2 ** $user_count))

  # Create results directory
  local results_path="results/$system/$crdt/$crdt_operation/$size/$users/$run_number/"
  mkdir -p benchmark/"$results_path"

  # Run the benchmark
  cd benchmark

  export SET_SIZE="$size"
  
  locust -f workloads/set.py --headless --users $users --spawn-rate 1 -H http://192.168.70.17:8000 --tags "$crdt_operation" --run-time $RUN_TIME --stop-timeout 99 --csv="$results_path/run" > locust_log.txt
  cd ..

  # Close the cluster
  curl -X GET http://192.168.70.17:8000/api/exit
  sleep 10
  ssh bportela@cop02.dcc.fc.up.pt "pkill java; pkill java"
  sleep 60
}

for SYSTEM in "${SYSTEMS[@]}"
do
  for SIZE in "${SET_SIZE[@]}"
  do
    for CRDT_OPERATION in "${CRDT_OPERATION_SET[@]}"
    do
      for USER_COUNT in "${NUMBER_OF_USERS[@]}"
      do
        for RUN_NUMBER in {1..3}
        do
        
          run_tests "$SYSTEM" "$SIZE" "$CRDT_OPERATION" "$USER_COUNT" "$RUN_NUMBER"
        
        done
      done
    done
  done
done
