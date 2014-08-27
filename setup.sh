#!/bin/bash

echo "backing up current packages"
dpkg --get-selections > $HOME/installed_packages_`date +%F`.txt
sudo cp /etc/apt/sources.list $HOME/sources-`date +%F`.list
sudo cp /etc/apt/sources.list.d ~/sources-`date +%F`.list.d -r
sudo apt-key exportall > ~/repo-`date +%F`.keys


echo "making symlinks"
ln -sf Xmodmap $HOME/.Xmodmap
ln -sf DXmodmap $HOME/.DXmodmap

