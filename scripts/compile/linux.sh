#!/bin/bash

bin_path="bin"
filename="colour-challenge_linux64"
target_path="$bin_path/$filename"
if [ -f "$target_path" ]; then
    rm "$target_path"
fi
.env/bin/pyinstaller gui.spec --noconfirm --noconsole --onefile --distpath "$bin_path"
mv "$bin_path/gui" "$target_path"
