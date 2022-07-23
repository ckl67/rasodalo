# rasodalo

RAspberry digital SOund level meter DAta LOgger - rasodalo

# Development environment

* [visual studio code](https://code.visualstudio.com/)
* [git](https://git-scm.com/download/win)
* [Python 3](https://www.python.org/downloads/)

# Window Setup

## Git

Start visual studio, use "source control" and choose menu "Clone"
enter: https://github.com/ckl67/rasodalo.git
Choose your local directory

In visual Studio, open terminal,

     git config --global user.name "ckl67"
     git config --global user.email "christian.klugesherz@gmail.com"

Make a first commit, and synhro, "Visual Studio" will start "Authorize Git Credential Manager"

Create a file .gitignore and add

    *.log
    __pycache__/


## python

Install Python
The default path is :

     C:\Users\[kluges1]\AppData\Local\Programs\Python\Python310
     C:\Users\[user]\AppData\Local\Programs\Python\Python310

Edit the system environment variables, and add the path

     For add the path, just surch in windows "environment variables"

Install [PyUSB](https://github.com/pyusb/pyusb)
PyUSB provides for easy access to the host machine's Universal Serial Bus (USB) system for Python 3.

    python.exe -m pip install --upgrade pip
    python.exe -m pip install PySUB 
    
## USB Devise

Get idVendor and idProduct thanks to USBView

Universal Serial Bus Viewer (USBView) or USBView.exe is a Windows graphical UI app that you can use to browse all USB controllers and connected USB devices on your computer. USBView works on all versions of Windows.

To download and use USBView, complete the following steps:

* Download and install the [Windows SDK]'https://developer.microsoft.com/fr-fr/windows/downloads/windows-sdk/)
* During the installation, select **only** the Debugging Tools for Windows box and clear all other boxes.
* By default, on a x64 PC the SDK will install USBView to the following directory. C:\Program Files (x86)\Windows Kits\10\Debuggers\x64
* Open the kits debugger directory for the processor type you're running, and then select USBView.exe to start the utility.

you should get 
     idVendor:                        0x10C4 = Silicon Laboratories, Inc.
     idProduct:                       0xEA60

This information has to be entered in the code

## Error which stops Windows development

I was not able to avoid "No backend available" by running the code

    python -m pip install libusb

This install the package 

    libusb-1.0.dll will be automatically added to:
    C:\Users\kluges1\AppData\Local\Programs\Python\Python310\Lib\site-packages\libusb\_platform\_windows\x86
    C:\Users\kluges1\AppData\Local\Programs\Python\Python310\Lib\site-packages\libusb\_platform\_windows\x64

Now just add those paths (the full path) to Windows Path and restart CMD 

This is not working, so I revert back to Raspberry Development

# Raspberry setup

## Install 

Using the Legacy version without desktop environment.
Raspberry [Pi Imager](https://www.raspberrypi.com/software/) is the quick and easy way to install Raspberry Pi OS 

Configure "Pi Imager" to activate : ssh; Wifi,..

You can use [Advanced IP scanner ](https://www.advanced-ip-scanner.com/fr/) to recover the IP address of your Raspberry

## remote

From inside VS Code, you will need to install the "Remote SSH" extension.
Next you can connect to your Raspberry Pi. 
Launch the VS Code command palette using Ctrl+Shift+P on Linux or Windows

     Remote SSH: Connect current window to host 

Add a new host :

Enter the SSH connection details, using user@host. For the user, enter the Raspberry Pi username (the default is pi). For the host, enter the IP address of the Raspberry Pi, or the hostname.
pi@192.168.1.59


## git

Install 

    sudo apt-get install git-core

Now that you have Git installed on your system, you need to customize your Git environment.
You only need to make these settings once; they will persist when you upgrade.
Git contains a tool called "git config" to let you view and modify configuration variables 

    git config --global user.name "ckl67" 
    git config --global user.email "christian.klugesherz@gmail.com"


Start visual studio, use "source control" and choose menu "Clone"
enter: https://github.com/ckl67/rasodalo.git
Choose your local directory

Make a first commit, and synhro, "Visual Studio" will start "Authorize Git Credential Manager"

Create a file .gitignore and add

    *.log
    __pycache__/

## Python3

Python is installed by default

We are using PyUSB which is a [Python](http://www.python.org/) library allowing easy [USB](http://www.usb.org/) access

    sudo apt install python3-pip
    pip3 install pyusb


## USB Connected

Connect your sound level meter on your raspberry and read Product + Vendor ID

    lsusb -v

   idVendor           0x10c4 Cygnal Integrated Products, Inc.
   idProduct          0xea60 CP2102/CP2109 UART Bridge Controller [CP210x family]

### Setting permissions for the usb device:

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

