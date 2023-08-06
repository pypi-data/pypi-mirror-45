import os
import os.path as path
from git import Repo
import subprocess
import paramiko
from Crypto.PublicKey import RSA
import json


def create(args):
    name = args.name
    create_dir = path.join(os.getcwd(), name)
    git_dir = path.join(create_dir, '.git')
    ignore_path = path.join(path.dirname(path.abspath(__file__)), 'template.gitignore')
    gitignore_path = path.join(create_dir, '.gitignore')
    egret_name = 'egret-{0}'.format(name)
    egret_dir = path.join(create_dir, egret_name)
    egret_src = path.join(egret_dir, 'src')
    submodule_dir = path.join(egret_src, 'ef')

    repo = None
    if make_dir(create_dir):
        repo = Repo.init(create_dir, '.git')
        f = open(ignore_path, 'r')
        gitignore = f.read()
        f.close()

        if not(path.isfile(gitignore_path)):
            f = open(gitignore_path, 'w')
            f.write(gitignore)
            f.close()

        repo.git.add('*')
        repo.git.commit('-m init')
    else:
        repo = Repo.init(create_dir, '.git')

    # egret project
    if not(path.isdir(egret_dir)):
        subprocess.call(['egret', 'create', egret_dir, '--type', 'eui'], shell=True)
    repo.git.add('*')
    repo.git.commit('-m create egret')

    git_username = input('git username: ')

    host = 'git.emonggames.com'
    port = '29418'
    protocol = 'ssh://'
    home = path.expanduser('~')

    remote = '{0}{1}:{2}'.format(protocol, host, port)
    user_remote = '{0}{1}@{2}:{3}'.format(protocol, git_username, host, port)

    ssh_path = path.join(home, '.ssh')
    ssh_rsa = path.join(ssh_path, 'id_rsa')
    ssh_rsa_pub = path.join(ssh_path, 'id_rsa.pub')
    if make_dir(ssh_path):
        key = RSA.generate(1024)
        f = open(ssh_rsa, 'wb')
        f.write(key.exportKey('PEM'))
        f.close()

        pub = key.publickey()
        f = open(ssh_rsa_pub, 'wb')
        f.write(pub.exportKey('OpenSSH'))
        f.close()

    if path.isfile(ssh_rsa_pub):
        f = open(ssh_rsa_pub, 'r')
        key = f.read()
        f.close()
        print(key)

    # ssh_key_dir = path.join(create_dir, 'ssh-key')
    # if make_dir(ssh_key_dir):
    #     key = RSA.generate(1024)
    #     f = open(path.join(ssh_key_dir, 'id_rsa'), 'wb')
    #     f.write(key.exportKey('PEM'))
    #     f.close()
    #
    #     pub = key.publickey()
    #     f = open(path.join(ssh_key_dir, 'id_rsa.pub'), 'wb')
    #     f.write(pub.exportKey('OpenSSH'))
    #     f.close()

    input('regist ssh key to git server and press enter')

    known_host_path = path.join(ssh_path, 'known_hosts')
    if not path.isfile(known_host_path):
        f = open(known_host_path, 'w')
        f.close()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_host_keys(known_host_path)
    ssh.connect(hostname=host, port=port, username=git_username)
    ssh.close()

    # return
    # with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
    if not path.isdir(submodule_dir):
        repo.git.submodule('add', '{0}/emong/egret-framework.git'.format(user_remote), './{0}/src/ef'.format(egret_name), b='local-submodule')

    external_lib_name = 'external-lib'
    external_lib_path = path.join(create_dir, external_lib_name)
    if not path.isdir(external_lib_path):
        repo.git.submodule('add', '{0}/emong/egret-framework.git'.format(user_remote), './{0}'.format(external_lib_name), b=external_lib_name)

    repo.git.add('*')
    repo.git.commit('-m add submodule')

    remove_files = [
        'Main.ts',
        'Platform.ts',
        'LoadingUI.ts'
    ]

    for file in remove_files:
        file_path = path.join(egret_src, file)
        if path.isfile(file_path):
            os.remove(file_path)

    main_template_path = path.join(submodule_dir, 'template', 'main.template')
    main_template = ''
    if path.isfile(main_template_path):
        f = open(main_template_path, 'r')
        main_template = f.read()
        f.close()

    maints_path = path.join(egret_src, 'Main.ts')
    if not path.isfile(maints_path):
        f = open(maints_path, 'w')
        f.write(main_template)
        f.close()

    egret_properties_path = path.join(egret_dir, 'egretProperties.json')
    if path.isfile(egret_properties_path):
        data = None
        with open(egret_properties_path, 'r+') as file:
            data = json.load(file)

        modules = data['modules']
        add_module = {}
        add_module['name'] = 'crypto-js'
        add_module['path'] = '../external-lib/crypto-js'
        modules.append(add_module)

        if not(data is None):
            with open(egret_properties_path, 'wt') as file:
                json.dump(data, file)

    repo.git.add('*')
    repo.git.commit('-m init egret Main.ts')


def make_dir(dir):
    try:
        if not(path.isdir(dir)):
            os.makedirs(dir)
            return True
        else:
            return False
    except OSError as e:
        if e.errno != e.errno.EEXIST:
            print('Failed to create directory')
            raise

