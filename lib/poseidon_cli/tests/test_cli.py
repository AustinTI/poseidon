# -*- coding: utf-8 -*-
"""
Created on 14 Jan 2019
@author: Charlie Lewis
"""
from poseidon_cli.cli import GetData
from poseidon_cli.cli import Parser
from poseidon_cli.cli import PoseidonShell
from poseidon_core.constants import NO_DATA
from poseidon_core.helpers.endpoint import endpoint_factory


def test_poseidonshell():
    shell = PoseidonShell()
    shell.do_help("foo")
    shell.do_help("")
    shell.do_show("foo")
    shell.do_show("all")
    shell.do_show("history 10")
    shell.do_show("history")
    shell.do_show("role")
    shell.do_show("role developer-workstation")
    shell.do_show("")
    shell.do_task("foo")
    shell.do_task("")
    shell.do_task("clear")
    shell.do_task("clear 10")
    shell.do_quit("foo")
    shell.do_exit("foo")
    shell.complete_show("foo", "foo bar", 1, 1)
    shell.complete_task("foo", "foo bar", 1, 1)
    shell.show_all("foo", [])
    shell.show_role("foo", [])
    shell.show_state("foo", [])
    shell.show_acls("foo", [])
    shell.show_os("foo", [])
    shell.show_what("foo", [])
    shell.show_history("foo", [])
    shell.show_where("foo", [])
    shell.show_version("foo", [])
    shell.help_show()
    shell.show_authors("foo", [])
    shell.task_set("foo", [])
    shell.task_collect("foo", [])
    shell.task_ignore("foo", [])
    shell.task_clear("foo", [])
    shell.task_remove("foo", [])
    shell.task_remove("ignored", [])
    shell.help_task()
    shell.emptyline()
    shell.do_shell("ls")
    shell.do_set("echo foo")
    shell.do_set("foo")


def test_check_flags():
    parser = Parser()
    (
        valid,
        fields,
        sort_by,
        max_width,
        unique,
        nonzero,
        output_format,
        ipv4_only,
        ipv6_only,
        ipv4_and_ipv6,
    ) = parser._check_flags({"fields": "all"}, "")
    assert fields == [
        "ID",
        "MAC Address",
        "Switch",
        "Port",
        "VLAN",
        "IPv4",
        "IPv4 Subnet",
        "IPv6",
        "IPv6 Subnet",
        "Ethernet Vendor",
        "Ignored",
        "State",
        "Next State",
        "First Seen",
        "Last Seen",
        "Previous States",
        "IPv4 OS\n(p0f)",
        "IPv6 OS\n(p0f)",
        "Previous IPv4 OSes\n(p0f)",
        "Previous IPv6 OSes\n(p0f)",
        "Role\n(NetworkML)",
        "Role Confidence\n(NetworkML)",
        "Previous Roles\n(NetworkML)",
        "Previous Role Confidences\n(NetworkML)",
        "IPv4 rDNS",
        "IPv6 rDNS",
        "SDN Controller Type",
        "SDN Controller URI",
        "History",
        "ACL History",
        "Pcap labels",
    ]
    expected_fields = ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"]
    (
        valid,
        fields,
        sort_by,
        max_width,
        unique,
        nonzero,
        output_format,
        ipv4_only,
        ipv6_only,
        ipv4_and_ipv6,
    ) = parser._check_flags(
        {
            "fields": expected_fields,
            "sort_by": 1,
            "max_width": 100,
            "unique": True,
            "nonzero": True,
            "output_format": "csv",
            "4": True,
            "6": True,
            "4and6": True,
        },
        "",
    )
    assert fields == expected_fields
    assert sort_by == 1
    assert max_width == 100
    assert unique == True
    assert nonzero == True
    assert output_format == "csv"
    assert ipv4_only == False
    assert ipv6_only == False
    assert ipv4_and_ipv6 == True


