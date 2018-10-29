#!/usr/bin/python
# coding:utf-8

import time
import paramiko
import yaml
import os
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


class SshClient:
    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.timeout = 10
        self.connection = None
        self.connect()

    def connect(self):
        ssh_client = paramiko.SSHClient()
        paramiko.util.log_to_file('logs/paramiko.log')
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
                           hostname=self.host,
                           port=self.port,
                           username=self.user,
                           password=self.passwd,
                           timeout=self.timeout
                           )
        self.connection = ssh_client

    def exec_cmd(self, cmd):
        check_os = 'uname'
        res_in, res_out, res_err = self.connection.exec_command(check_os, timeout=60)
        real_os = res_out.read().strip().lower()
        if real_os == 'linux':
            pre_command = '. /etc/profile &> /dev/null;. ~/.bash_profile &> /dev/null;'
        elif real_os == 'aix' or real_os == 'hp_ux':
            pre_command = '. /etc/profile &> /dev/null;. ~/.profile &> /dev/null;'
        else:
            pre_command = ''
        command = '{0}{1}'.format(pre_command, cmd)
        stdin, stdout, stderr = self.connection.exec_command(command, timeout=3600)
        return stdout, stderr

    @staticmethod
    def upload__callback(trans, total):
        sys.stdout.write('upload %10d [%3.2f%%]\r' %(trans, trans*100/int(total)))
        sys.stdout.flush()
        # print 'Data upload %10d [%3.2f%%]\r' % (trans, trans * 100 / int(total)), ;

    @staticmethod
    def download__callback(trans, total):
        sys.stdout.write('download %10d [%3.2f%%]\r' %(trans, trans*100/int(total)))
        sys.stdout.flush()
        # print 'Data download %10d [%3.2f%%]\r' % (trans, trans * 100 / int(total)), ;

    def get_file(self, local_file, remote_file):
        sftp = self.connection.open_sftp()
        sftp.get(remote_file, local_file, callback=self.download__callback)
        sftp.close()

    def up_file(self, local_file, remote_file):
        sftp = self.connection.open_sftp()
        sftp.put(local_file, remote_file, callback=self.upload__callback)
        sftp.close()

    def close_connect(self):
        self.connection.close()


def module_lists(config_file='config/module.yml'):
    f = open(config_file, 'r')
    lines = f.read()
    res = yaml.load(lines)
    lists = []
    for i in res['services']:
        lists.append(res['services'][i])
    return lists


def server_lists(config_file='config/module.yml'):
    f = open(config_file, 'r')
    lines = f.read()
    res = yaml.load(lines)
    __local = res['servers']['local_host']
    __remote = res['servers']['remote_host']
    __static = res['servers']['static_host']
    return __local, __remote, __static

def get_file(action='compose', config_file='config/module.yml'):
    f = open(config_file, 'r')
    lines = f.read()
    res = yaml.load(lines)
    res = res[action]['file']
    return res

def download(module, localhost):
    ssh1 = SshClient(host=localhost['host'], port=localhost['port'], user=localhost['user'], passwd=localhost['passwd'])
    remote_path = module['path']
    remote_zip = '{0}.zip'.format(remote_path)
    zip_cmd = 'zip -rq {0} {1}; #@{2}'.format(remote_zip, remote_path, localhost['host'])
    out, out_err = ssh1.exec_cmd(zip_cmd)
    print(zip_cmd)
    out.read()
    out_err.read()
    local = './tmp/{0}'.format(os.path.basename(remote_zip))
    print('download: {0} from {1}'.format(module['container_name'], localhost['host']))
    ssh1.get_file(local_file=local, remote_file=remote_zip)
    print('')
    delete_zip = 'rm -f {0}; #@{1}'.format(remote_zip, localhost['host'])
    out, out_err = ssh1.exec_cmd(delete_zip)
    print(delete_zip)
    out.read()
    out_err.read()
    ssh1.close_connect()


def backup(module, remotehost):
    remote_path = module['path']
    ssh = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'],
                    passwd=remotehost['passwd'])
    localtime = time.time()
    date = time.strftime('%Y%m%d%H%M%S', time.localtime(localtime))
    cmd = '/bin/cp -a {0} {0}_{1}; #@{2}'.format(remote_path, date, remotehost['host'])
    out, out_err = ssh.exec_cmd(cmd)
    print(cmd)
    out.read()
    out_err.read()
    ssh.close_connect()


def upload(module, remotehost):
    remote_path = module['path']
    remote_zip = '{0}.zip'.format(remote_path)
    local = './tmp/{0}'.format(os.path.basename(remote_zip))
    ssh2 = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'],
                     passwd=remotehost['passwd'])
    print('upload: {0} to {1}').format(module['container_name'], remotehost['host'])
    ssh2.up_file(local, '/{0}'.format(os.path.basename(remote_zip)))
    print ('')
    delete_path = 'rm -rf {0}; #@{1}'.format(remote_path, remotehost['host'])
    out, out_err = ssh2.exec_cmd(delete_path)
    print(delete_path)
    out.read()
    out_err.read()
    unzip_cmd = 'unzip -oq -d / /{0}; #@{1}'.format(os.path.basename(remote_zip), remotehost['host'])
    out, out_err = ssh2.exec_cmd(unzip_cmd)
    print(unzip_cmd)
    out.read()
    out_err.read()
    delete_zip = 'rm -f /{0}; #@{1}'.format(os.path.basename(remote_zip), remotehost['host'])
    out, out_err = ssh2.exec_cmd(delete_zip)
    print(delete_zip)
    out.read()
    out_err.read()
    ssh2.close_connect()


