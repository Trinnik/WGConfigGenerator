import codecs
import qrcode
import qrcode.image.svg
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization


# generate private key and return cryptography object and bytes
def generate_private_key():
    private_key = X25519PrivateKey.generate()
    bytes_ = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return [private_key, bytes_]


# derive a public key from provided private key
def derive_public_key(private_key):
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    return public_key


# encode key bytes as utf8 string
def encode_key(key_bytes=bytes):
    return codecs.encode(key_bytes, "base64").decode("utf8").strip()


# generate qr code containing wireguard config and return as svg string
def generate_qr_string(configuration):
    return qrcode.make(
        configuration, image_factory=qrcode.image.svg.SvgPathFillImage
    ).to_string(encoding="unicode")


# generate filled wireguard config
def generate_config(values=dict):
    wg_config_template = "[Interface]\nPrivateKey = {interface_privatekey}\nAddress = {interface_address}\n\n[Peer]\nPublicKey = {peer_publickey}\nPresharedKey = {interface_sharedkey}\nEndpoint = {peer_endpoint}\nAllowedIPs = {peer_allowedips}\nPersistentKeepalive = {peer_keepalive}"

    return wg_config_template.format(**values)


# generate admin data
def generate_admin_info(values=dict):
    admin_info_template = "Device Name: {device_name}\nIP Address: {interface_address}\nPublic Key: {interface_publickey}\nShared Key: {interface_sharedkey}"

    return admin_info_template.format(**values)