def test_display_results():
    parser = Parser()
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "vlan": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv6": "1212::1",
    }
    endpoints = [endpoint]
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4", "IPv6"],
        ipv4_only=False,
        ipv6_only=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv6"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
        unique=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
        nonzero=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
        nonzero=True,
        unique=True,
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
        nonzero=True,
        unique=True,
        output_format="csv",
    )
    parser.display_results(
        endpoints,
        ["ID", "MAC Address", "Switch", "Port", "VLAN", "IPv4"],
        ipv4_only=False,
        ipv4_and_ipv6=True,
        nonzero=True,
        unique=True,
        output_format="json",
    )


def test_get_flags():
    parser = Parser()
    valid, flags, not_flags = parser.get_flags(
        "show all --fields=[id, mac] --sort_by=2 -4 --output_format=csv"
    )
    assert flags == {
        "fields": ["id", "mac"],
        "sort_by": "2",
        "4": True,
        "output_format": "csv",
    }
    assert not_flags == "show all"


def test_completion():
    parser = Parser()
    words = parser.completion("this is a test", "this is a test", ["this"])
    assert words == []


def test_display_ip():
    parser = Parser()
    fields = ["foo", "bar", "IPv4", "IPv6"]
    assert ["foo", "bar", "IPv4"] == parser.display_ip_filter(
        fields, True, False, False
    )
    assert ["foo", "bar", "IPv6"] == parser.display_ip_filter(
        fields, False, True, False
    )
    assert fields == parser.display_ip_filter(fields, False, False, True)


def test_get_name():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    name = GetData._get_name(endpoint)
    assert name == "foo"


def test_get_mac():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    mac = GetData._get_mac(endpoint)
    assert mac == "00:00:00:00:00:00"


def test_get_switch():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    switch = GetData._get_switch(endpoint)
    assert switch == "foo"


def test_get_port():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    port = GetData._get_port(endpoint)
    assert port == "1"


def test_get_vlan():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "vlan": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    vlan = GetData._get_vlan(endpoint)
    assert vlan == "foo"


def test_get_controller():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "controller": "foo",
    }
    controller = GetData._get_controller(endpoint)
    assert controller == "foo"
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    controller = GetData._get_controller(endpoint)
    assert controller == NO_DATA


def test_get_controller_type():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "controller_type": "foo",
    }
    controller_type = GetData._get_controller_type(endpoint)
    assert controller_type == "foo"
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    controller_type = GetData._get_controller_type(endpoint)
    assert controller_type == NO_DATA


def test_get_acls():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
    }
    endpoint.acl_data = []
    acls = GetData._get_acls(endpoint)
    assert acls == "[]"


def test_get_ipv4():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
    }
    ipv4 = GetData._get_ipv4(endpoint)
    assert ipv4 == "0.0.0.0"


def test_get_ipv6():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv6": "1212::1",
    }
    ipv6 = GetData._get_ipv6(endpoint)
    assert ipv6 == "1212::1"


def test_get_ipv4_subnet():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
    }
    ipv4_subnet = GetData._get_ipv4_subnet(endpoint)
    assert ipv4_subnet == NO_DATA
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ipv4_subnet = GetData._get_ipv4_subnet(endpoint)
    assert ipv4_subnet == "0.0.0.0/24"


def test_get_ipv6_subnet():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv6": "1212::1",
    }
    ipv6_subnet = GetData._get_ipv6_subnet(endpoint)
    assert ipv6_subnet == NO_DATA
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv6": "1212::1",
        "ipv6_subnet": "1212::1/64",
    }
    ipv6_subnet = GetData._get_ipv6_subnet(endpoint)
    assert ipv6_subnet == "1212::1/64"


