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
        knobs=knobs,
        exemplar="",
        identifier="take.wifi"
    )

    @iterm2.StatusBarRPC
    async def coro(knobs):
        output = subprocess.check_output(args=[airport_path, "-I"]).decode()

        #info = re.match("^ *(agrCtlRSSI|state|lastTxRate|SSID):", contents)


iterm2.run_until_complete(main)
