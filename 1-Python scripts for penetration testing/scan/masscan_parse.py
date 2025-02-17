#!/usr/bin/env python
# Copyright (c) 2019, Gouasmia Zakaria
# All rights reserved.


import xml.etree.ElementTree
import sys
import re
import os.path


#------------------------------------
# Object to hold Masscan host items
#------------------------------------
class HostItem():

    def __init__(self, ip):
        self.ip = ip
        self.ports = []

    def __str__(self):
        s  = '{0}\n'.format(self.ip)
        s += '{0}\n'.format('=' * len(self.ip))

        for port in self.ports:
            s += '{0}/{1}: '.format(port[0], port[1])
            if port[2] != '':
                s += 'Service: {0} '.format(port[2])
            if port[3] != '':
                s += 'Banner: {0}'.format(port[3])

        s += '\n'

        return s


def usage():
    print("masscan_parse.py masscan_xml_file")
    sys.exit()


def ip_key(ip):
    """
    Return an IP address as a tuple of ints.

    This function is used to sort IP addresses properly.
    """
    return tuple(int(part) for part in ip.split('.'))


def create_host(address, ports):
    """
    Create a new host object.
    """
    h = HostItem(address)

    for port in ports:
        name, banner = get_service(port.find('service'))
        h.ports.append((int(port.attrib['portid']), port.attrib['protocol'], name, banner))

    return h


def get_service(service):
    """
    Get the service name.

    If the product attribute it set then use it otherwise use the name
    attribute.
    """
    if service is None:
        name = ''
        banner = ''

    else:
        name = service.attrib.get('product', None)
        if name is None:
            name = service.attrib.get('name', '')

        banner = service.attrib.get('banner', '')

    return name, banner


def open_masscan_file(filename):
    """
    Open the given Masscan XML file and load it as an XML object.
    """
    if not os.path.exists(filename):
        print("{0} does not exist.".format(filename))
        sys.exit()

    if not os.path.isfile(filename):
        print("{0} is not a file.".format(filename))
        sys.exit()

    try:
        # Load Masscan XML file into the tree and get the root element.
        nf = xml.etree.ElementTree.ElementTree(file=filename)
        root = nf.getroot()

        # Make sure this is an Masscan XML file
        if root.tag == 'nmaprun' and root.attrib['scanner'] == 'masscan':
            return filename, root
        else:
            print('{0} is not a Masscan XML file.'.format(filename))
            sys.exit()

    except Exception as e:
        print('XML Parse Error: {0}'.format(e))
        sys.exit()


if __name__ == '__main__':
    ##
    # Process program arguments
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == '-h':
        usage()
    else:
        file_name, mscan = open_masscan_file(sys.argv[1])

    ##
    # Find all the host objects in the Masscan file
    hosts = mscan.findall('host')

    ##
    # Process each of the hosts
    for host in hosts:
        address = host.find('address').attrib['addr']
        ports = host.findall('ports/port')

        if ports != []:
            h = create_host(address, ports)
            print(h)

