import os
import os.path as path
from git import Repo
from git import Git
import subprocess


def create(args):
    name = args.name
    create_dir = path.join(os.getcwd(), name)
    git_dir = path.join(create_dir, '.git')
    ignore_path = path.join(path.dirname(path.abspath(__file__)), 'templete.gitignore')
    gitignore_path = path.join(create_dir, '.gitignore')
    egret_name = 'egret-{0}'.format(name)
    egret_dir = path.join(create_dir, egret_name)
    submodule_dir = path.join(create_dir, egret_dir, 'src', 'ef')

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

    # repo.git.branch()
    # repo.git.checkout('HEAD', b='master')
    # subprocess.run(['egret', 'create', 'egret-{0}'.format(name), '--type', 'eui'])

    if not(path.isdir(egret_dir)):
        subprocess.call(['egret', 'create', egret_dir, '--type', 'eui'], shell=True)


    git_username = input('git username: ')
    domain = 'git.emonggames.com:29418'
    protocol = 'ssh://'
    remote = protocol + domain
    user_remote = '{0}{1}@{2}'.format(protocol, git_username, domain)
    print(remote)
    print(user_remote)

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

    # git_ssh_cmd = 'ssh -o StrictHostKeyChecking=no ssh://qkrsogusl3@git.emonggames.com:29418'

    git_ssh_cmd = 'ssh {0}'.format(user_remote)
    # git_ssh_cmd = 'ssh -o StrictHostKeyChecking=no ssh://qkrsogusl3@git.emonggames.com:29418'
    print(git_ssh_cmd)

    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', 'ssh://qkrsogusl3@git.emonggames.com:29418'], shell=True)

    # return
    with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
        repo.git.submodule('add', 'ssh://qkrsogusl3@git.emonggames.com:29418/emong/egret-framework.git', './{0}/src/ef'.format(egret_name), b='local-submodule')


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

