import os
import yaml
import types
import logging


class AnsibleInventory:
    UNIVERSAL_TAG = 'dofaucet'
    DEFAULT_DOFAUCET_DNSROOT = 'example.com'
    DEFAULT_DO_PROJECT = UNIVERSAL_TAG
    DEFAULT_INTERNAL_DNS_PREFIX = 'dointern'
    DEFAULT_EXTERNAL_DNS_PREFIX = 'infra'
    # FIXME: pull these defaults from the DO API if possible
    DEFAULT_DO_IMAGE_SLUG = 'fedora-29-x64'
    DEFAULT_DO_SIZE_SLUG = 's-1vcpu-1gb'  # 's-2vcpu-2gb' 's-1vcpu-1gb'
    DEFAULT_DO_REGION = 'fra1'

    def __init__(self):
        self._logger = logging.getLogger('dofaucet')

        self.dofaucet_defaults = {
            'dofaucet_dnsroot': self.DEFAULT_DOFAUCET_DNSROOT,
            'do_project': self.DEFAULT_DO_PROJECT,
            'do_image_slug': self.DEFAULT_DO_IMAGE_SLUG,
            'do_size_slug': self.DEFAULT_DO_SIZE_SLUG,
            'do_region': self.DEFAULT_DO_REGION,
            'internal_dns_prefix': self.DEFAULT_INTERNAL_DNS_PREFIX,
            'external_dns_prefix': self.DEFAULT_EXTERNAL_DNS_PREFIX,
            'universal_tag': self.UNIVERSAL_TAG,
            'do_tags': list(),
            'do_ssh_key_names': list()
        }

    def load_inventory(self, yml_path):
        inventory = dict()
        yml_path = os.path.expanduser(yml_path)
        yml_content = yaml.safe_load(open(yml_path, 'r'))

        # force the "all" group to be defined
        yml_content.setdefault('all', dict())
        # load inventory defaults from the "all" group
        inventory_defaults = yml_content['all'].get('vars', dict())

        for group_name in yml_content.keys():
            # 3-way merge dofaucet defaults, inventory defaults and group vars with the last defined option winning
            group_vars = {**self.dofaucet_defaults, **inventory_defaults, **yml_content[group_name].get('vars', dict())}
            # vars = self._load_groupvars(group_name, yml_content)
            group_hosts = yml_content[group_name].get('hosts', list())
            group_vars, group_hosts = self._fix_idiosyncrasies(group_vars, group_hosts)
            # hosts in the inventory usually use their full FQDN
            # we can't change this because ansible uses this inventory name to connect
            # arrange the hostname, not the external FQDN, to be our droplet names
            droplets = [hostname.split('.')[0] for hostname in group_hosts]

            inventory[group_name] = types.SimpleNamespace(group_name=group_name, dropletnames=droplets, **group_vars)

        return inventory

    def _fix_idiosyncrasies(self, group_vars, group_hosts):
        # depending on the yml, we may get a list or a string for these.
        for item in ['do_ssh_key_names', 'do_tags', 'do_ssh_key_names']:
            if isinstance(group_vars[item], str):
                group_vars[item] = group_vars[item].split()
        # i suspect this may be a list if hosts definitions look like this: "hosts: [foo, bar]"
        #  not sure if that's "ansible-legal", though.
        if isinstance(group_hosts, str):
            group_hosts = group_hosts.split()
        # users might specify dns prefixes with leading or trailing dots by mistake
        for item in ['internal_dns_prefix', 'external_dns_prefix', 'dofaucet_dnsroot']:
            group_vars[item] = group_vars[item].strip('.')
        return (group_vars, group_hosts)
