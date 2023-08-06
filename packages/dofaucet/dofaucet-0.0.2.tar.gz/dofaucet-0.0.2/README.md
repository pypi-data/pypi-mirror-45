dofaucet
===

# tl;dr
Read YAML-formatted ansible inventory, create digitalocean droplets accordingly.

Neat tricks: 
 - creates DNS records for both internal and external droplet IPs
 - adds ssh pubkeys to droplets (only keys already uploaded to DO)
 - adds alls created droplets to a project so they're easy to identify

# Example usage

## Inventory

foo.yml
```
all:
  vars:
    do_ssh_key_names: ['my_key', 'my_friends_key']
    dofaucet_dnsroot: example.com
    do_project: test_webstack_ansible
    do_image_slug: fedora-28-x64

foohosts:
  vars:
    do_tags: foohosts
  hosts:
    foo.infra.example.com

barhosts:
  vars:
    do_tags: barhosts
    # the bar app needs more ram
    do_size_slug: s-1vcpu-2gb
  hosts:
    bar.infra.example.com
```
## dofaucet CLI
```
dofaucet --token 23234242 --project foo --inventory foo.yml
```

# future ideas

Ansible is python3, so we could use the native ansible functionality to parse the inventory.
Example code:
```
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager

loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='~/inventory.yml')
variable_manager = VariableManager(loader=loader, inventory=inventory)
```