def test_get_ether_vendor():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ether_vendor = GetData._get_ether_vendor(endpoint)
    assert ether_vendor == NO_DATA
    endpoint.endpoint_data = {
        "ether_vendor": "VENDOR",
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ether_vendor = GetData._get_ether_vendor(endpoint)
    assert ether_vendor == "VENDOR"


def test_get_ipv4_rdns():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ipv4_rdns = GetData._get_ipv4_rdns(endpoint)
    assert ipv4_rdns == NO_DATA
    endpoint.endpoint_data = {
        "ipv4_rdns": "foo.internal",
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ipv4_rdns = GetData._get_ipv4_rdns(endpoint)
    assert ipv4_rdns == "foo.internal"


def test_get_ipv6_rdns():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ipv6_rdns = GetData._get_ipv6_rdns(endpoint)
    assert ipv6_rdns == NO_DATA
    endpoint.endpoint_data = {
        "ipv6_rdns": "foo.internal",
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
        "ipv4_subnet": "0.0.0.0/24",
    }
    ipv6_rdns = GetData._get_ipv6_rdns(endpoint)
    assert ipv6_rdns == "foo.internal"


def test_get_ignored():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    ignored = GetData._get_ignored(endpoint)
    assert ignored == "False"


def test_get_state():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    state = GetData._get_state(endpoint)
    assert state == "unknown"


def test_get_next_state():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    state = GetData._get_next_state(endpoint)
    assert state == "None"


def test_get_first_seen():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.unknown()
    GetData._get_first_seen(endpoint)


def test_get_last_seen():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.unknown()
    GetData._get_last_seen(endpoint)


def test_get_prev_state():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.p_prev_state = None
    prev_state = GetData._get_prev_state(endpoint)
    assert prev_state == None
    endpoint.unknown()
    GetData._get_prev_state(endpoint)
    endpoint.queue()
    GetData._get_prev_state(endpoint)


def test_get_history():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    history = GetData._get_history(endpoint)
    assert history == "No history recorded yet."


def test_get_ipv4_os():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv4": "0.0.0.0",
    }
    endpoint.metadata = {"ipv4_addresses": {}}
    ipv4_os = GetData._get_ipv4_os(endpoint)
    assert ipv4_os == NO_DATA
    endpoint.metadata = {"ipv4_addresses": {"0.0.0.0": {"short_os": "foo"}}}
    ipv4_os = GetData._get_ipv4_os(endpoint)
    assert ipv4_os == "foo"


def test_get_ipv6_os():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
        "ipv6": "1212::1",
    }
    endpoint.metadata = {"ipv6_addresses": {}}
    ipv6_os = GetData._get_ipv6_os(endpoint)
    assert ipv6_os == NO_DATA
    endpoint.metadata = {"ipv6_addresses": {"1212::1": {"short_os": "foo"}}}
    ipv6_os = GetData._get_ipv6_os(endpoint)
    assert ipv6_os == "foo"


def test_get_pcap_labels():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.metadata = {"mac_addresses": {}}
    pcap_labels = GetData._get_pcap_labels(endpoint)
    assert pcap_labels == NO_DATA
    endpoint.metadata = {"mac_addresses": {"00:00:00:00:00:00": {"pcap_labels": "foo"}}}
    pcap_labels = GetData._get_pcap_labels(endpoint)
    assert pcap_labels == "foo"


def test_get_role():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.metadata = {"mac_addresses": {}}
    role = GetData._get_role(endpoint)
    assert role == NO_DATA
    endpoint.metadata = {
        "mac_addresses": {
            "00:00:00:00:00:00": {"classification": {"labels": ["foo", "bar", "baz"]}}
        }
    }
    role = GetData._get_role(endpoint)
    assert role == "foo"


def test_get_role_confidence():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    endpoint.metadata = {"mac_addresses": {}}
    confidence = GetData._get_role_confidence(endpoint)
    assert confidence == "0"
    endpoint.metadata = {
        "mac_addresses": {
            "00:00:00:00:00:00": {"classification": {"confidences": [10.0, 9.0, 8.0]}}
        }
    }
    confidence = GetData._get_role_confidence(endpoint)
    assert confidence == "10.0"


def test_get_prev_roles():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    GetData._get_prev_roles(endpoint)


def test_get_prev_role_confidences():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    GetData._get_prev_role_confidences(endpoint)


def test_get_prev_ipv4_oses():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    GetData._get_prev_ipv4_oses(endpoint)


def test_get_prev_ipv6_oses():
    endpoint = endpoint_factory("foo")
    endpoint.endpoint_data = {
        "tenant": "foo",
        "mac": "00:00:00:00:00:00",
        "segment": "foo",
        "port": "1",
    }
    GetData._get_prev_ipv6_oses(endpoint)
