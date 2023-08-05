#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
import configparser
import os
import gevent
import time


GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)

def print_success(msg='Success!'):
    click.secho(msg, fg='cyan')

def print_failed(msg='Failed!'):
    click.secho(msg, fg='red')

def print_progress(msg='Waiting...'):
    click.secho(msg, fg='yellow')

def print_error(msg):
    click.secho(msg, fg='red')

def make_progress_msg(msg):
    return click.style(msg, fg = 'yellow')

def make_error_msg(msg):
    return click.style(msg, fg = 'red')

def config(filepath, section, **data):
    conf = configparser.ConfigParser()
    if os.path.exists(filepath):
        conf.read(filepath)

    val = conf[section]
    if val:
        data.update(val)

    conf[section] = data

    with open(filepath, 'w') as f:
        conf.write(f)
        f.close()

is_done = False

def print_dynamic_progress(msg = 'Waiting...'):
    print('begin progress')
    gevent.sleep(0)
    count = 0
    pl = ('⠸' ,'⠼' ,'⠴' ,'⠦' ,'⠧' ,'⠏' ,'⠙' ,'⠹')
    while count < 10000:
        for p in pl:
            print(f'{p} {msg}', end='\r')
        count += 1
    print('Success!       ')

def work():
    print('begin work')
    gevent.sleep(0)
    time.sleep(2)
    is_done = True
    print('end work')

class Progress():
    is_done = False
    is_waiting = True

    def print_dynamic_progress(self, msg = 'Waiting...'):
        print('begin progress')
        pl = ('⠸' ,'⠼' ,'⠴' ,'⠦' ,'⠧' ,'⠏' ,'⠙' ,'⠹')
        while not self.is_done:
            print(self.is_done, self.is_waiting)
            while self.is_waiting:
                for p in pl:
                    print(msg)
                    print(f'{p} {msg}', end='\r')
        print('Success!       ')

if __name__ == "__main__":
    #  gevent.joinall([
        #  gevent.spawn(work),
        #  gevent.spawn(print_dynamic_progress),
    #  ])
    print_dynamic_progress()


