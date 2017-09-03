#!/usr/local/bin/python3
import argparse
import os
import sys
import shutil

HOME_DIR = os.path.expanduser('~')
SSH_KEYS_DIR = '%s/.ssh' % HOME_DIR
KEYS_STORAGE_DIR = '%s/.ssh-key-switcher' % HOME_DIR

def basename(f):
    return f.split('/')[-1]

def init():
    if all([os.path.exists(KEYS_STORAGE_DIR), os.path.isdir(KEYS_STORAGE_DIR)]):
        return True
    os.makedirs(KEYS_STORAGE_DIR, exist_ok=False)
    return True


def list_accounts(args):
    dirs = [basename(f.path) for f in os.scandir(KEYS_STORAGE_DIR) if f.is_dir()]
    if not dirs:
        print("There are not any accounts")
    else:
        for dir in dirs:
            print(dir)


def make_account(args):
    name = '%s/%s' % (KEYS_STORAGE_DIR, args.name)
    if not os.path.exists(name):
        os.mkdir(name)
    return name

def help(args):
    print("Switch keys between accounts for .ssh")


def write_current_account(account):
    file_name = '%s/.current' % KEYS_STORAGE_DIR
    f = open(file_name, 'w')
    f.write(account)
    f.close()

def read_current_account():
    file_name = '%s/.current' % KEYS_STORAGE_DIR
    f = open(file_name)
    account  =f.readline()
    f.close()
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


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(description='User database utility')
    subparsers = parser.add_subparsers()
    subparsers.required = True

    parser_help = subparsers.add_parser('help', help='Help of the command')
    parser_help.set_defaults(func=help)

    parser_list = subparsers.add_parser('list', help='List accounts')
    parser_list.set_defaults(func=list_accounts)

    parser_make = subparsers.add_parser('make', help='List accounts')
    parser_make.add_argument('name', help='Name of new account')
    parser_make.set_defaults(func=make_account)

    parser_make = subparsers.add_parser('make', help='List accounts')
    parser_make.add_argument('name', help='Name of new account')
    parser_make.set_defaults(func=make_account)

    parser_set_current = subparsers.add_parser('current', help='Set a current account')
    parser_set_current.add_argument('name', help='Name of the account')
    parser_set_current.set_defaults(func=set_current)

    parser_switch = subparsers.add_parser('switch', help='Switch to account')
    parser_switch.add_argument('name', help='Name of the account')
    parser_switch.set_defaults(func=switch_accounts)
    
    return parser.parse_args()


def main():
    init()
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
