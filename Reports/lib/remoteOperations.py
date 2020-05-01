#!/usr/bin/python
from fabric.api import *
from fabric import network

class remote_ops():

    def __init__(self, **kwargs):
        self.commands = ['uname', 'hostname']
        self.defaultPort = 22

        if 'runMode' in kwargs:
            self.runMode = kwargs['runMode']
        else:
            self.runMode = None

        if 'sshUser' in kwargs:
            self.sshUser = kwargs['sshUser']
        else:
            self.sshUser = None

        if 'sshPassword' in kwargs:
            self.sshPassword = kwargs['sshPassword']
        else:
            self.sshPassword = None

        if 'sshPort' in kwargs:
            self.sshPort = kwargs['sshPort']
        else:
            self.sshPort = None

    def task(self):
        try:
            for cmd in self.commands:
                run(cmd, shell=False)
        except Exception, e:
            print("Unable to run command: " + cmd + '\n '+str(e))

        network.disconnect_all()

    def execute(self, hosts):
        if self.sshUser:
            env.user = self.sshUser

        if self.sshPassword:
            env.password = self.sshPassword

        if self.runMode and self.sshPassword:
            env.parallel = True
        else:
            env.parallel = False

        if self.sshPort:
            env.port = self.sshPort
        else:
            env.port = self.defaultPort

        execute(self.task,hosts=hosts)
