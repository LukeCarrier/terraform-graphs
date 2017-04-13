#!/usr/bin/env python

from argparse import ArgumentParser
import re
import sys

import pydotplus

def process(file):
    data = file.read()
    graph = pydotplus.parser.parse_dot_data(data)

    label_re = re.compile(r'(\[(?P<subgraph>\w+)\] )?(?P<resource_type>[\w-]+)\.(?P<resource_name>[\w-]+)(\.(?P<module_resource_type>[\w-]+))?(\.(?P<module_resource_name>[\w-]+))?')

    for label, node in graph.obj_dict['subgraphs']['"root"'][0]['nodes'].items():
        match = label_re.match(label[1:-1])

        if match is None:
            continue

        resource_type = match.group('resource_type')
        resource_name = match.group('resource_name')

        if resource_type == 'module':
            module_name = match.group('resource_name')
            resource_type = match.group('module_resource_type')
            resource_name = match.group('module_resource_name')

        fill_colour = None
        if resource_type == 'azurerm_dns_a_record':
            fill_colour = 'sienna'
        elif resource_type == 'azurerm_dns_zone':
            fill_colour = 'sienna1'
        elif resource_type == 'azurerm_network_interface':
            fill_colour = 'forestgreen'
        elif resource_type == 'azurerm_network_security_group':
            fill_colour = 'orangered'
        elif resource_type == 'azurerm_network_security_rule':
            fill_colour = 'orange'
        elif resource_type == 'azurerm_storage_account':
            fill_colour = 'springgreen'
        elif resource_type == 'azurerm_virtual_machine':
            fill_colour = 'dodgerblue'

        if fill_colour is not None:
            node[0]['attributes']['style']     = '"filled"'
            node[0]['attributes']['fillcolor'] = '"' + fill_colour + '"'

    return graph.to_string()


if __name__ == '__main__':
    parser = ArgumentParser(description='Terraform graph post-processor')
    parser.add_argument('-s', '--source', type=str, required=False, help='Graphviz source file')
    args = parser.parse_args()

    if args.source is not None:
        with open(args.source, 'r') as f:
            print(process(f))
    else:
        print(process(sys.stdin))
