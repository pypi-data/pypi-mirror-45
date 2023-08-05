from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from pathlib import Path
import sys


def transfer(host, username, password, project_path, to_path='.'):
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        with SFTPClient.from_transport(ssh.get_transport()) as sftp:
            _transferring(ssh, sftp, Path(project_path), to_path)
    return 'Successful!'


def _transferring(ssh, sftp, file_path, root_path):
    root_path = f'{root_path}/{file_path.name}'
    if file_path.is_dir():
        ssh.exec_command(f'mkdir -p {root_path}')[1].read()
        for f in file_path.iterdir():
            _transferring(ssh, sftp, file_path / f.name, root_path)
    else: sftp.put(file_path, root_path)


def main():
    params = sys.argv[1:]
    if len(params) == 4: host, username, password, to_path = params
    elif len(params) == 3:
        host, username, password = params
        to_path = '.'
    else: return 'Error: please check the command (propor <host> <username> <password> <to_path>).'
    return transfer(host, username, password, Path.cwd(), to_path)
