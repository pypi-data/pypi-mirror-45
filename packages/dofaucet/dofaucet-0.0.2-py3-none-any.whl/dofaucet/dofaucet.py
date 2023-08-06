import logging
import time
import digitalocean


class DoFaucet:

    def __init__(self, token):
        self._logger = logging.getLogger('dofaucet')
        self.do_token = token
        self.do_account_manager = digitalocean.Manager(token=self.do_token)
        self.raw_api_manager = digitalocean.baseapi.BaseAPI(token=self.do_token)

        self._project_resource_url_cache = dict()
        self._all_ssh_keys = self.do_account_manager.get_all_sshkeys()
        self._logger.debug('all ssh keys: %s', self._all_ssh_keys)

        self._all_projects_do_api_response = self.raw_api_manager.get_data(url='projects', type='GET')['projects']

    def _get_project_resource_url_by_name(self, project_name):
        # FIXME: what happens should the DO api return 2 IDs for a given projectname? are projectnames unique?
        for element in self._all_projects_do_api_response:
            if element['name'] == project_name:
                project_id = element['id']
                break
        else:
            raise ValueError('DO API did not return any projects ids for the provided project names')
        url = 'projects/{}/resources'.format(project_id)
        return url

    def _get_ssh_keys_by_names(self, key_names):
        ssh_keys = [key for key in self._all_ssh_keys if key.name in key_names]
        if not ssh_keys:
            raise ValueError('DO API did not return any ssh keys for the provided key names')
        self._logger.debug('found ssh keys for names: %s', ssh_keys)
        return ssh_keys

    def add_droplet_to_do_project(self, droplet, project_name):
        droplet_id = str(droplet.id)
        apidata = {'resources': ['do:droplet:' + droplet_id]}
        self.raw_api_manager.get_data(url=self._get_project_resource_url_by_name(project_name), type='POST',
                                      params=apidata)
        self._logger.debug('droplet %s: added to project %s', droplet.name, project_name)

    def set_do_dns_records(self, droplet, dnsroot, external_prefix, internal_prefix):
        subdomain = '.'.join([external_prefix, dnsroot])
        self._manipulate_dns(name=droplet.name, prefix=subdomain, record_type='A', ip=droplet.ip_address)
        self._manipulate_dns(name=droplet.name, prefix=subdomain, record_type='AAAA', ip=droplet.ip_v6_address.lower())

        subdomain = '.'.join([internal_prefix, dnsroot])
        self._manipulate_dns(name=droplet.name, prefix=subdomain, record_type='A', ip=droplet.private_ip_address)

    def _manipulate_dns(self, name, prefix, record_type, ip):
        try:
            do_dns_mgr = self.do_account_manager.get_domain(prefix)
        except digitalocean.baseapi.NotFoundError:
            # setting up domains is beyond the scope of this tool
            self._logger.info('droplet %s: unable to add %s record in domain %s. is it correctly integrated with DO?',
                              name, record_type, prefix)
        else:
            for rcrd in [rcrd for rcrd in do_dns_mgr.get_records() if rcrd.name == name and rcrd.type == record_type]:
                self._logger.info('droplet %s: removing obsolete %s record, %s, %s', name, rcrd.type, prefix, rcrd.data)
                rcrd.destroy()
            self._logger.info('droplet %s: adding %s record, %s, %s', name, record_type, prefix, ip)
            do_dns_mgr.create_new_domain_record(type=record_type, name=name, data=ip)

    def tag_droplet(self, droplet, tags):
        if not isinstance(tags, list):
            raise TypeError('tags argument has to be a list of tags')
        self._logger.info('droplet %s: set tags: %s', droplet.name, ', '.join(tags))
        for tag in tags:
            tagger = digitalocean.Tag(token=self.do_token, name=tag)
            tagger.create()
            tagger.add_droplets(str(droplet.id))

    def drip(self, name, do_region, do_image_slug, do_size_slug, do_ssh_key_names):
        # FIXME: this should propably work like _manipulate_dns, recreating droplets when they exist
        droplet = digitalocean.Droplet(token=self.do_token,
                                       name=name,
                                       region=do_region,
                                       image=do_image_slug,
                                       size_slug=do_size_slug,
                                       backups=False,
                                       ipv6=True,
                                       private_networking=True,
                                       ssh_keys=self._get_ssh_keys_by_names(do_ssh_key_names)
                                       )
        self._logger.info('droplet %s: creating...', name)
        droplet.create()
        self._logger.info('droplet %s: id: %s', name, droplet.id)

        while not (droplet.ip_address and droplet.ip_v6_address):
            time.sleep(1)
            self._logger.info('droplet %s: waiting for ip addresses', name)
            droplet.load()
        self._logger.info('droplet %s: ips: %s, %s, %s',
                          name,
                          droplet.ip_address,
                          droplet.ip_v6_address,
                          droplet.private_ip_address.lower())
        return droplet

