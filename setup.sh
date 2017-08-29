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

packagelist="$dotfiles/package_lists/linux_packages.txt"
xargs -a <(awk '! /^ *(#|$)/' "$packagelist") -r -- sudo apt-get install

if hash pip 2>/dev/null; then
    pip freeze > $backups/$HOST-pip-packages_`date +%F`.txt 2>>$error
else
    echo "pip not installed, continuing happily"
    echo "pip not installed" >>$error
fi

sudo cp "$dotfiles/scripts/define" "/usr/local/bin/define"

echo "making symlinks"
ln -sf $dotfiles/Xmodmap $HOME/.Xmodmap
ln -sf $dotfiles/DXmodmap $HOME/.DXmodmap
ln -sf $dotfiles/bashrc $HOME/.bashrc
ln -sf $dotfiles/bash_aliases $HOME/.bash_aliases
ln -sf $dotfiles/rc_common $HOME/.rc_common
ln -sf $dotfiles/vimrc $HOME/.vimrc
ln -sf $dotfiles/git $HOME/.config/git

mkdir -p $HOME/.TeXworks/templates
ln -sf $dotfiles/Texworks/templates $HOME/.TeXworks/templates/custom

if [ ! -d "$HOME/xmonad" ]; then
    mkdir "$HOME/xmonad"
fi

ln -sf $dotfiles/xmonad/xmonad.hs $HOME/xmonad/xmonad.hs

if [ ! -d "$HOME/.config/git" ]; then
    mkdir -p "$HOME/.config/git"
fi

ln -sf $dotfiles/git/ignore $HOME/.config/git/ignore

mkdir -p $HOME/.vim/backup

echo "Errors may have happened, check $error"
cat $error
