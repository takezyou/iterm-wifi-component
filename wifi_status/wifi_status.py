#!/usr/bin/env python3

import iterm2
import subprocess
import re

airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
signals = ["▁", "▂", "▄", "▆", "█"]


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description="Wifi status",
        detailed_description="Wifi status bar components",
        knobs=[],
        exemplar="wifi  | ▁▂▄ | ",
        update_cadence=5,
        identifier="take.wifi"
    )

    @iterm2.StatusBarRPC
    async def wifi_status(knobs):
        signal = ""

        output = subprocess.check_output(args=[airport_path, "-I"]).decode()
        info = re.findall("[\s]*(agrCtlRSSI|agrCtlNoise|state|lastTxRate|SSID):[\s]([!-~\ ]*)", output)
        rssi = int(info[0][1])
        noise = int(info[1][1])
        rate = info[3][1]
        ssid = info[5][1]
        snr = rssi - noise

        if int(rate) == 0:
            signal = "🙅‍♂️"
            status = "{0}".format(signal)
        else:
            # 25dB SNR -> 5 bars
            power = min(snr // 5, 5)
            signal = "".join(signals[:power])
            status = "{0}  | {1} |".format(ssid, signal)
        # print(f"rssi: {rssi}, noise: {noise}, snr: {snr}, ssid: {ssid}")
        return status

    await component.async_register(connection, wifi_status)

iterm2.run_forever(main)
