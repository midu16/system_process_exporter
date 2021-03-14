# Linux system process monitoring and exporter to Prometheus and Grafana
Prometheus systemprocess_exporter 


### TravisCI
[![Build Status](https://travis-ci.com/midu16/systemprocess_exporter.svg?branch=master)](https://travis-ci.com/midu16/systemprocess_exporter)

### Solution Architecture

![LLD Solution Architecture](https://github.com/midu16/system_process_pushgateway/blob/master/documentation/Untitled%20Diagram.png)

The transmission interval of the data for the interface ```(1)``` is each second.
The data flow is from the ```systemprocess_exporter``` towards ```pushgateway```, triggered by the ```POST```method sent by ```systemprocess_exporter```.

The transmission interval of the data for the interface ```(2)``` is dependent by the ```scrape_interval``` parameter set into the ```prometheus.yml```. The data flow is from the ```pushgateway``` towards ```prometheus```, triggered by the ```GET```method request from ```prometheus```. 

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
The following picture is presenting a set of data samples results for *java* process:
![Grafana results](https://github.com/midu16/systemprocess_exporter/blob/master/documentation/Screenshot_2021-03-10%20SystemProcess%20Usage%20-%20Grafana.png)

![Grafana results1](https://github.com/midu16/systemprocess_exporter/blob/4c4da95f404c821853733caf05b92830fb26dbd5/documentation/Screenshot_2021-03-14%20SystemProcess%20Usage%20-%20Grafana.png)

### Testing capabilities
```
$ sudo yum install stress
$ stress --cpu 4 --io 3 --vm 2 --vm-bytes 20G --timeout 20s
```
### Progress
* [x] Building the export functions
* [x] Exporting data to ```pushgateway```
* [x] Supporting host resolution into the push-url
* [x] Supporting data export from the ```systemprocess_exporter``` to ```pushgateway``` with 1second resolution
* [x] Improving the CPU usage performance of the ```systemprocess_exporter```. Lower the consumption of the CPU < 10%
* [ ] Adding complete_process_command to the data payload of the push 
* [x] Generic Grafana dashboard
* [ ] Supporting the ```{process_name:pid:io_counters}``` statistics
* [ ] Defining Prometheus-alertmanager alarm thresholds
* [ ] Building .rpm package


### Documentation

[1] https://psutil.readthedocs.io/en/latest/#psutil.Process.name

[2] https://docs.pytest.org/en/stable/
