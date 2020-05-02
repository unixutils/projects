#!/usr/bin/python
from fabric.api import *

class remote_ops():

    def __init__(self, **kwargs):

        self.defaultPort = 22

        if 'parallelMode' in kwargs:
            self.parallelMode = kwargs['parallelMode']
        else:
            self.parallelMode = False

        if 'hosts' in kwargs:
            self.hosts = kwargs['hosts']
        else:
            self.hosts = None

        if 'sshUser' in kwargs:
            self.sshUser = kwargs['sshUser']
        else:
            self.sshUser = None

        if 'sshPassword' in kwargs:
            self.sshPassword = kwargs['sshPassword']
        else:
            self.sshPassword = None

        if 'sshKeyFile' in kwargs:
            self.sshKeyFile = kwargs['sshKeyFile']
        else:
            self.sshKeyFile = None

        if 'sshPort' in kwargs:
            self.sshPort = kwargs['sshPort']
        else:
            self.sshPort = None

        if 'commands' in kwargs:
            self.commands = kwargs['commands']
        else:
            self.commands = None

        if 'commandTimeOut' in kwargs:
            self.commandTimeOut = kwargs['commandTimeOut']
        else:
            self.commandTimeOut = None

        if 'excludeHosts' in kwargs:
            self.excludeHosts = kwargs['excludeHosts']
        else:
            self.excludeHosts = None

        if 'sudoPassword' in kwargs:
            self.sudoPassword = kwargs['sudoPassword']
        else:
            self.sudoPassword = None

        if 'connectTimeout' in kwargs:
            self.connectTimeout = kwargs['connectTimeout']
        else:
            self.connectTimeout = None


    def runCommands(self):
        if self.commands:
            try:
                for cmd in self.commands:
                    run(cmd, shell=False)
            except Exception, e:
                raise Exception('Unable to run command: ' + cmd + '\n '+ str(e))
        else:
            raise Exception('No Commands given to run.')


    def executeTask(self):
        env.output_prefix = False
        env.abort_on_prompts = False
        env.disable_known_hosts = True
        env.eagerly_disconnect = True
        env.disable_known_hosts = True

        if self.sshUser:
            env.user = self.sshUser

        if self.sshPassword:
            env.password = self.sshPassword

        if self.sshKeyFile:
            env.key_filename = self.sshKeyFile

        if self.sudoPassword:
            env.sudo_password = self.sudoPassword

        if self.parallelMode and self.sshPassword:
            env.parallel = True
            env.output_prefix = True
        else:
            print("Cannot run Parallel-mode without ssh-password OR ssh-private-key. Switching to Serial-mode.")
            env.parallel = False

        if self.sshPort:
            env.port = self.sshPort
        else:
            env.port = self.defaultPort

        if self.commandTimeOut:
            env.command_timeout = self.commandTimeOut

        if self.excludeHosts:
            env.exclude_hosts = self.excludeHosts

        if self.connectTimeout:
            env.timeout = self.connectTimeout

        if self.hosts:
            execute(self.runCommands, hosts = self.hosts)
        else:
            raise Exception('No hosts given to execute task.')
