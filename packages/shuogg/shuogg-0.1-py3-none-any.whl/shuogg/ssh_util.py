'''
SSH提供了2种方式:
    1. 直接执行函数exec_onecmd,exec_multicmd,exec_cmdlist等
    2. new个SSH对象

eg:
exec_cmd('192.168.75.124','root','123456','ifconfig')
exec_cmds('192.168.75.124','root','123456',['cd /home','ls -l'])

ssh1 = SSH('192.168.75.124','root','123456')
ssh1.exec_cmd('ifconfig')
ssh1.exec_cmds(['cd /home','ls -l'])

newstr1 = list_to_cmd(['cd /home', 'ls -l'])
newstr2 = multistr_to_cmd('cd /home', 'ls -l')
'''

import paramiko


def exec_cmd(hostaddr, username, password, cmd):
    """
    执行一条命令
    :param hostaddr:
    :param username:
    :param password:
    :param cmd:
    :return:
    """
    s = paramiko.SSHClient()
    # 读取know_host
    s.load_system_host_keys()
    # 建立SSH连接
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostaddr, 22, username, password)
    stdin, stdout, stderr = s.exec_command(cmd)
    ret_list = []
    for x in stdout.readlines():
        ret_list.append(x.strip())
    s.close()
    return ret_list


def exec_cmds(hostaddr, username, password, cmdlist):
    """
    执行多条命令
    :param hostaddr:
    :param username:
    :param password:
    :param cmdlist:
    :return:
    """
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostaddr, 22, username, password)
    ret_list = []
    for cmd in cmdlist:
        stdin, stdout, stderr = s.exec_command(cmd)
        for x in stdout.readlines():
            ret_list.append(x.strip())
    s.close()
    return ret_list


def list_to_string(ret_list):
    ret_str = ''
    for ret in ret_list:
        ret_str += ret + '\n'
    return ret_str


def __list_to_cmd(strlist):
    """
    ['aa', 'bb', 'cc'] ==> 'aa;bb;cc;'
    :param strlist:
    :return:
    """
    temp_str = ''
    for x in strlist:
        temp_str = temp_str + x + ';'
    return temp_str


def __multistr_to_cmd(*strs):
    """
    ['aa', 'bb', 'cc'] ==> 'aa;bb;cc;'
    :param strs:
    :return:
    """
    temp_str = ''
    for x in strs:
        temp_str = temp_str + x + ';'
    return temp_str


class SSH():
    def __init__(self, hostaddr, username, password):
        super(SSH, self).__init__()
        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostaddr, 22, username, password)

    def __del__(self):
        self.sshclient.close()

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.sshclient.exec_command(cmd)
        ret_list = []
        for x in stdout.readlines():
            ret_list.append(x.strip())
        return ret_list

    def exec_cmds(self, cmdlist):
        for cmd in cmdlist:
            stdin, stdout, stderr = self.sshclient.exec_command(cmd)
            ret_list = []
            for x in stdout.readlines():
                ret_list.append(x.strip())
        return ret_list

    def close(self):
        self.sshclient.close()
