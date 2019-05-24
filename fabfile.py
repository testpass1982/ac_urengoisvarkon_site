from fabric.api import *
from fabric.contrib import files
from fabric.contrib.files import exists
from fabric.colors import green, red
from fabric.contrib import project
import time
import json
import os
import zipfile


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('tmp/', zipf)
    zipf.close()

# env.use_ssh_config = False
# env.disable_known_hosts = True
# from fabric import Connection
# https://micropyramid.com/blog/automate-django-deployments-with-fabfile/

if os.name == 'nt':
    p = 'python'
else:
    p = 'python3'

try:
    with open("secret.json") as secret_file:
        secret = json.load(secret_file)
        env.update(secret)
        # env.hosts = secret['hosts']
except FileNotFoundError:
    print('***ERROR: no secret file***')

PATH_TO_PROJECT = '{}/{}/'.format(env.path_to_projects, env.project_name)

#check if os is not windows
if os.name != 'nt':
    env.use_ssh_config = True
    env.hosts = ['server']

def test_connection():
    # get_secret()
    run('ls -la')
    run('uname -a')

def backup():
    print(green('pulling remote repo...'))
    local('git pull')
    print(green('adding all changes to repo...'))
    local('git add .')
    print(green("enter your comment:"))
    comment = input()
    local('git commit -m "{}"'.format(comment))
    print(green('pushing master...'))
    local('git push -u origin master')

@runs_once
def remote_migrate():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        # run('cd {}{}'.format(env.path_to_projects, env.project_name))
        with prefix(env.activate):
            run('{} manage.py makemigrations --noinput'.format(p))
            run('{} manage.py migrate --noinput'.format(p))
            run('deactivate')

def local_migrate():
    local('{} manage.py makemigrations'.format(p))
    local('{} manage.py migrate'.format(p))

def app_migrate(app):
        with cd('{}{}'.format(env.path_to_projects, env.project_name)):
            with prefix(env.activate):
                run('pwd')
                run('{} manage.py makemigrations {}'.format(p, app))
                run('{} manage.py migrate {}'.format(p, app))
                run('deactivate')
                print(green('app {} migrated'.format(app)))
# def activate_virtualenv():

# def deactivate():

def create_superuser():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        with prefix(env.activate):
            run('pwd')
            run('{} manage.py init_admin'.format(p))
            run('deactivate')
            print(green('superuser created'))

def check_exists(filename):
    if files.exists(filename):
        print(green('YES {} exists!'.format(filename)))
        return True
    else:
        print(red('{} NOT exists!'.format(filename)))
        return False

def test_remote_folder():
    execute(check_exists, '{}{}'.format(env.path_to_projects, env.project_name))

def test():
    local('{} manage.py test'.format(p))

#as user
def clone():
    print(green('CLONING...'))
    run('git clone {}'.format(env.git_repo))

#as user
def update():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        print(green('UPDATING...'))
        run('git pull')

#as user
def make_configs():
    local("sed 's/PROJECT_NAME/{}/g; \
                s/DOMAIN_NAME/{}/g; \
                s/USERNAME/{}/g' \
            nginx_config_template > {}_nginx".format(
        env.project_name, env.domain_name, env.user, env.project_name))
    print(green('***NGINX CONFIG READY***'))
    local("sed 's/PROJECT_NAME/{}/g; \
                s/USERNAME/{}/g' \
            systemd_config_template > {}.service".format(
        env.project_name, env.user, env.project_name))
    print(green('***SYSTEMD CONFIG READY***'))
    print(green("""
************************
****CONFIGS COMPLETE****
************************
    """))

#as sudo
# def copy_systemd_config():
#     run('cp {}.service /etc/systemd/system/{}.service'.format(env.project_name))
#     run('cd /etc/systemd/system/')
#     run('systemctl enable {}.service'.format(env.project_name))
#     run('systemctl start {}.service'.format(env.project_name))

