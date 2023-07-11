#!/usr/bin/bash
echo "[+] Start of installation..."
mkdir -p /home/"$USER"/.apps/
mv ChangingThemes /home/"$USER"/.apps/
echo "[Desktop Entry]
Encoding=UTF-8
Type=Application
Terminal=false
Exec=/home/$USER/.apps/ChangingThemes
" > /home/"$USER"/.config/autostart/ChangingThemes.desktop
echo "[+] Installation is complete!"
