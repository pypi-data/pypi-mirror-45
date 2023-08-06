#!/usr/bin/env python

from __future__ import absolute_import
import libvirt
from xml.dom import minidom


def get_network_domains(network, uri):
    network_hosts = []
    # conn = libvirt.openReadOnly(uri)
    conn = libvirt.open(uri)
    if conn is None:
        return network_hosts

    hosts = conn.listDomainsID()

    for host in hosts:
        dom = conn.lookupByID(host)
        raw_xml = dom.XMLDesc(0)
        xml = minidom.parseString(raw_xml)
        interfaces = xml.getElementsByTagName('interface')
        usesNetwork = False
        for interface in interfaces:
            usesNetwork = usesNetwork or iterate_interfaces(interface, network)
        if usesNetwork:
            network_hosts.append(dom.name())

    conn.close()
    return network_hosts



def iterate_interfaces(interface, network):
    """
    Returns true if the interface uses the given network

    Otherwise returns false
    """
    if interface.getAttribute('type') != 'network':
        return False
    interfaceNodes = interface.childNodes
    for node in interfaceNodes:
        if node.nodeName != 'source':
            continue
        if 'network' not in list(node.attributes.keys()):
            return False
        if node.attributes['network'].nodeValue == network:
            return True
        return False


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_network_domains': get_network_domains
        }