#as sudo
def copy_nginx_config():
    print(green('checking nginx-configuration'))
    # put('{}_nginx'.format(env.project_name), '/etc/nginx/sites-available/{}_nginx'.format(env.project_name), use_sudo=True)
    if not exists('/etc/nginx/sites-available/{}_nginx'.format(env.project_name), use_sudo=True):
        put('{}_nginx'.format(env.project_name), '/home/{}/'.format(env.user))
        sudo('mv /home/{}/{}_nginx /etc/nginx/sites-available/'.format(env.user, env.project_name))
        sudo('nginx -t')
        sudo('ln -s /etc/nginx/sites-available/{}_nginx /etc/nginx/sites-enabled/'.format(env.project_name))
        sudo('nginx -s reload')
    else:
        print(red('nginx configuration for project {} exists'.format(env.project_name)))

def copy_systemd_config():
    print(green('checking systemd-configuration'))
    if not exists('/etc/systemd/system/{}.service'.format(env.project_name)):
        put('{}.service'.format(env.project_name), '/home/{}'.format(env.user))
        sudo('mv /home/{}/{}.service /etc/systemd/system/'.format(env.user, env.project_name))
        sudo('systemctl enable {}.service'.format(env.project_name))
        sudo('systemctl start {}.service'.format(env.project_name))
        # sudo('systemctl status {}.service'.format(env.project_name))
        # time.sleep(3)
        # send('q')
        # run('whoami')

    else:
        print(red('systemd {}.service already exists'.format(env.project_name)))

def copy_configs():
    copy_nginx_config()
    copy_systemd_config()

# env.local_static_root = '/static_root/'
# env.remote_static_root = '{}{}/static_root/'.format(env.path_to_projects, env.project_name)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def deploy_static():
    local('{} manage.py collectstatic --noinput'.format(p))
    zipf = zipfile.ZipFile('collected_static.zip', 'w', zipfile.ZIP_DEFLATED)
    execute(zipdir, 'static_root/', zipf)
    zipf.close()
    put('collected_static.zip', '{}'.format(PATH_TO_PROJECT))
    with cd(PATH_TO_PROJECT):
        run('unzip collected_static.zip')
        run('rm collected_static.zip')
        sudo('nginx -s reload')
    sudo('service gunicorn restart')
    sudo('systemctl restart {}.service'.format(env.project_name))
    sudo('nginx -s reload')
    # zip_ref = zipfile.ZipFile('{}/{}/collected_static.zip'.format(env.path_to_projects, env.project_name))
    # zip_ref.extractall('{}/{}/static_root/'.format(env.path_to_projects, env.project_name))

    # remote_dir = env.remote_static_root
    # local_dir = env.local_static_root

def remote_test():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        with prefix(env.activate):
            run('{} manage.py test'.format(p))

def commit():
    local('git add .')
    local('git commit -m "commit {}"'.format(time.ctime()))

def deploy():
    if not exists('{}{}'.format(env.path_to_projects, env.project_name)):
        print(red('project folder {}{} does not exist'.format(env.path_to_projects, env.project_name)))
        test()
        clone()
        remote_migrate()
        create_superuser()
        copy_systemd_config()
        copy_nginx_config()
        deploy_static()
        remote_test()
        #change secret key
        #change debug mode
        #change allowed hosts
        local('{} functional_tests.py {}'.format(p, env.domain_name))
    else:
        print(green('project folder exists, updating...'))
        test()
        update()
        remote_migrate()
        app_migrate('mainapp')
        remote_test()
        deploy_static()
        #change  secret_key
        #change debug mode
        #change allowed hosts
        sudo('systemctl restart {}.service'.format(env.project_name))
        sudo('systemctl show {}.service --no-page'.format(env.project_name))
        sudo('nginx -s reload')
        local('{} functional_tests.py {}'.format(p, env.domain_name))

    # local('git add .')
    # local('git commit -m "deploy on {}"'.format(c_time))
    # local('git push -u origin master')
    # #switch_debug("True", "False")
    # local('python3 manage.py collectstatic --noinput')
    # print(green('***Executing on {} as {}***'.format(unv.hosts, env.user)))
    # #switch_debug("False", "True")
