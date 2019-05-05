#!/usr/bin/env python3

import iterm2
import subprocess
import math
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
        info = re.findall("[\s]*(agrCtlRSSI|state|lastTxRate|SSID):[\s]([!-~]*)", output)
        rssi = info[0][1]
        rate = info[2][1]
        ssid = info[4][1]

        if int(rate) == 0:
            signal = "🙅‍♂️"
            status = "{0}".format(signal)
        else:
            _rssi = (5 - int(rssi) / -20)

            for r in range(math.ceil(_rssi)):
                signal = signal + signals[r]
            status = "{0}  | {1} |".format(ssid, signal)
        return status

    await component.async_register(connection, wifi_status)

iterm2.run_forever(main)
