#!/bin/python3
# -*- coding:utf-8 -*-

import os
import paramiko
import psycopg2


class NodeSSH:

    def __init__(self, ip, user, pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd

        self.ssh = None
        self.sftp = None

        self.root_path = os.path.dirname(os.path.dirname(__file__))
        self.login()

    def login(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, username=self.user, password=self.pwd)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        self.ssh = ssh
        self.sftp = sftp

    def check_ssh(self):
        try:
            assert self.ssh
            self.ssh.exec_command("\n")
        except ConnectionError:
            return False
        return True

    def send_cmd(self, command, timeout=600, logFlag=True):
        if self.check_ssh():
            print("=> " + command) if logFlag else None
            std_in, std_out, std_err = self.ssh.exec_command(command, timeout=timeout)
            res = std_out.read().decode()
            ret = std_err.read().decode()
            result = res if res else ret
            print("<= " + result) if logFlag else None
        else:
            raise ConnectionError("connect error!")
        return result

    def push_file(self, local_file, remote_file):
        self.sftp.put(local_file, remote_file)

    def download_file(self, local_file, remote_file):
        self.sftp.get(local_file, remote_file)


class DbConnect:
    def __int__(self):
        pass

    def connect(self):
        psycopg2.connect()
        pass

    def send_sql(self):
        pass

    def check_connect(self):
        pass


class Cluster:
    def __int__(self):
        pass
