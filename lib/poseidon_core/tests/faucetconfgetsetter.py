from poseidon_core.controllers.faucet.config import FaucetRemoteConfGetSetter
from poseidon_core.controllers.sdnconnect import SDNConnect
from poseidon_core.helpers.config import Config
from poseidon_core.helpers.config import yaml_in
from poseidon_core.helpers.config import yaml_out
from poseidon_core.helpers.prometheus import Prometheus


class FaucetLocalConfGetSetter(FaucetRemoteConfGetSetter):
    def __init__(self, **_kwargs):
        self.faucet_conf = {}

    @staticmethod
    def config_file_path(config_file):
        return config_file

    def read_faucet_conf(self, config_file):
        if not config_file:
            config_file = self.DEFAULT_CONFIG_FILE
        faucet_conf = yaml_in(config_file)
        if isinstance(faucet_conf, dict):
            self.faucet_conf = faucet_conf
        return self.faucet_conf

    def write_faucet_conf(self, config_file=None, faucet_conf=None):
        if not config_file:
            config_file = self.DEFAULT_CONFIG_FILE
        if faucet_conf is None:
            faucet_conf = self.faucet_conf
        self.faucet_conf = faucet_conf
        return yaml_out(config_file, self.faucet_conf)

    def set_port_conf(self, dp, port, port_conf):
        switch_conf = self.get_switch_conf(dp)
        switch_conf["interfaces"][port] = port_conf
        self.write_faucet_conf()

    def update_switch_conf(self, dp, switch_conf):
        self.faucet_conf["dps"][dp].update(switch_conf)
        self.write_faucet_conf()

    def _get_mirrored_ports(self, dp, mirror_port):
        mirror_interface_conf = self.get_port_conf(dp, mirror_port)
        mirrored_ports = None
        if mirror_interface_conf:
            mirrored_ports = mirror_interface_conf.get("mirror", None)
        return mirror_interface_conf, mirrored_ports

    def _set_mirror_config(self, dp, mirror_port, mirror_interface_conf, ports=None):
        if ports:
            if isinstance(ports, set):
                ports = list(ports)
            mirror_interface_conf["mirror"] = ports
        # Don't delete DP level config when setting mirror list to empty,
        # as that could cause an unnecessary cold start.
        elif "mirror" in mirror_interface_conf:
            del mirror_interface_conf["mirror"]
        self.set_port_conf(dp, mirror_port, mirror_interface_conf)

    def mirror_port(self, dp, mirror_port, port):
        mirror_interface_conf, ports = self._get_mirrored_ports(dp, mirror_port)
        ports = set(ports)
        ports.add(port)
        self._set_mirror_config(dp, mirror_port, mirror_interface_conf, ports)

    def unmirror_port(self, dp, mirror_port, port):
        mirror_interface_conf, ports = self._get_mirrored_ports(dp, mirror_port)
        ports = set(ports)
        if port in ports:
            ports.remove(port)
            self._set_mirror_config(dp, mirror_port, mirror_interface_conf, ports)

    def clear_mirror_port(self, dp, mirror_port):
        mirror_interface_conf, _ = self._get_mirrored_ports(dp, mirror_port)
        self._set_mirror_config(dp, mirror_port, mirror_interface_conf)


def get_test_config():
    config = Config().get_config()
    config["faucetconfrpc_address"] = None
    return config


def get_sdn_connect(logger):
    config = get_test_config()
    prom = Prometheus()
    return SDNConnect(
        config, logger, prom, faucetconfgetsetter_cl=FaucetLocalConfGetSetter
    )
