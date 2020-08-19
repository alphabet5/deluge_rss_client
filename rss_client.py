# Built-in modules
import xml.etree.ElementTree as ET
from datetime import datetime
import re

from time import sleep
#import pickle

# 3rd party modules
import requests
import netmiko


def parse_arguments(arguments_yaml_file='arguments.yaml'):
    import yaml
    import argparse
    from pydoc import locate
    import sys
    with open(arguments_yaml_file, 'r') as y:
        data = yaml.load(y, Loader=yaml.FullLoader)
        parser = argparse.ArgumentParser()
        for argument, parameters in data.items():
            if 'type' in parameters.keys():
                parameters['type'] = locate(parameters['type'])
            if 'required' in parameters.keys():
                if type(parameters['required']) == str:
                    parameters['required'] = exec(parameters['required'])
            parser.add_argument('--' + argument, **parameters)
        return parser.parse_args()


def p_xml(element):
    if len(element) > 0:
        return_dict = dict()
        for x in element:
            if x.tag in return_dict:
                if type(return_dict[x.tag]) != list:
                    return_dict[x.tag] = [return_dict[x.tag]]
                return_dict[x.tag].append(p_xml(x))
            else:
                return_dict[x.tag] = p_xml(x)
        return return_dict
    else:
        return element.text

import subprocess
if __name__ == '__main__':
    args = vars(parse_arguments('arguments.yaml'))

    PARAMS = dict()
    r = requests.get(url=args['url'], params=PARAMS)

    last_run = datetime(2000, 1, 1) #pickle.load(open('last_run.db', 'rb'))
    element_tree = ET.fromstring(r.content)
    elements = p_xml(element_tree)
    first_item = True
    for item in elements['channel']['item']:
        if datetime.strptime(re.match('.*?\d{1,2}\s.*?\s\d{4}\s\d{2}:\d{2}:\d{2}', item['pubDate']).group(), '%a, %d %b %Y %H:%M:%S') > last_run:
            print(item['title'])
            command = 'deluge-console -d 192.168.3.98 -p 58846 -U localclient -P 0621b9144fbc4703a6dde4f9f641bcf35164e8e5 add "' + item['link'] + '"'
            subprocess.call(command, shell=True)

    # if 'remote' in args:
    #     conn = netmiko.ConnectHandler(device_type='terminal_server', ip=args['remote'],
    #                                   username=args['username'], password=args['password'])
    #     result = conn.send_command(command)
    #     print(result)
    # else:
    #pickle.dump(datetime.now(), open('last_run.db', 'wb'))
