# -*- coding: utf-8 -*-
"""
Test module for collector.
@author: Charlie Lewis
"""
from poseidon_core.helpers.collector import Collector
from poseidon_core.helpers.endpoint import endpoint_factory


def test_Collector():
    """
    Tests Collector
    """
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {"mac": "00:00:00:00:00:00"}
    a = Collector(endpoint, "foo")
    a.start_collector()
    a.stop_collector()
    a.get_collectors()
    a.host_has_active_collectors("foo")
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {"mac": "00:00:00:00:00:00", "container_id": "foo"}
    a = Collector(endpoint, "foo")
    a.stop_collector()
