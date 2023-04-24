 

 # Start a poetry shell


 ```sh
 $ poetry shell
 ```

## Parse Results

```sh
python results/parse_results.py
```

# Run a single benchmark

 locust -f workloads/register.py --users 1 --spawn-rate 1 -H http://localhost:8000 --tags update --run-time 10m --stop-timeout 99
