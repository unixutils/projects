#!/bin/python
import os
import sys
import yaml

here = os.path.dirname(os.path.realpath(__file__))

class manage_host_config:
    def __init__(self, **kwargs):
        self.configFile = os.path.join(here, "..", "dat", "inventory.yaml")
        if 'groupName' in kwargs:
            self.groupName = kwargs['groupName']
        else:
            self.groupName = 'all'
        if 'hostName' in kwargs:
            self.hostName = kwargs['hostName']
        else:
            self.hostName = 'all'
        self.hostConfig = self.loadHostConfig()
        self.hostparams = self.hostConfig['host_config']['valid_host_params']
        for param in self.hostparams:
            if locals()['param'] not in kwargs:
               kwargs[locals()['param']] = 'NULL'
            setattr(self, locals()['param'], kwargs[locals()['param']])

    def loadHostConfig(self):
        with open(self.configFile, 'r') as stream:
            try:
                host_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise Exception('Unable to read inventory.')
            return host_config

    def getGroups(self):
        return self.hostConfig['host_config']['groups'].keys()

    def getHosts(self):
        hostList = []
        if self.groupName == 'all':
            for group in self.getGroups():
                for host in self.hostConfig['host_config']['groups'][group].keys():
                    hostList.append(host)
        else:
            if self.groupExists():
                host = self.hostConfig['host_config']['groups'][self.groupName].keys()
                hostList.append(host)
        return hostList

    def getHostGroup(self):
        if self.hostExists():
            for group in self.getGroups():
                if self.hostName in self.hostConfig['host_config']['groups'][group].keys():
                    return group
        else:
            raise Exception(self.hostName + ' ' + 'does not exist.')

    def getHostInfo(self):
        hostInfoDict = {}
        if self.hostName == 'all':
           for group in self.getGroups():
               for host in self.hostConfig['host_config']['groups'][group].keys():
                   hostInfo = self.hostConfig['host_config']['groups'][group][host]
                   hostInfoDict.update({host : hostInfo})
        elif self.hostExists():
            group = self.getHostGroup()
            hostInfo = self.hostConfig['host_config']['groups'][group][self.hostName]
            hostInfoDict.update({self.hostName : hostInfo})
        else:
            raise Exception(self.hostName + ' ' + 'does not existsss.')
        return hostInfoDict

    def groupExists(self):
        if self.groupName in self.getGroups():
           return True
        else:
           return False

    def hostExists(self):
        if self.hostName in self.getHosts()[0]:
           return True
        else:
           return False

    def validateNewGroupParams(self):
        if self.groupName == 'all':
            raise Exception('Group name cannot be "all"')
        elif self.groupExists():
            raise Exception(self.groupName + ' ' + 'already exists.')
        else:
            return True

    def addNewGroup(self):
        if self.validateGroupParams():
            self.hostConfig['host_config']['groups'].update({self.groupName:''})

    def validateNewHostParams(self):
        param_missing = False
        for param in self.hostparams:
           if not hasattr(self, locals()['param']) or getattr(self, locals()['param']) == 'NULL':
              param_missing = True
        if self.hostName == 'all':
            raise Exception('Host name cannot be "all"')
        elif self.hostExists():
            raise Exception('"' + self.hostName + '"' + ' ' + 'already exists.')
        elif not self.groupExists():
            raise Exception('"' + self.groupName + '"' + ' ' + 'does not exists.')
        elif param_missing:
            raise Exception('Requires' + ' ' + str(self.hostparams) + ' ' + 'parameteres to add host' + ' ' + self.hostName)
        else:
            return True

    def addNewHost(self):
        if self.validateNewHostParams():
            hostNameDict = {self.hostName : {}}
            for param in self.hostparams:
                hostNameDict[self.hostName].update({ locals()['param'] : getattr(self, locals()['param'])})
            self.hostConfig['host_config']['groups'][self.groupName].update(hostNameDict)

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
