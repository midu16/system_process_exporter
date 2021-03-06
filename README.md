# Linux system process monitoring and exporter to Prometheus and Grafana
Prometheus pushgateway systemprocess 


### Solution Architecture

![LLD Solution Architecture](https://github.com/midu16/system_process_pushgateway/blob/master/documentation/Untitled%20Diagram.png)

### Introduction to the cli
```
midu@localhost $ python3 main.py -h       
usage: main.py [-h] [-c COLUMNS] [-s SORT_BY] [--descending] [-n N] [-u] [-p] [-e]

Process Viewer, Monitor & Prometheus-PushGateway exporter - Mihai Idu 2021

optional arguments:
  -h, --help            show this help message and exit
  -c COLUMNS, --columns COLUMNS
                        Columns to show, available are name,create_time,cores,cpu_usage,status,nice,memory_usage,read_bytes,write_bytes,n_threads,username. Default is
                        name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores.
  -s SORT_BY, --sort-by SORT_BY
                        Column to sort by, default is memory_usage .
  --descending          Whether to sort in descending order.
  -n N                  Number of processes to show, will show all if 0 is specified, default is 25 .
  -u, --live-update     Whether to keep the program on and updating process information each second
  -p, --prometheus-pushgateway
                        Push the data to the Prometheus pushgateway each second. Using default endpoint http://localhost:9091/metrics/job/top/instance/machine
  -e, --endpoint-pushgateway
                        Changing the default endpoint of pushgateway.
```

### Building the binary application and packaging 

- Manual build the application using the ````pyinstall````:
        
    ```
    $ pyinstaller --onefile main.py
    ```

- Using travis-ci :
    
    ```
  .travis.yml
  ```
  
### Grafana dashboard results
