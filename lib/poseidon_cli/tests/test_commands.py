# -*- coding: utf-8 -*-
"""
Created on 18 Jan 2019
@author: Charlie Lewis
"""
from faucetconfgetsetter import FaucetLocalConfGetSetter
from faucetconfgetsetter import get_test_config
from poseidon_cli.commands import Commands
from poseidon_core.helpers.config import Config
from poseidon_core.helpers.endpoint import endpoint_factory


def test_commands():
    commands = Commands(
        config=get_test_config(), faucetconfgetsetter_cl=FaucetLocalConfGetSetter
    )
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    commands.sdnc.endpoints = {}
    commands.sdnc.endpoints[endpoint.name] = endpoint

    commands.what_is("foo")
    commands.history_of("foo")
    commands.acls_of("foo")
    commands.where_is("foo")
    commands.show_devices("foo bar")
    commands.show_devices("all")
    commands.change_devices("foo")
    commands.remove("foo")
    commands.clear_ignored("foo")
    commands.clear_ignored("ignored")
    commands.ignore("foo")
    commands.remove_ignored("foo")

    endpoint2 = endpoint_factory("foo2")
    endpoint2.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    commands.sdnc.endpoints[endpoint2.name] = endpoint2
    commands.what_is("00:00:00:00:00:00")
