#!/usr/bin/env bash

INSTALL_FOLDER=~/.config/matplotlib/stylelib/


echo "Install *.mplstyle at"
echo $INSTALL_FOLDER
echo -n "(y/n)? "
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then
    mkdir -p  $INSTALL_FOLDER
    cp ./*.mplstyle $INSTALL_FOLDER
else
    echo You can also create a sym-link:
    echo ln -s ./*.mplstyle $INSTALL_FOLDER
fi
