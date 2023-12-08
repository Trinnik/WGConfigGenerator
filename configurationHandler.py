import os


class config:
    def __init__(self):
        self.wg_peer_public_key = os.environ.get('WG_PEER_PUBLIC_KEY', '7YjLT7VB4nEXAMPLEfk6PUBLICSap4KEYJQYkKCLkjY=')
        self.wg_peer_endpoint = os.environ.get('WG_PEER_ENDPOINT', 'wg.example.com:51820')
        self.wg_peer_allowed_ips = os.environ.get('WG_PEER_ALLOWED_IPS', '0.0.0.0/0')
        self.wg_peer_persistent_keepalive = os.environ.get('WG_PEER_PERSISTENT_KEEPALIVE', '0')
        self.webpage_title = os.environ.get('WEBPAGE_TITLE', 'Wireguard Config Generator')
        self.webpage_network_name = os.environ.get('WEBPAGE_NETWORK_NAME', 'My Wireguard Network')

        self.write_template_data()

    def write_template_data(self):
        with open('./templates/index_base.html', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace('VAR_NETWORKNAME', self.webpage_network_name)
        filedata = filedata.replace('VAR_PAGETITLE', self.webpage_title)

        with open('./templates/index.html', 'w') as file:
            file.write(filedata)