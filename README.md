# rasodalo

RAspberry digital SOund level meter DAta LOgger - rasodalo

# Development environment

Install
* [visual studio code](https://code.visualstudio.com/)

# Window Setup

# git

Install
* [git](https://git-scm.com/download/win)

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

### Python 3

Install Python
* [Python 3](https://www.python.org/downloads/)

The default path is :

     C:\Users\[kluges1]\AppData\Local\Programs\Python\Python310

     C:\Users\[user]\AppData\Local\Programs\Python\Python310

Add these path to system environment variables

     For add the path, just surch in windows "environment variables"

### PyUSB

Install [PyUSB](https://github.com/pyusb/pyusb)
PyUSB provides for easy access to the host machine's Universal Serial Bus (USB) system for Python 3.
PyUSB does nt include the Backend

    python.exe -m pip install --upgrade pip
    python.exe -m pip install PySUB 

### Backend 

From here I recommend to jump to the last part of this doc, relative to "protocol revert engineering".
In fact Zadig will delete the default USB driver provided by Vellman DEM202 Sotfware. 

Meaning the CP210x VCP Drivers for Windows will be removed, and libusb will be associated with the USB.
So Datalogger cannot be used anymore, because : "CP210x USB to UART bridge Driver" is removed 

PyUSB need a backend.

        Jump to Zadig, Next is not the solution !

            python.exe -m pip install libusb

        is not the solution ! 
        This will install libusb-1.0.dll to:
            C:\Users\kluges1\AppData\Local\Programs\Python\Python310\Lib\site-packages\libusb\_platform\_windows\x86
            C:\Users\kluges1\AppData\Local\Programs\Python\Python310\Lib\site-packages\libusb\_platform\_windows\x64

        In case you have used it, you have to remove it

            python.exe -m pip uninstall libusb

### Zadig

PyUsb needs a 'backend' installation step which is not well documented for windows. 
The leading candidates are libusb-win32 vs libusb-1.0.22 which has a recommended installer: zadig.

[Zadig](https://zadig.akeo.ie/) is a Windows application that installs generic USB drivers, such as WinUSB, libusb-win32/libusb0.sys or libusbK, to help you access USB devices.

Run Zadig : Option --> List all Devices, and then connect the specific device to libusb-win32 
Zadig will download, and install the driver ! 

#### IF issue

Disconnect the device.
Run cmd.exe and type in to open devices management:

    set devmgr_show_nonpresent_devices=1
    devmgmt

In menu click – View – Show hidden devices.
Right click on your device and click Uninstall.


Go to a hidden directory 
    c:\windows\inf 
    
and delete those oem*.inf files which contains a reference to your device.

Remove original libusb driver/zadig directory because Windows might look for all known places to find a device driver.
Delete 

    C:\Users\kluges1\usb_driver

Reboot.
 
## USB Devise

Get idVendor and idProduct thanks to USBView

Zadig, will also provide this information!

Universal Serial Bus Viewer (USBView) or USBView.exe is a Windows graphical UI app that you can use to browse all USB controllers and connected USB devices on your computer. USBView works on all versions of Windows.

To download and use USBView, complete the following steps:

* Download and install the [Windows SDK]'https://developer.microsoft.com/fr-fr/windows/downloads/windows-sdk/)
* During the installation, select **only** the Debugging Tools for Windows box and clear all other boxes.
* By default, on a x64 PC the SDK will install USBView to the following directory. C:\Program Files (x86)\Windows Kits\10\Debuggers\x64
* Open the kits debugger directory for the processor type you're running, and then select "USBView.exe" to start the utility.

you should get 
     idVendor:                        0x10C4 = Silicon Laboratories, Inc.
     idProduct:                       0xEA60

This information has to be entered in the code

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

# Protocol

## DEM202 Sound Level Meter

To revert engineer the procol used, you can use WhireShark + USB Capture

For taht We are using the software provided by Velman data logger for the [sound level meter DEM202](https://www.velleman.eu/support/downloads/?code=DEM202)

Be care, use a virtualbox Win environment for that.
Because Zadig will remove the origin Driver !

So under Virtual Box 
Install the tool.
Then run under: C:\Program Files (x86)\Sound Level Meter Datalogger

I case of issue, It is possible that the .NET Framework 3.5 package is missing on your PC.
Download and install .NET Framework 3.5 by following link :
https://docs.microsoft.com/en-us/dotnet/framework/install/dotnet-35-windows

        After installation of .NET Framework 3.5, follow the procedure below please.

        Remove the installed DEM202 software.
        Restart the computer.
        After restart, re-install the DEM202 software with full administrator rights.
        How to install with full administrator rights:

        Click with right mouse button on the setup file, and choose in the pop-up menu "Run as administrator" and follow the instructions on the screen.

## WireShark

Filter

usb.idVendor == 0x10C4