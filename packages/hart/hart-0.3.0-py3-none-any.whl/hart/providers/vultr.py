from .base import BaseLibcloudProvider

class VultrProvider(BaseLibcloudProvider):

    def __init__(self, token):
        constructor = get_driver(Provider.VULTR)
        self.driver = constructor(token)


    def create_node(self):
        size = get_size(self.driver, args.size)
        image = get_image(self.driver, args.debian_codename)
        location = get_location(self.driver, args.region)
        node = self.driver.create_node(args.minion_id, size, image, location, ex_ssh_key_ids=[
            key_pair.id
        ], ex_create_attr={
            'userdata': cloud_init,
            'notify_activate': False,
            'enable_private_network': args.private_networking,
            'hostname': minion_id,
            'tag': args.tags,
        })


    def create_remote_ssh_key(self, key_name, ssh_key, public_key):
        # The vultr provider mistakenly returns a success bool instead of the key pair.
        # PR from 2017 that fixes it: https://github.com/apache/libcloud/pull/998
        # ¯\_(ツ)_/¯s
        self.driver.create_key_pair(key_name, public_key)
        key_pairs = self.driver.list_key_pairs()
        for key_pair in key_pairs:
            if key_pair.name == key_name:
                break
        else:
            raise ValueError('Failed to create ssh key pair')
        return key_pair, key_pair


    def get_image(self, debian_codename):
        for image in self.driver.list_images():
            if image.extra['family'] == 'debian' and image.extra['arch'] == 'x64' and debian_codename in image.name:
                return image

        raise ValueError('Debian %s image not found' % debian_codename)


    def destroy_node(self, node):
        # Vultr doesn't handle deleting nodes that haven't finished
        # initialization well, wait for the node to finish boot before
        # destroying it
        timeout = 180
        start_time = time.time()
        while True:
            time.sleep(3)
            node = self.get_updated_node(node)
            if node.state == NodeState.RUNNING:
                self.driver.destroy_node(node)
                break
            if time.time() - start_time > timeout:
                raise ValueError('Timed out waiting to delete initializing node: %s' % node.id)
