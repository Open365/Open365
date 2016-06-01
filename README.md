Open365 Installer
=================

# Overview

This is the main [Open365](https://open365.io/) installer. It installs all the required components to
run Open365 in your computer.

# Requirements

- Docker
- Docker-compose (1.3 or higher)
- Python3

### Python packages
- Debian / Ubuntu:

```
 $ apt-get install libmysqlclient-dev
 $ pip3 install mysqlclient 
 $ pip3 install pymongo
 $ pip3 install ldap3
 $ pip3 install requests
```

- Fedora

```
 $ pip3 install pymongo
 $ pip3 install ldap3
 $ pip3 install requests
 $ yum install python3-mysql
```

We require SELinux to be disabled.

# How to use it

## Install Open365

Execute the next command and follow the instructions:

    $ sudo ./open365 install

This will download all the required docker images, and start running open365.
In this beta release these images can occupy more than 15gb of space. We are
in the process of reducing this to a respectable number.

## Uninstall Open365

If you want to uninstall Open365, you just need to run:

    $ sudo ./open365 destroy

This command will clean everything related with Open365.

## Create users and domain

If you want to create new users run the following command:

    $ sudo ./open365 user-create USERNAME --surname SURNAME --password PASS --email USER_EMAIL

For more information about this command run:

    $ sudo ./open365 user-create -h

Since it is possible to create users in different domains, there is an option to
create new domains:

    $ sudo ./open365 create-domain DOMAIN

# Contribute

[Contribute](CONTRIBUTING.md)

# Issue Tracking
We use the GitHub issue tracking.

# Licensing
Open365 is licensed under the AGPL. Check [LICENSE](LICENSE) for licensing information.
