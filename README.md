# Overview

Sometimes companies requires to use their own Github/Bitbucket accounts despite
you already have your own account with dozens of repositories. But Github and 
Bitbucket identify you and your permissions by the keys. And they 
can't use the same keys in multiple accounts.

There are some solutions how to use multiple accounts but all of them are painful.

This little script helps you to keep various keys and switch between them.

## Requirements

- Python2.7 or newer
- Writeable home directory "~"
- Standard path with .ssh keys ("~/.ssh") - *you can fork and modify it 
whenever you want*

## Installation

- Download [the latest version of util](https://github.com/alexshin/ssh-key-switcher/blob/master/ssh-key-switcher.py)

`$ wget https://raw.githubusercontent.com/alexshin/ssh-key-switcher/master/ssh-key-switcher.py`

- Copy it to directory from $PATH

`$ cp ./ssh-key-switcher.py /usr/local/bin/ssh-key-switcher`

- Ensure that your user have permissions to execute the script:

`$ chmod u+x /usr/local/bin/ssh-key-switcher`


## How to use it

Type: `$ ssh-key-switcher --help` to give you detailed examples
