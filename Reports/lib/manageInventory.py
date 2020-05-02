#!/bin/python
import os
import sys
import yaml

here = os.path.dirname(os.path.realpath(__file__))

class manage_host_config(object):
    def __init__(self, **kwargs):
        self.configFile = os.path.join(here, "..", "dat", "inventory.yaml")
        self.hostConfig = self.loadHostConfig()

    def loadHostConfig(self):
        with open(self.configFile, 'r') as stream:
            try:
                host_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise Exception('Unable to read inventory.')
            return host_config

    def getGroups(self):
        return self.hostConfig['host_config']['groups'].keys()

    def getHosts(self, groupName = None):
        hostList = []
        if not groupName:
            for group in self.getGroups():
                for host in self.hostConfig['host_config']['groups'][group].keys():
                    hostList.append(host)
        else:
            if self.groupExists(groupName):
                host = self.hostConfig['host_config']['groups'][self.groupName].keys()
                hostList.append(host)
        return hostList

    def getHostGroup(self, hostName):
        if self.hostExists(hostName):
            for group in self.getGroups():
                if hostName in self.hostConfig['host_config']['groups'][group].keys():
                    return group
        else:
            raise Exception(hostName + ' ' + 'does not exist.')

    def groupExists(self, groupName):
        if groupName in self.getGroups():
           return True
        else:
           return False

    def hostExists(self, hostName):
        if hostName in self.getHosts():
           return True
        else:
           return False

    def addGroup(self, groupName):
        if not self.groupExists(groupName):
            self.hostConfig['host_config']['groups'].update({groupName:{}})
        else:
            raise Exception('"' + groupName + '"' + ' ' + 'already exists.')

    def addHost(self, hostName, groupName):
        if not self.hostExists(hostName):
            if self.groupExists(groupName):
                self.hostConfig['host_config']['groups'][groupName].update({hostName:''})
            else:
                raise Exception('"' + groupName + '"' + ' ' + 'does not exists.')
        else:
            raise Exception('"' + hostName + '"' + ' ' + 'already exists.')

    def deleteGroup(self):
        if self.groupExists():
            self.hostConfig['host_config']['groups'].pop(self.groupName)
        else:
            raise Exception( 'group:' + '"' + self.groupName + '"' + ' ' + 'does not exists.')
    
    def deleteHost(self):
        if self.hostExists():
            group = self.getHostGroup()
            self.hostConfig['host_config']['groups'][group].pop(self.hostname)
        else:
            raise Exception( 'host:' + '"' + self.hostName + '"' + ' ' + 'does not exists.')

    def setDefaultUser(self, defaultUser):
            self.hostConfig['host_config'].update({'default_user':defaultUser})

    def getDefaultUser(self):
        if self.hostConfig['host_config']['default_user'].strip() != '':
            defaultInventoryUser = self.hostConfig['host_config']['default_user']
        else:
            defaultInventoryUser = None
        return defaultInventoryUser

    def deleteDefaultUser(self):
        self.hostConfig['host_config'].update({'default_user':''})

    def setDefaultSshKey(self, defaultSshKey):
        if self.keyExists(defaultSshKey):
            self.hostConfig['host_config'].update({'default_ssh_key_path':defaultSshKey})
        else:
            raise Exception('Key file: {} does not exists.'.format(defaultSshKey))

    def getDefaultSshKey(self):
        if not self.hostConfig['host_config']['default_ssh_key_path']:
            defaultInventorySshKeyPath = self.hostConfig['host_config']['default_ssh_key_path']
            if self.keyExists(str(defaultInventorySshKeyPath)):
                defaultInventorySshKey = defaultInventorySshKeyPath
            else:
                defaultInventorySshKey = None
        else:
            defaultInventorySshKey = None
        return defaultInventorySshKey
     
    def deleteDefaultSshKey(self):
        self.hostConfig['host_config'].update({'default_ssh_key_path':''})

    def setDefaultEncryptedSshPassword(self, defaultEncryptedSshPassword):
        self.hostConfig['host_config'].update({'default_password_encrypted':defaultEncryptedSshPassword})

    def getDefaultEncryptedSshPassword(self):
        if self.hostConfig['host_config']['default_password_encrypted'].strip() != '':
            defaultEncrypedSshPassword = self.hostConfig['host_config']['default_password_encrypted']
        else:
            defaultEncrypedSshPassword = None
        return defaultEncrypedSshPassword

    def deleteDefaultEncryptedSshPassword(self):
        self.hostConfig['host_config'].update({'default_password_encrypted':''})

    def keyExists(self, key):
        if os.path.exists(key):
            return True
        else:
            return False
