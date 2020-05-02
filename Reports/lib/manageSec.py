#!/usr/bin/python
import os
import sys
from cryptography.fernet import Fernet
from manageInventory import manage_host_config

class manage_sec(manage_host_config):
    def __init__(self, **kwargs):
        super(manage_sec, self).__init__()

    def generateKey(self):
        return Fernet.generate_key()

    def createKeyFile(self):
        with open("key.key", "wb") as key_file:
            key_file.write(self.generateKey())

    def getKeyFromFile(self):
        KeyFile = open("key.key", "rb").read()
        cip = Fernet(KeyFile)
        return cip

    def encryptPassword(self, defaultSshPassword):
        self.createKeyFile()
        key = self.getKeyFromFile()
        encodedSecret = key.encrypt(defaultSshPassword)
        return encodedSecret

    def decryptPassword(self):
        key = self.getKeyFromFile()
        return key.decrypt(self.getDefaultEncryptedSshPassword())
        
    def storeEncryptedPassword(self):
        encryptedPassword = self.encryptPassword()
        self.setDefaultEncryptedSshPassword(encryptedPassword)
