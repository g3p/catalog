Item Catalog app

-Intro
Catalog is an application that provides a list of items within a variety of categories. Catalog provides a user registration
and authentication system. Registered users have the ability to post, edit and delete their own items.

-Set Up Environment
The VM is a Linux server system that runs on top of your own computer.
We're using the Vagrant software to configure and manage the VM. Here are the tools you'll need to install to get it running:

Git

If you don't already have Git installed, download Git from git-scm.com. Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash). 
(On Mac or Linux systems you can use the regular terminal program.)

VirtualBox

VirtualBox is the software that actually runs the VM. You can download it from virtualbox.org, here.
Install the platform package for your operating system.  You do not need the extension pack or the SDK.

Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. 
You can download it from vagrantup.com. Install the version for your operating system.

Run the virtual machine!

Using the terminal, change directory to fullstack/vagrant (cd fullstack/vagrant), then type vagrant up to launch your virtual machine.

Once it is up and running, type vagrant ssh to log into it. This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt.
When you want to log out, type exit at the shell prompt.  To turn the virtual machine off (without deleting anything), type vagrant halt. 
If you do this, you'll need to run vagrant up again before you can log into it. 
Be sure to change to the /vagrant directory by typing cd /vagrant in order to share files between your home machine and the VM.  


-Installation
Unzip Catalog in /vagrant/Catalog folder

-Set Up
run database_setup.py to create the catalog database, and run lotsofitems.py to populate it.

-How to run
run python project.py

-Usage
open the browser to http://localhost:5000/ to explore the app