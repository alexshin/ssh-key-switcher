#!/usr/bin/env python
import argparse
import os
import shutil

HOME_DIR = os.path.expanduser('~')
SSH_KEYS_DIR = '%s/.ssh' % HOME_DIR
KEYS_STORAGE_DIR = '%s/.ssh-key-switcher' % HOME_DIR
DECORATE_LINE_LENGTH = 10
DECORATE_LINE_SYMBOL = '-'

DESCRIPTION = """
Switch keys between accounts for .ssh
{underline}

Helps to switch between ssh-keys. This tool can keep separated keys inside "{key_storage_dir}".

Example how to use it:
1. First of all you should create some accounts:
> ssh-key-switcher make my_keys
> ssh-key-switcher make company_keys

2. Then identify current keys:
> ssh-key-switcher current company_keys

This operation will copy your keys from "{ssh_dir}" to "{key_storage_dir}/company_keys"

3. You can switch between keys using:
> ssh-key-switcher switch my_keys
or
> ssh-key-switcher switch company_keys

Enjoy it!
""".format(key_storage_dir=KEYS_STORAGE_DIR, ssh_dir=SSH_KEYS_DIR, underline='-' * 15)


def decorate(sep=None, length=None):
    if not sep:
        sep = DECORATE_LINE_SYMBOL
    if not length and not isinstance(length, int):
        length = DECORATE_LINE_LENGTH

    return sep * length


def basename(f):
    return f.split(os.sep)[-1]


def scandir(dir):
    for _, dirs, _ in os.walk(dir):
        return dirs


def init():
    d = scandir(KEYS_STORAGE_DIR)
    if all([os.path.exists(KEYS_STORAGE_DIR), os.path.isdir(KEYS_STORAGE_DIR)]):
        return True
    os.makedirs(KEYS_STORAGE_DIR)
    return True


def list_accounts(args):
    dirs = scandir(KEYS_STORAGE_DIR)
    if not dirs:
        print("There are not any accounts")
    else:
        print("You have the next accounts:")
        print(decorate())
        current = read_current_account()
        for d in dirs:
            sep = '-'
            if d == current:
                sep = '*'
            print('{sep} {dir}'.format(sep=sep, dir=d))


def make_account(args):
    name = '%s/%s' % (KEYS_STORAGE_DIR, args.name)
    if not os.path.exists(name):
        os.mkdir(name)
    return name


def write_current_account(account):
    file_name = '%s/.current' % KEYS_STORAGE_DIR
    f = open(file_name, 'w')
    f.write(account)
    f.close()


def read_current_account():
    account = None
    try:
        file_name = '%s/.current' % KEYS_STORAGE_DIR
        f = open(file_name)
        account = f.readline()
        f.close()
    except:
        pass
    return account


def copy_keys(fr, to):
    for _, _, files in os.walk(fr):
        for f in files:
            source = '%s/%s' % (fr, f)
            dest = '%s/%s' % (to, f)
            shutil.copy2(source, dest) 


def set_current(args):
    name = '%s/%s' % (KEYS_STORAGE_DIR, args.name)
    if not os.path.exists(name):
        raise OSError('Directory does not exist. Make account first')
    
    write_current_account(args.name)
    copy_keys(SSH_KEYS_DIR, name)


def remove_files(directory):
    for _, _, files in os.walk(directory):
        for f in files:
            os.remove('%s/%s' %(directory, f))


def switch_accounts(args):
    from_account = read_current_account()
    to_account = args.name

    copy_keys(SSH_KEYS_DIR, '%s/%s' % (KEYS_STORAGE_DIR, from_account))
    remove_files(SSH_KEYS_DIR)
    copy_keys('%s/%s' % (KEYS_STORAGE_DIR, to_account), SSH_KEYS_DIR)
    write_current_account(to_account)


def parse_args(parser):
    subparsers = parser.add_subparsers()
    subparsers.required = True

    parser_list = subparsers.add_parser('list', help='List accounts')
    parser_list.set_defaults(func=list_accounts)

    parser_make = subparsers.add_parser('create', help='Create a new account')
    parser_make.add_argument('name', help='Name for new account')
    parser_make.set_defaults(func=make_account)

    parser_set_current = subparsers.add_parser('current', help='Set existing account as current')
    parser_set_current.add_argument('name', help='Name of the account')
    parser_set_current.set_defaults(func=set_current)

    parser_switch = subparsers.add_parser('switch', help='Switch to account')
    parser_switch.add_argument('name', help='Name of the account')
    parser_switch.set_defaults(func=switch_accounts)
    
    return parser.parse_args()


def main():
    init()
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    args = parse_args(parser)

    args.func(args)


if __name__ == '__main__':
    try:
        main()
    except OSError as e:
        print(e.message)
        exit(1)
