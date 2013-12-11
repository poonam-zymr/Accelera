create_blob = {
    "config_name": "zymr-config",
    "radio_config_count": "2",
    "radio_config": {
            "radio_24g_status": "enabled",
            "radio_50g_status": "enabled"
        },
    "system_config": {
        "sntp_server": "pool.ntp.org",
        "log_server": "logserver"
    },
    "wif_config_count": "2",
    "wif_config": [
        {
            "ssid": "zymr-2.4g",
            "security": "wpa-psk",
            "passphrase": "accelera"
        },
        {
            "ssid": "zymr-5a",
            "security": "wpa-psk",
            "passphrase": "accelera"
        }
    ]
}

edit_blob = {
    "radio_config_count": "2",
    "radio_config": {
            "radio_24g_status": "enabled",
            "radio_50g_status": "enabled"
        },
    "system_config": {
            "sntp_server": "sntpserver.org",#parameter to be changed
            "log_server": "logserver.org"#parameter to be changed
    },
    "wif_config_count": "2",
    "wif_config": [
        {
            "ssid": "Z3-2.4g",#parameter to be changed
            "security": "wpa2-psk",#parameter to be changed
            "passphrase": "welcome"#parameter to be changed
        },
        {
            "ssid": "Z3-5a",#parameter to be changed
            "security": "wpa2-psk",#parameter to be changed
            "passphrase": "welcome"#parameter to be changed
        }
    ]
}
