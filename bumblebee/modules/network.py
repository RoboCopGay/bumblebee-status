"""
show SSID of wifi device connected or Ethernet Connected
for best use insert shortcup for select and connect in wifi network:
    -m shortcut network -p shortcut.cmd="bash $HOME/.bin/wifi.py" shortcut.labels="[wifi]"
requires:
    $HOME/.bin/network/network.get_status
    $HOME/.bin/wifi.py
    $HOME/.bin/rofi_run
    rofi

    instalation:
        git clone https://github.com/RoboCopGay/bumblebee-network-module.git $HOME/.bin

        sudo apt install rofi
        sudo dnf install rofi
        sudo yum install rofi
        sudo pacman -S   rofi
"""
import bumblebee.engine
from os import popen, system
from sys import argv

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.get_status))
    def get_status(self, widget):
        return popen("bash $HOME/.bin/network/network.get_status").read().strip()
