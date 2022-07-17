# rasodalo
RAspberry digital SOund level meter DAta LOgger - rasodalo

Welcome to the rasodalo wiki!

# Development environment

Even if the code will run on a Raspberry, as it will be developed in Python we will working under Windons 
* [git](https://git-scm.com/download/win)
* [visual studio code](https://code.visualstudio.com/)
* [Python 3](https://www.python.org/downloads/)

# Setup

Start visual studio, use "source control" and choose menu "Clone"
enter: https://github.com/ckl67/rasodalo.git
Choose your local directory

In visual Studio, open terminal,

     git config --global user.name "ckl67"
     git config --global user.email "christian.klugesherz@gmail.com"


# Raspberry 

Using the Legacy version without desktop environment.
Raspberry Pi Imager is the quick and easy way to install Raspberry Pi OS 
 
= PyUSB =

We are using PyUSB which is a [Python](http://www.python.org/) library allowing easy [USB](http://www.usb.org/) access

    sudo apt install python3-pip
    pip3 install pyusb

= USB Connected =

Connect your sound level meter on your raspberry and read Product + Vendor ID

    lsusb -v

   idVendor           0x10c4 Cygnal Integrated Products, Inc.
   idProduct          0xea60 CP2102/CP2109 UART Bridge Controller [CP210x family]

= Setting permissions for the usb device: =

create a file called "/etc/udev/rules.d/50-usb-perms.rules". 
The file has to end in ".rules" to be read.

Add this rule to the file:

    SUBSYSTEM=="usb", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", GROUP="plugdev", MODE="0660"

then run:

    sudo udevadm control --reload ; sudo udevadm trigger

Make sure your user is in group plugdev:

    groups pi

After you plug in your device, you can check the permissions with:

    ls -l /dev/bus/usb/001/023
    crw-rw---- 1 root plugdev 189, 23 Aug 16 00:38 /dev/bus/usb/001/023

      (Replace /dev/bus/usb/001/023 with your device path; that was mine. 
      It changes every time you plug in the usb device. 
      You can find it by seeing which new file appears when you plug in the device.)

      That means group plugdev can "rw" the device, and I am in that group, so it works.

You can test which rules are being applied with:

    udevadm test $(udevadm info -q path -n /dev/bus/usb/001/002)
    (That's how I finally figured out that my file wasn't being read, because it didn't end in ".rules".)
