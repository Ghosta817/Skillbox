#!/bin/bash

my_dir="$HOME/TET"

#if [[ $(id -u) -ne 0 ]] ;
#       then echo "Please run as root" ; exit 1 ;
#fi

#git clone https://gitlab.skillbox.ru/ilia_k/python_basic_diploma.git -b master $my_dir
git clone git@gitlab.skillbox.ru:ilia_k/python_basic_diploma.git -b master $my_dir

chmod 755 $my_dir && cd $my_dir

sudo apt update && sudo apt install tmux python3.8-venv -y
python3 -m venv venv

source venv/bin/activate
python -m pip install --upgrade pip
pip install -r Install_Bot/requirements.txt
deactivate

rm -rf Install_Bot .git
rm -f .gitignore Win_runBot.bat readme.md
[ ! -d "$HOME/bin" ] && mkdir -p "$HOME/bin" && source .bashrc
chmod 750 Ubnt_runBot.sh && mv Ubnt_runBot.sh "$HOME/bin/runBot.sh"