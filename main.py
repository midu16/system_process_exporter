"""
This is the systemprocess_exporter ephemeral exporter of process cpu, memory and disk usage per process.
"""
__author__ = 'Mihai IDU'

import requests
import time
import psutil,getpass,os
import argparse


def memory_usage_data_payload_command(username):
    """
        This fucntion is similar tomemory_usage_data_payload just enhancing the infromations of the pid.

    :param username:            The username of the user under which the systemprocess_exporter runs.
    :return:                    The retun is a REST-API POST call to the Prometheus-pushgateway endpoint.
    """
    # the newer structure format will be 
    process_dict = {"memory_usage" + "{" + "process=" + '"' + str(proc.name()) + '"' + " , " + "pid=" + '"' + str(
        proc.pid) + '"' + "process_command=" + '"' + str(proc.cmdline()) + '"' + "}": proc.memory_percent(memtype="rss") for proc in psutil.process_iter() if
                    proc.username() == username}
    """
        Make sure that the key is of type str. Is generated as dictionary.
            Make sure that the value is of type float. Is generated as dictionary.
    """
    key = []
    for index in process_dict.keys():
        key.append(str(index))

    value = []
    for index in process_dict.values():
        value.append(str(round(index, 2)))

    data = []
    for index in range(0, len(process_dict.keys())):
        data.append(str(key[index]) + ' ' + str(value[index]) + '\n')
    return data


def memory_usage_data_payload(username):
    """
        This fucntion is building the payload of the post method to the pushgateway-server.

    :param username:            The username of the user under which the systemprocess_exporter runs.
    :return:                    The retun is a REST-API POST call to the Prometheus-pushgateway endpoint.
    """
    process_dict = {"memory_usage" + "{" + "process=" + '"' + str(proc.name()) + '"' + " , " + "pid=" + '"' + str(
        proc.pid) + '"' + "}": proc.memory_percent(memtype="rss") for proc in psutil.process_iter() if
                    proc.username() == username}
    """
        Make sure that the key is of type str. Is generated as dictionary.
            Make sure that the value is of type float. Is generated as dictionary.
    """
    key = []
    for index in process_dict.keys():
        key.append(str(index))

    value = []
    for index in process_dict.values():
        value.append(str(round(index, 2)))

    data = []
    for index in range(0, len(process_dict.keys())):
        data.append(str(key[index]) + ' ' + str(value[index]) + '\n')
    return data

def cpu_usage_data_payload(username):
    """
    :param username:            The username of the user under which the systemprocess_exporter runs.
    :return:                    The cpu_measure data-payload
    """
    process_dict = {"cpu_usage" + "{" + "process=" + '"' + str(proc.name()) + '"' + " , " + "pid=" + '"' + str(
        proc.pid) + '"' + "}": proc.cpu_percent(interval=None) for proc in psutil.process_iter() if
                    proc.username() == username}
    """
        Make sure that the key is of type str. Is generated as dictionary.
            Make sure that the value is of type float. Is generated as dictionary.
    """
    key = []
    for index in process_dict.keys():
        key.append(str(index))

    value = []
    for index in process_dict.values():
        value.append(str(round(index, 2)))

    data = []
    for index in range(0, len(process_dict.keys())):
        data.append(str(key[index]) + ' ' + str(value[index]) + '\n')
    return data

# building the pushgateway_post function
def pushgateway_post(endpoint, data):
    """"
        The function is transporing the payload to the designated endpoint.
    :param endpoint:            Cli custom value of the enpoint. type string. <ip_addr>:<port>
    :param data:                The data-payload to be transporter
    :return:                    The return is a REST-API POST call to the prometheus-pushgateway-server endpoint.
    """
    #curl -X POST -H  "Content-Type: text/plain" --data "$var" http://localhost:9091/metrics/job/top/instance/machine
    url = 'http://'+str(endpoint)+'/metrics/job/top/instance/machine'
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    time.sleep(0.5)
    return requests.post(url, data='%s' % data, headers=headers)

#list to plain text function conversion for better
def fun(data):
    return "".join([str(item) for var in data for item in var])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Viewer, Monitor & Prometheus-PushGateway exporter - Mihai Idu 2021")
    parser.add_argument("-pp", "--prometheus-pushgateway", action="store_true",
                        help="Push the data to the Prometheus pushgateway each second. Using default endpoint http://localhost:9091/metrics/job/top/instance/machine")
    parser.add_argument("-e", "--pushgateway-server-ipaddr", type=str, default="localhost",
                        help="Changing the localhost pudshgateway-server IPaddr. ")
    parser.add_argument("-p", "--pushgateway-server-port", type=str, default="9091",
                        help="Changing the pushgateway-server port.")
    # managing the arguments
    args = parser.parse_args()
    prometheus_pushgateway = args.prometheus_pushgateway
    # changing the IPaddr of  pushgateway-server.
    pushgateway_server_ip_addr = str(args.pushgateway_server_ipaddr)
    # changing the port communication of the default pushgateway-server.
    pushgateway_server_port = str(args.pushgateway_server_port)
    # print the processes for the first time
    while prometheus_pushgateway:
        endpoint_pushgateway = str(pushgateway_server_ip_addr) + ":" + str(pushgateway_server_port)
    # calling the actions
        user_name = getpass.getuser()
        pushgateway_post(endpoint_pushgateway,fun(memory_usage_data_payload(user_name)))
        pushgateway_post(endpoint_pushgateway,fun(cpu_usage_data_payload(user_name)))

