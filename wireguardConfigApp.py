import re
import wireguardTool
import configurationHandler
from flask import Flask, request, render_template, jsonify


config = configurationHandler.config()
wg_peer_public_key = config.wg_peer_public_key
wg_peer_endpoint = config.wg_peer_endpoint
wg_peer_allowed_ips = config.wg_peer_allowed_ips
wg_peer_persistent_keepalive = config.wg_peer_persistent_keepalive

app = Flask(__name__)


# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle form submission
@app.route("/generate", methods=["POST"])
def generateWireguardConfig():
    if request.method == "POST":
        wg_interface_address = request.json["address"]
        wg_device_name = request.json["deviceName"]
        client_is_linux = False

        # validate address input
        if not re.search(
            "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(3[0-2]|[0-2]?[0-9])$",
            wg_interface_address,
        ):
            return jsonify(success=False, message="IP Address Not Valid")

        else:
            # generate shared key
            wg_interface_shared_key = wireguardTool.generate_private_key()

            # generate private key
            wg_interface_private_key = wireguardTool.generate_private_key()

            # derive public key
            wg_interface_public_key = wireguardTool.derive_public_key(
                wg_interface_private_key[0]
            )

            config_template_values = {
                "interface_privatekey": wireguardTool.encode_key(
                    wg_interface_private_key[1]
                ),
                "interface_address": wg_interface_address,
                "peer_publickey": wg_peer_public_key,
                "interface_sharedkey": wireguardTool.encode_key(
                    wg_interface_shared_key[1]
                ),
                "peer_endpoint": wg_peer_endpoint,
                "peer_allowedips": wg_peer_allowed_ips,
                "peer_keepalive": wg_peer_persistent_keepalive,
            }

            admin_info_values = {
                "device_name": wg_device_name,
                "interface_address": wg_interface_address,
                "interface_publickey": wireguardTool.encode_key(
                    wg_interface_public_key
                ),
                "interface_sharedkey": wireguardTool.encode_key(
                    wg_interface_shared_key[1]
                ),
            }

            wireguard_config = wireguardTool.generate_config(config_template_values)
            qr_code = wireguardTool.generate_qr_string(wireguard_config)

            admin_info = wireguardTool.generate_admin_info(admin_info_values)

            return jsonify(
                success=True, qrcode=qr_code, info=admin_info, config=wireguard_config
            )


# Failure page route
@app.route("/failure")
def failure():
    return "Config generation failed. Invalid IP address or mask."


if __name__ == "__main__":
    app.run(debug=False)
