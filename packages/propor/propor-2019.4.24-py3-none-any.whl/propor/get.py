from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from pathlib import Path
import sys


def download(host, username, password, local_path, remote_path):
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        with SFTPClient.from_transport(ssh.get_transport()) as sftp:
            _transferring(sftp, remote_path, local_path)
    return 'Successful!'


def _transferring(sftp, file_path, root_path):
    file_name = file_path.split('/')[-1]
    root_path = root_path / file_name
    if '.' in file_name: sftp.get(file_path, root_path)
    else:
        Path(root_path).mkdir(parents=True, exist_ok=True)
        files = sftp.listdir(file_path)
        for f in files: _transferring(sftp, f'{file_path}/{f}', root_path)


def get():
    params = sys.argv[1:]
    if len(params) == 4: host, username, password, remote_path = params
    else: return 'Error: please check the command (propor-get <host> <username> <password> <remote_path>).'
    return download(host, username, password, Path.cwd(), remote_path)
