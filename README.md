# XWiki Playbook
Ansible playbook to install xwiki on ubuntu using standalone distribution method.

## XWiki Introduction
* XWiki is a free and opensource advanced Wiki Software which is written in Java. It runs on servlet containers like JBoss, Tomcat etc. It uses a database such as MySQL or PostgreSQL to store its information.
* XWiki installation using standalone distribution is the fastest and easiest way because all components needed by XWiki are automatically installed on the server. This XWiki software provides an in-built  XWiki, with a portable database (HSQLDB) and a lightweight Java container (Jetty).
## Features
* A very robust WYSIWYG editor for page editing
* A powerful wiki syntax
* Content organization
* Create your own applications
* Version Control
* Advanced search 
## Hardware and Software Requirements
* Java 1.8.0_101 or greater installed for XWiki >= 8.1 (Java 7 or greater for XWiki < 8.1, Java 6 or greater for XWiki versions < 6.0)
* A Servlet Container supporting Servlet 3.0.1 (Servlet 2.4 for XWiki versions < 7.0)
* A Database and a JDBC 4 Driver for your database
* Enough memory, at least 2 GB RAM (or 1 GB for small Wikis)
## Documentation
Visit the [XWiki official](https://www.xwiki.org/xwiki/bin/view/Documentation/) page for full usage instructions, admin guide and developer guide including installation, tutorials, and examples.
## XWiki Installation Guide
Refer here: [Installation on Ubuntu 18.04](https://linoxide.com/install-xwiki-ubuntu/)
### Step 1: Install Java
* XWiki is a Java-based application, so you will need to install Java 8 or above to meet its software requirement.
1. Update the repositories
```
$ apt-get update
```
2. Install OpenJDK
```
$ apt-get install openjdk-8-jdk
```
3. Verify the version of the JDK
```
$ java -version
```
### Step 2: Download and Install XWiki
* We need to download the generic installer that works on all platforms.
```
$ wget http://download.forge.ow2.org/xwiki/xwiki-enterprise-installer-generic-8.1-standard.jar
```
* Once you have downloaded this installer, you can install this downloaded package using Java. The installer takes you to a popup window or various interactive sections where it demands an output like entering 1 (accept or proceed)/ 2 (quit) /3 (redisplay) from you to proceed with the installation.
```
$ java -jar xwiki-enterprise-installer-generic-8.1-standard.jar
```
### Step 3: Start xwiki using bash command
* Once the installation is done, you need to move to the application folder and run the XWiki startup script using bash command.
```
$ bash start_xwiki.sh  
```
### Step 4: Launch the application
* Once XWiki is started, you can point your browser to access the Web interface.
```
http://ServerIP or Hostname:8080/ 
```
### Enable X11 Forwarding
***
* X11 forwarding is a mechanism that allows a user to start up remote applications but forward the application display to your local Windows machine.
* During xwiki installation, the installer takes you to a popup window so you have to enable X11 forwarding.
### Putty
***
If you are using putty to connect to remote host, follow the below steps:
  *  Start PuTTY.
  *  In the PuTTY Configuration section, on the left panel, select Connection → SSH → X11
  *  On the right panel, click on the Enable X11 forwarding checkbox
  *  Click on Session option on the left panel.
  *  Enter the hostname or IP address in the Host Name textbox
  *  Save the session.
### MobaXterm
***
  * In MobaXterm, X11 is automatically enabled.
### Linux
***
* Enabling the X11 forwarding feature in SSH is done within the SSH configuration file.
* The configuration file is /etc/ssh/ssh_config, and must be edited with sudo or Root user access.
* In a terminal, open up ssh_config in the Nano or vi text editor tool.
```
$ sudo nano /etc/ssh/ssh_config
```
* Add/modify following line:
```
[...]

ForwardX11 yes
```
* Save the file and restart sshd service to effect the changes.
```
$ sudo systemctl restart sshd
```
## Ansible Installation
***
```
$ pip3 install ansible
```
## Ansible playbook to install XWiki
***
```
---
# ansible playbook to install xwiki
- name: Download/Install Java and xwiki
  hosts: localhost
  gather_facts: true
  tasks:
    - name: Update APT package manager repositories cache
      become: true
      apt:
        update_cache: yes

    - name: Gather the package facts
      package_facts:
        manager: auto

    - name: Install OpenJDK Java
      become: true
      apt:
        name: openjdk-8-jdk
        state: present
      when: "'openjdk-8-jdk' not in ansible_facts.packages"

    - name: Check xwiki is downloaded or not
      stat:
        path: /home/$USER/xwiki-enterprise-installer-generic-8.1-standard.jar
      register: st

    - name: Download xwiki using the url
      become: true
      get_url:
        url: "http://download.forge.ow2.org/xwiki/xwiki-enterprise-installer-generic-8.1-standard.jar"
        dest: /home/$USER
      when: not st.stat.exists

    - name: Check xwiki is installed or not
      stat:
        path: /home/$USER/XWiki Enterprise 8.1
      register: result
      
    - name: Install xwiki
      when: not result.stat.exists
      shell: cd /home/$USER && java -jar xwiki-enterprise-installer-generic-8.1-standard.jar

    - name: Start xwiki using the bash command
      shell: nohup bash /home/$USER/'XWiki Enterprise 8.1'/start_xwiki.sh &
```
## Running Playbook
***
```
$ ansible-playbook <playbook-name>.yml -K
```
**Note:** `nohup.out` file is generated in _/home/username_ or the current directory where you have executed the command.