def get_compose_file(compose, localhost, remotehost):
    ssh1 = SshClient(host=localhost['host'], port=localhost['port'], user=localhost['user'], passwd=localhost['passwd'])
    remote_path = compose['path']
    local = './tmp/{0}'.format(os.path.basename(remote_path))
    print('download: {0} from {1}').format(remote_path, localhost['host'])
    ssh1.get_file(local_file=local, remote_file=remote_path)
    print('')
    ssh1.close_connect()
    ssh2 = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'],
                     passwd=remotehost['passwd'])
    print('upload: {0} to {1}').format(remote_path, remotehost['host'])
    ssh2.up_file(local, remote_path)
    print('')
    ssh2.close_connect()


def get_static_file(static, localhost, statichost):
    ssh1 = SshClient(host=localhost['host'], port=localhost['port'], user=localhost['user'], passwd=localhost['passwd'])
    static_path = static['path']
    static_zip = '{0}.zip'.format(static_path)
    zip_cmd = 'zip -rq {0} {1}; #@{2}'.format(static_zip, static_path, localhost['host'])
    out, out_err = ssh1.exec_cmd(zip_cmd)
    print(zip_cmd)
    out.read()
    out_err.read()
    local = './tmp/{0}'.format(os.path.basename(static_zip))
    print('download: {0} from {1}').format(static_path, localhost['host'])
    ssh1.get_file(local_file=local, remote_file=static_zip)
    print('')
    delete_zip = 'rm -f {0}; #@{1}'.format(static_zip, localhost['host'])
    out, out_err = ssh1.exec_cmd(delete_zip)
    print(delete_zip)
    out.read()
    out_err.read()
    ssh1.close_connect()

    ssh2 = SshClient(host=statichost['host'], port=statichost['port'], user=statichost['user'],
                     passwd=statichost['passwd'])
    localtime = time.time()
    date = time.strftime('%Y%m%d%H%M%S', time.localtime(localtime))
    cmd = '/bin/cp -a {0} {0}_{1}; #@{2}'.format(static_path, date, statichost['host'])
    out, out_err = ssh2.exec_cmd(cmd)
    print(cmd)
    out.read()
    out_err.read()
    print('upload: {0} to {1}').format(static_path, statichost['host'])
    ssh2.up_file(local, '/{0}'.format(os.path.basename(static_zip)))
    print('')
    delete_path = 'rm -rf {0}; #@{1}'.format(static_path, statichost['host'])
    out, out_err = ssh2.exec_cmd(delete_path)
    print(delete_path)
    out.read()
    out_err.read()
    unzip_cmd = 'unzip -oq -d / /{0}; #@{1}'.format(os.path.basename(static_zip), statichost['host'])
    out, out_err = ssh2.exec_cmd(unzip_cmd)
    print(unzip_cmd)
    out.read()
    out_err.read()
    delete_zip = 'rm -f /{0}; #@{1}'.format(os.path.basename(static_zip), statichost['host'])
    out, out_err = ssh2.exec_cmd(delete_zip)
    print(delete_zip)
    out.read()
    out_err.read()
    ssh2.close_connect()


def start_service(module, compose, remotehost):
    cmd = "cat {0}|grep build:|cut -d : -f 2|xargs mkdir -p".format(compose['path'])
    ssh = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'], passwd=remotehost['passwd'])
    out, out_err = ssh.exec_cmd(cmd)
    out.read()
    out_err.read()

    stop_cmd = "docker-compose -f {0} stop {1}".format(compose['path'], module['container_name'])
    out, out_err = ssh.exec_cmd(stop_cmd)
    print(out.read())
    print(out_err.read())

    rm_cmd = "docker-compose -f {0} rm -f {1}".format(compose['path'], module['container_name'])
    out, out_err = ssh.exec_cmd(rm_cmd)
    print(out.read())
    print(out_err.read())

    start_cmd = "docker-compose -f {0} up --build -d {1}".format(compose['path'], module['container_name'])
    out, out_err = ssh.exec_cmd(start_cmd)
    print(out.read())
    print(out_err.read())

def check_service(modulename, remotehost):
    cmd = "/usr/bin/docker ps 2>/dev/null|grep -w {0}|grep -w healthy|wc -l".format(modulename)
    ssh = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'], passwd=remotehost['passwd'])
    out, out_err = ssh.exec_cmd(cmd)
    res = out.read().strip()
    out_err.read()
    return res

def get_service_logs(modulename, remotehost):
    cmd = "/usr/bin/docker logs {0}".format(modulename)
    ssh = SshClient(host=remotehost['host'], port=remotehost['port'], user=remotehost['user'], passwd=remotehost['passwd'])
    out, out_err = ssh.exec_cmd(cmd)
    res = out.read().strip()
    out_err.read()
    return res