#!/bin/env python3

import sys
import argparse
import logging

from dofaucet.dofaucet import DoFaucet
from dofaucet.ansibleinventory import AnsibleInventory


def open_faucet():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s: %(message)s',
                        handlers=[logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger('dofaucet')

    parser = argparse.ArgumentParser(description='read ansible yaml inventory, create droplets')
    parser.add_argument('--token', metavar='do_api_token', type=str, required=True, help='DO API token')
    parser.add_argument('--inventory', dest='inventory_path', metavar='example.yml', type=str, required=True,
                        help='ansible inventory file')
    parser.add_argument('--project', metavar='project', type=str, required=False, default=None,
                        help='DO project name, overrides the inventory-level project name (unimplemented)')
    parser.add_argument('--debug', dest='debug', action='store_true', required=False, default=False,
                        help='Activate debugging output')
    cliargs = parser.parse_args()

    if cliargs.debug:
        logger.setLevel(logging.DEBUG)
        logger.info('Loglevel set to DEBUG')

    inventoryparser = AnsibleInventory()
    inventory = inventoryparser.load_inventory(cliargs.inventory_path)
    myfaucet = DoFaucet(token=cliargs.token)
    created_droplets = list()

    for group_name, group_props in inventory.items():
        logger.info('setting up group %s', group_name)
        for dropletname in group_props.dropletnames:
            logger.info('creating droplet: %s', dropletname)
            logger.debug('\tdo ssh keys: %s', group_props.do_ssh_key_names)
            logger.debug('\tdo project: %s', group_props.do_project)
            logger.debug('\tdo image slug: %s', group_props.do_image_slug)
            logger.debug('\tdo size slug: %s', group_props.do_size_slug)
            logger.debug('\tdo tags: %s', group_props.do_tags)
            logger.debug('\tuniversal tag: %s', group_props.universal_tag)
            logger.debug('\tdo region: %s', group_props.do_region)
            logger.debug('\tDNS TLD: %s', group_props.dofaucet_dnsroot)
            logger.debug('\tinternal dns prefix: %s', group_props.internal_dns_prefix)
            logger.debug('\texternal dns prefix: %s', group_props.external_dns_prefix)

            do_droplet = myfaucet.drip(name=dropletname,
                                       do_region=group_props.do_region,
                                       do_image_slug=group_props.do_image_slug,
                                       do_size_slug=group_props.do_size_slug,
                                       do_ssh_key_names=group_props.do_ssh_key_names)

            myfaucet.add_droplet_to_do_project(do_droplet, group_props.do_project)
            myfaucet.tag_droplet(do_droplet, [*group_props.do_tags, group_props.universal_tag])

            myfaucet.set_do_dns_records(droplet=do_droplet,
                                        dnsroot=group_props.dofaucet_dnsroot,
                                        external_prefix=group_props.external_dns_prefix,
                                        internal_prefix=group_props.internal_dns_prefix)
            created_droplets.append(do_droplet)

    logger.info('done, droplet ids: %s', ' '.join([str(droplet.id) for droplet in created_droplets]))

if __name__ == '__main__':
    open_faucet()
