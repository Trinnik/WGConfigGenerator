# WireguardConfigGenerator
A very limited scope Python Flask application for generating Wireguard configurations and QR codes.

Keys are generated using the Python cryptography module, compiled into a configuration, and sent to the client. No data is stored in the process.

The user is provided a QR code, the raw client config, and a simple text output containing information for their administrator.

This application is designed to run inside a Docker container and behind a web proxy, thus gunicorn is used for simplicity.

## Usage
The best way to get this up and running to build a docker image using the included DockerFile.

The following environment variables are expected and are used to generate the configurations.

- WG_PEER_PUBLIC_KEY
    - Peer PublicKey
- WG_PEER_ENDPOINT
    - Peer Endpoint
- WG_PEER_ALLOWED_IPS
    - Peer AllowedIPs
- WG_PEER_PERSISTENT_KEEPALIVE
    - Peer PersistentKeepalive
- WEBPAGE_TITLE
    - The page title. Seen in the tab label of most browsers.
- WEBPAGE_NETWORK_NAME
    - A short name for your network. Displayed as the sub heading under "Generate Wireguard Config"