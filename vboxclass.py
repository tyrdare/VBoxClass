import paramiko
import sys
import subprocess


class VBoxServer:
    vbox_command = "/home/user/bin/vboxmanage"

    def __init__(self, host: str, username: str, password: str):
        self.__user = username
        self.__password = password
        self.__host = host
        self.ssh_conn = None

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str):
        if password:
            self.__password = password

    @property
    def user(self) -> str:
        return self.__user

    @user.setter
    def user(self, username: str):
        if username:
            self.__user = username

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, hostname):
        self.__host = hostname

    def connect_to_server(self):
        if not self.__host or not self.__user or not self.__password:
            raise paramiko.SSHException("host, user or password field is empty")
        self.ssh_conn = paramiko.SSHClient()
        self.ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_conn.connect(
            self.__host, username=self.__user, password=self.__password
        )

    def running_vms(self) -> str:
        cmd = [self.vbox_command, "list", "runningvms"]
        if self.ssh_conn is None:
            # assume we are running commands locally
            output = subprocess.check_output(cmd)
        else:
            stdin, stdout, stderr = self.ssh_conn.exec_command(cmd)
            output = stdout.read()
        return output

    def registered_vms(self) -> str:
        cmd = [self.vbox_command, "list", "vms"]
        if self.ssh_conn is None:
            output = subprocess.check_output(cmd)
        else:
            stdin, stdout, stderr = self.ssh_conn.exec_command(cmd)
            output = stdout.read()
        return output

    def is_running(self, name_or_uuid: str) -> bool:
        if name_or_uuid in self.running_vms():
            return True
        return False

    def is_registered(self, name_or_uuid: str) -> bool:
        if name_or_uuid in self.registered_vms():
            return True
        return False
