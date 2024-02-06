# run this after archinstall, make sure you have git, steam, networkmanager, iwd, xorg-server, python, and nvidia (if applicable) already installed, choose systemd, and pipewire for audio please. Run this script as root and name the user "steamos"
# to connect to wifi use this:
# 1) iwctl
# 2) station wlan0 connect <ssid>
# 3) exit
# 4) sudo nmcli device wifi connect <SSID> password <password>

import os

os.system("clear")
choice = input("Are you running this script as root? y/n\n")
if choice.lower() == "y":
    choice = input("Are you using nvidia? y/n\n")
    if choice == "y":
        os.system("nvidia-xconfig")
    
    os.system("sudo agetty -a -n steamos")
    os.system("systemctl enable NetworkManager")
    os.system("systemctl start NetworkManager")
    os.system("pacman -Syu ntfs-3g")
    os.system("pacman -Syu exfatprogs")
    os.system("pacman -S exfat-utils")
    
    # auto update
    with open("/etc/systemd/system/pacman-update.timer", "w") as file:
        file.write("[Unit]\nDescription=Run pacman-update.service weekly\n\n[Timer]\nOnCalendar=weekly\nPersistent=true\n\n[Install]\nWantedBy=multi-user.target")

    with open("/etc/systemd/system/pacman-update.service", "w") as file:
        file.write("[Unit]\nDescription=Update Arch Linux packages\n\n[Service]\nType=oneshot\nExecStart=/usr/bin/pacman -Syu --noconfirm")

    os.system("sudo systemctl enable --now pacman-update.timer")

    with open("/etc/systemd/system/steam.service", "w") as file:
        file.write("[Unit]\nDescription=Steam Client Boot\n\n[Service]\nType=simple\nExecStart=/usr/bin/steam\nRestart=on-failure\nRestartSec=30\nUser=steamos\nEnvironment=DISPLAY=:0\n\n[Install]\nWantedBy=multi-user.target")

    os.system("sudo systemctl enable steam.service")
    os.system("reboot")

elif choice.lower() == "n":
    print("Please run this as root!")

else:
    print(f"'{choice}' is not a valid option.")
