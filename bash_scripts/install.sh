#!/usr/bin/bash
echo "[+] Start of installation..."
mv __main__.py style.py
chmod +x style.py
mkdir -p /home/"$USER"/.apps/Styles
mv style.py /home/"$USER"/.apps/Styles
echo "[Desktop Entry]
Encoding=UTF-8
Type=Application
Terminal=false
Exec=/usr/bin/python3 /home/$USER/.apps/Styles/style.py
" > /home/"$USER"/.config/autostart/style.desktop
echo "[+] Installation is complete!"
