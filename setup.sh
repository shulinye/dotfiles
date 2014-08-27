#!/bin/bash

echo "backing up current packages"
dpkg --get-selections > $HOME/$HOST-installed_packages_`date +%F`.txt
sudo cp /etc/apt/sources.list $HOME/$HOST-sources-`date +%F`.list
sudo cp /etc/apt/sources.list.d ~/$HOST-sources-`date +%F`.list.d -r
sudo apt-key exportall > ~/$HOST-repo-`date +%F`.keys


echo "making symlinks"
ln -sf Xmodmap $HOME/.Xmodmap
ln -sf DXmodmap $HOME/.DXmodmap

