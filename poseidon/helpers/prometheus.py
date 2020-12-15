# -*- coding: utf-8 -*-
"""
Created on 5 December 2018
@author: Charlie Lewis
"""
import datetime
import logging
import socket
from binascii import hexlify
import requests

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Info
from prometheus_client import Summary
from prometheus_client import start_http_server

from poseidon.constants import NO_DATA
from poseidon.helpers.config import Config
from poseidon.helpers.endpoint import EndpointDecoder


class Prometheus():

    def __init__(self):
        self.logger = logging.getLogger('prometheus')
        self.prom_metrics = {}
        self.controller = Config().get_config()
        self.prometheus_addr = self.controller['prometheus_ip'] + ':' + self.controller['prometheus_port']

    def initialize_metrics(self):
        self.prom_metrics['info'] = Info('poseidon_version', 'Info about Poseidon')
        self.prom_metrics['ipv4_table'] = Gauge('poseidon_endpoint_ip_table',
                                                'IP Table',
                                                ['mac',
                                                 'tenant',
                                                 'segment',
                                                 'port',
                                                 'role',
                                                 'ipv4_os',
                                                 'hash_id'])
        self.prom_metrics['roles'] = Gauge('poseidon_endpoint_roles',
                                           'Number of endpoints by role',
                                           ['role'])
        self.prom_metrics['oses'] = Gauge('poseidon_endpoint_oses',
                                          'Number of endpoints by OS',
                                          ['ipv4_os'])
        self.prom_metrics['current_states'] = Gauge('poseidon_endpoint_current_states',
                                                    'Number of endpoints by current state',
                                                    ['current_state'])
        self.prom_metrics['vlans'] = Gauge('poseidon_endpoint_vlans',
                                           'Number of endpoints by VLAN',
                                           ['tenant'])
        self.prom_metrics['port_tenants'] = Gauge('poseidon_endpoint_port_tenants',
                                                  'Number of tenants by port',
                                                  ['port',
                                                   'tenant'])
        self.prom_metrics['port_hosts'] = Gauge('poseidon_endpoint_port_hosts',
                                                'Number of hosts by port',
                                                ['port'])
        self.prom_metrics['last_rabbitmq_routing_key_time'] = Gauge('poseidon_last_rabbitmq_routing_key_time',
                                                                    'Epoch time when last received a RabbitMQ message',
                                                                    ['routing_key'])
        self.prom_metrics['ncapture_count'] = Counter('poseidon_ncapture_count', 'Number of times ncapture ran')
        self.prom_metrics['monitor_runtime_secs'] = Summary('poseidon_monitor_runtime_secs',
                                                            'Time spent in Monitor methods',
                                                            ['method'])
        self.prom_metrics['endpoint_role_confidence_top'] = Gauge('poseidon_role_confidence_top',
                                                                  'Confidence of top role prediction',
                                                                  ['mac',
                                                                   'name',
                                                                   'role',
                                                                   'ipv4_os',
                                                                   'ipv4_address',
                                                                   'ipv6_address',
                                                                   'hash_id'])
        self.prom_metrics['endpoint_role_confidence_second'] = Gauge('poseidon_role_confidence_second',
                                                                  'Confidence of second role prediction',
                                                                  ['mac',
                                                                   'name',
                                                                   'role',
                                                                   'ipv4_os',
                                                                   'ipv4_address',
                                                                   'ipv6_address',
                                                                   'hash_id'])
        self.prom_metrics['endpoint_role_confidence_third'] = Gauge('poseidon_role_confidence_third',
                                                                  'Confidence of third role prediction',
                                                                  ['mac',
                                                                   'name',
                                                                   'role',
                                                                   'ipv4_os',
                                                                   'ipv4_address',
                                                                   'ipv6_address',
                                                                   'hash_id'])
        self.prom_metrics['endpoints'] = Gauge('poseidon_endpoints',
                                               'All endpoints',
                                               ['mac',
                                                'tenant',
                                                'segment',
                                                'ether_vendor',
                                                'controller_type',
                                                'controller',
                                                'name',
                                                'port',
                                                'hash_id'])
        self.prom_metrics['endpoint_state'] = Gauge('poseidon_endpoint_state',
                                                    'State for all endpoints',
                                                    ['mac',
                                                     'tenant',
                                                     'segment',
                                                     'ether_vendor',
                                                     'name',
                                                     'port',
                                                     'state',
                                                     'hash_id'])
        self.prom_metrics['endpoint_os'] = Gauge('poseidon_endpoint_os',
                                                 'Operating System for all endpoints',
                                                 ['mac',
                                                  'tenant',
                                                  'segment',
                                                  'ether_vendor',
                                                  'name',
                                                  'port',
                                                  'ipv4_os',
                                                  'hash_id'])
        self.prom_metrics['endpoint_role'] = Gauge('poseidon_endpoint_role',
                                                 'Top role for all endpoints',
                                                 ['mac',
                                                  'tenant',
                                                  'segment',
                                                  'ether_vendor',
                                                  'name',
                                                  'port',
                                                  'top_role',
                                                  'hash_id'])
        self.prom_metrics['endpoint_ip'] = Gauge('poseidon_endpoint_ip',
                                                 'IP Address for all endpoints',
                                                 ['mac',
                                                  'tenant',
                                                  'segment',
                                                  'ether_vendor',
                                                  'name',
                                                  'port',
                                                  'ipv4_address',
                                                  'ipv6_address',
                                                  'ipv4_subnet',
                                                  'ipv6_subnet',
                                                  'ipv4_rdns',
                                                  'ipv6_rdns',
                                                  'hash_id'])
        self.prom_metrics['endpoint_metadata'] = Gauge('poseidon_endpoint_metadata',
                                                       'Metadata for all endpoints',
                                                       ['mac',
                                                        'tenant',
                                                        'segment',
                                                        'ether_vendor',
                                                        'prev_state',
                                                        'next_state',
                                                        'acls',
                                                        'ignore',
                                                        'ipv4_subnet',
                                                        'ipv6_subnet',
                                                        'ipv4_rdns',
                                                        'ipv6_rdns',
                                                        'controller_type',
                                                        'controller',
                                                        'name',
                                                        'state',
                                                        'port',
                                                        'top_role',
                                                        'ipv4_os',
                                                        'ipv4_address',
                                                        'ipv6_address',
                                                        'hash_id'])

    @staticmethod
    def get_metrics():
        metrics = {'info': {},
                   'roles': {},
                   'oses': {},
                   'current_states': {'known': 0,
                                      'unknown': 0,
                                      'mirroring': 0,
                                      'shutdown': 0,
                                      'queued': 0,
                                      'reinvestigating': 0},
                   'vlans': {},
                   'port_tenants': {},
                   'port_hosts': {},
                   'ncapture_count': 0}
        return metrics

    def update_metrics(self, hosts):

        def ip2int(ip):
            ''' convert ip quad octet string to an int '''
            if not ip or ip in ['None', '::']:
                res = 0
            elif ':' in ip:
                res = int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)
            else:
                o = list(map(int, ip.split('.')))
                res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
            return res

        metrics = Prometheus.get_metrics()

        # get version
        try:
            with open('/poseidon/VERSION', 'r') as f:  # pragma: no cover
                for line in f:
                    metrics['info']['version'] = line.strip()
        except Exception as e:
            print('Unable to get version from the version file')

        for host in hosts:
            if host['role'] in metrics['roles']:
                metrics['roles'][host['role']] += 1
            else:
                metrics['roles'][host['role']] = 1
            if host['ipv4_os'] in metrics['oses']:
                metrics['oses'][host['ipv4_os']] += 1
            else:
                metrics['oses'][host['ipv4_os']] = 1

            if host['state'] in metrics['current_states']:
                metrics['current_states'][host['state']] += 1
            else:
                metrics['current_states'][host['state']] = 1

            if host['tenant'] in metrics['vlans']:
                metrics['vlans'][host['tenant']] += 1
            else:
                metrics['vlans'][host['tenant']] = 1

            if (host['port'], host['tenant']) in metrics['port_tenants']:
                metrics['port_tenants'][(
                    host['port'], host['tenant'])] += 1
            else:
                metrics['port_tenants'][(host['port'], host['tenant'])] = 1

            if host['port'] in metrics['port_hosts']:
                metrics['port_hosts'][host['port']] += 1
            else:
                metrics['port_hosts'][host['port']] = 1

            try:
                self.prom_metrics['ipv4_table'].labels(mac=host['mac'],
                                                       tenant=host['tenant'],
                                                       segment=host['segment'],
                                                       port=host['port'],
                                                       role=host['role'],
                                                       ipv4_os=host['ipv4_os'],
                                                       hash_id=host['id']).set(ip2int(host['ipv4']))
            except Exception as e:  # pragma: no cover
                self.logger.error(
                    'Unable to send {0} results to prometheus because {1}'.format(host, str(e)))

        try:
            for role in metrics['roles']:
                self.prom_metrics['roles'].labels(role=role).set(metrics['roles'][role])
            for os_t in metrics['oses']:
                self.prom_metrics['oses'].labels(ipv4_os=os_t).set(metrics['oses'][os_t])
            for current_state in metrics['current_states']:
                self.prom_metrics['current_states'].labels(current_state=current_state).set(metrics['current_states'][current_state])
            for vlan in metrics['vlans']:
                self.prom_metrics['vlans'].labels(tenant=vlan).set(metrics['vlans'][vlan])
            for port_tenant in metrics['port_tenants']:
                self.prom_metrics['port_tenants'].labels(port=port_tenant[0],
                                                         tenant=port_tenant[1]).set(metrics['port_tenants'][port_tenant])
            for port_host in metrics['port_hosts']:
                self.prom_metrics['port_hosts'].labels(
                    port=port_host).set(metrics['port_hosts'][port_host])
            self.prom_metrics['info'].info(metrics['info'])
        except Exception as e:  # pragma: no cover
            self.logger.error(
                'Unable to send results to prometheus because {0}'.format(str(e)))

    def prom_query(self, var, start_time_str, end_time_str, step='30s'):
        payload = {'query': var, 'start': start_time_str, 'end': end_time_str, 'step': step}
        try:
            response = requests.get('http://%s/api/v1/query_range' % self.prometheus_addr, params=payload)
            return response.json()['data']['result']
        except Exception:
            return None

    def latest_metric(self, metric):
        return metric['values'][-1]

    def latest_value(self, metric):
        return float(self.latest_metric(metric)[1])

    def latest_timestamp(self, metric):
        return self.latest_metric(metric)[0]

    def metric_label(self, metric, label, default_value=NO_DATA):
        return metric['metric'].get(label, default_value)

    def scrape_prom(self):
        current_time = datetime.datetime.utcnow()
        # 6 hours in the past and 2 hours in the future
        start_time = current_time - datetime.timedelta(hours=6)
        end_time = current_time + datetime.timedelta(hours=2)
        start_time_str = start_time.isoformat()[:-4]+"Z"
        end_time_str = end_time.isoformat()[:-4]+"Z"
        mr = self.prom_query('poseidon_endpoint_metadata', start_time_str, end_time_str)
        r1 = self.prom_query('poseidon_role_confidence_top', start_time_str, end_time_str)
        r2 = self.prom_query('poseidon_role_confidence_second', start_time_str, end_time_str)
        r3 = self.prom_query('poseidon_role_confidence_third', start_time_str, end_time_str)

        hashes = {}
        role_hashes = {}
        if r1:
            for metric in r1:
                hash_id = self.metric_label(metric, 'hash_id')
                if not hash_id in role_hashes:
                    role_hashes[hash_id] = {
                        'mac': self.metric_label(metric, 'mac'),
                        'ipv4_address': self.metric_label(metric, 'ipv4_address', ''),
                        'ipv4_os': self.metric_label(metric, 'ipv4_os'),
                        'timestamp': str(self.latest_timestamp(metric)),
                        'top_role': self.metric_label(metric, 'role'),
                        'top_confidence': self.latest_value(metric)}
        if r2:
            for metric in r2:
                hash_id = self.metric_label(metric, 'hash_id')
                if hash_id in role_hashes:
                    role_hashes[hash_id]['second_role'] = self.metric_label(metric, 'role')
                    role_hashes[hash_id]['second_confidence'] = self.latest_value(metric)
        if r3:
            for metric in r3:
                hash_id = self.metric_label(metric, 'hash_id')
                if hash_id in role_hashes:
                    role_hashes[hash_id]['third_role'] = self.metric_label(metric, 'role')
                    role_hashes[hash_id]['third_confidence'] = self.latest_value(metric)
        if mr:
            for metric in mr:
                latest = self.latest_value(metric)
                hash_id = self.metric_label(metric, 'hash_id')
                if hash_id in hashes:
                    if latest > hashes[hash_id]['latest']:
                        hashes[hash_id] = metric['metric']
                        hashes[hash_id]['latest'] = latest
                else:
                    hashes[hash_id] = metric['metric']
                    hashes[hash_id]['latest'] = latest
        return hashes, role_hashes

    def get_stored_endpoints(self):
        ''' load existing endpoints from Prometheus. '''
        endpoints = {}
        hashes, role_hashes = self.scrape_prom()
        # format hash metrics into endpoints
        for h in hashes:
            p_endpoint = hashes[h]
            p_endpoint.update({
                'name': p_endpoint['hash_id'],
                'p_next_state': p_endpoint.get('next_state', None),
                'p_prev_state': p_endpoint.get('prev_state', None),
                'acl_data': [],  # TODO: acl_data
                'metadata': {'mac_addresses': {}, 'ipv4_addresses': {}, 'ipv6_addresses': {}},
                'endpoint_data': {
                    'mac': p_endpoint['mac'],
                    'segment': p_endpoint['segment'],
                    'port': p_endpoint['port'],
                    'vlan': p_endpoint['tenant'],
                    'tenant': p_endpoint['tenant'],
                    'ipv4': p_endpoint.get('ipv4_address', ''),
                    'ipv6': p_endpoint.get('ipv6_address', ''),
                    'controller_type': p_endpoint['controller_type'],
                    'controller': p_endpoint.get('controller', ''),
                    'name': p_endpoint['name'],
                    'ether_vendor': p_endpoint['ether_vendor'],
                    'ipv4_subnet': p_endpoint.get('ipv4_subnet', ''),
                    'ipv4_rdns': p_endpoint.get('ipv4_rdns', ''),
                    'ipv6_rdns': p_endpoint.get('ipv6_rdns', ''),
                    'ipv6_subnet': p_endpoint.get('ipv6_subnet', '')}})
            mac = p_endpoint['mac']
            for role_hash in role_hashes.values():
                role_mac = role_hash['mac']
                if mac != role_mac:
                    continue
                if not mac in p_endpoint['metadata']['mac_addresses']:
                    roles = [role_hash['top_role'], role_hash['second_role'], role_hash['third_role']]
                    confidences = [role_hash['top_confidence'], role_hash['second_confidence'], role_hash['third_confidence']]
                    p_endpoint['metadata']['mac_addresses'][mac] = {
                        'classification': {
                            'labels': roles,
                            'confidences': confidences,
                         },
                        'pcap_labels': ''}
                ipv4 = role_hash['ipv4_address']
                if not ipv4 in p_endpoint['metadata']['ipv4_addresses']:
                    p_endpoint['metadata']['ipv4_addresses'][ipv4] = {'short_os': role_hash['ipv4_os']}
            endpoint = EndpointDecoder(p_endpoint).get_endpoint()
            endpoints[endpoint.name] = endpoint
        return endpoints

    @staticmethod
    def start(port=9304):
        start_http_server(port)
