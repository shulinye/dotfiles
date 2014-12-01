#!/bin/bash

error="$HOME/error_`date +%F`"
echo -n > $error #clearing errorlog
dotfiles="$HOME/.dotfiles"

if [ -z "$HOST" ]; then
    echo "What's my hostname?"
    read HOST
fi

echo "backing up current packages"
if [ ! -d "$HOME/backups" ]; then
    mkdir -p "$HOME/backups"
    backups="$HOME/backups"
fi

dpkg --get-selections > "$backups/$HOST-installed_packages_`date +%F`.txt"
sudo cp /etc/apt/sources.list "$backups/$HOST-sources-`date +%F`.list"
sudo cp /etc/apt/sources.list.d "$backups/$HOST-sources-`date +%F`.list.d" -r
sudo apt-key exportall > "$backups/$HOST-repo-`date +%F`.keys"

echo "updating repos"
sudo apt-get update

if hash pip 2>/dev/null; then
    pip freeze > $backups/$HOST-pip-packages_`date +%F`.txt 2>>$error
else
    echo "pip not installed, continuing happily"
    echo "pip not installed" >>$error
fi

echo "making symlinks"
ln -sf $dotfiles/Xmodmap $HOME/.Xmodmap
ln -sf $dotfiles/DXmodmap $HOME/.DXmodmap
ln -sf $dotfiles/bashrc $HOME/.bashrc

if [ ! -d "$HOME/xmonad" ]; then
    mkdir "$HOME/xmonad"
fi

ln -sf $dotfiles/xmonad/xmonad.hs $HOME/xmonad/xmonad.hs

if [ ! -d "$HOME/.config/git" ]; then
    mkdir -p "$HOME/.config/git"
fi

ln -sf $dotfiles/git/ignore $HOME/.config/git/ignore

echo "Errors may have happened, check $error"
cat $error
