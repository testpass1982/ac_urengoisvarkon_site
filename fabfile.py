from fabric.api import *
from fabric.contrib import files
from fabric.contrib.files import exists
from fabric.colors import green, red, blue
from fabric.contrib import project
import time
import json
import os
import zipfile


# env.use_ssh_config = False
# env.disable_known_hosts = True
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
    print(green(
"""
***************************
**REMOTE MIGRATE COMPLETE**
***************************
"""
    ))

def local_migrate():
    local('{} manage.py makemigrations'.format(p))
    local('{} manage.py migrate'.format(p))
    print(green(
"""
**********************
**MIGRATION COMPLETE**
**********************
"""
    ))

def app_migrate(app):
        with cd('{}{}'.format(env.path_to_projects, env.project_name)):
            with prefix(env.activate):
                run('pwd')
                run('{} manage.py makemigrations {}'.format(p, app))
                run('{} manage.py migrate {}'.format(p, app))
                run('deactivate')
                print(green(
"""
****************************
***Django App {} migrated***
****************************
""".format(app)))
# def activate_virtualenv():

# def deactivate():

def create_superuser():
    put('secret.json', '{}{}/'.format(env.path_to_projects, env.project_name))
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        with prefix(env.activate):
            run('pwd')
            run('{} manage.py init_admin'.format(p))
            run('deactivate')
            print(green("""
*******************
*Superuser created*
*******************
"""))

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
    print(green(
"""
********************
**Testing complete**
********************
"""
    ))

#as user
def clone():
    print(green('CLONING...'))
    run('git clone {}'.format(env.git_repo))
    print(green(
"""
********************
**CLONING COMPLETE**
********************
"""
    ))

#as user
def update():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        print(green('UPDATING...'))
        run('git add .')
        run('git commit -m "server commit {}"'.format(time.ctime()))
        run('git pull')
    print(green(
"""
********************
**UPDATE COMPLETE***
********************
"""
    ))

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
****CONFIGS CREATED*****
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
    else:
        print(red('systemd {}.service already exists'.format(env.project_name)))

def copy_configs():
    copy_nginx_config()
    copy_systemd_config()
    print(green(
"""
*************************************
**SYSTEMD AND NGINX CONFIG UPLOADED**
*************************************
"""
    ))

# env.local_static_root = '/static_root/'
# env.remote_static_root = '{}{}/static_root/'.format(env.path_to_projects, env.project_name)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
    print(green(
"""
********************
***FOLDER ZIPPED****
********************
"""
    ))

def deploy_static():
    local('{} manage.py collectstatic --noinput'.format(p))
    zipf = zipfile.ZipFile('collected_static.zip', 'w', zipfile.ZIP_DEFLATED)
    execute(zipdir, 'static_root/', zipf)
    zipf.close()
    put('collected_static.zip', '{}'.format(PATH_TO_PROJECT))
    local('rm collected_static.zip')
    with cd(PATH_TO_PROJECT):
        run('unzip collected_static.zip')
        run('rm collected_static.zip')
        sudo('nginx -s reload')
    # sudo('service gunicorn restart')
    sudo('systemctl restart {}.service'.format(env.project_name))
    sudo('nginx -s reload')
    print(green("""
***********************
*Static files uploaded*
***********************
    """))
    # zip_ref = zipfile.ZipFile('{}/{}/collected_static.zip'.format(env.path_to_projects, env.project_name))
    # zip_ref.extractall('{}/{}/static_root/'.format(env.path_to_projects, env.project_name))

    # remote_dir = env.remote_static_root
    # local_dir = env.local_static_root

def remote_test():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        with prefix(env.activate):
            run('{} manage.py test'.format(p))
    print(green(
"""
************************
**REMOTE TEST COMPLETE**
************************
"""
    ))

def commit():
    local('git add .')
    local('git commit -m "commit {}"'.format(time.ctime()))
    print(green(
"""
********************
**COMMIT COMPLETE***
********************
"""
    ))

def fill_db_with_demo_data():
    with cd('{}{}'.format(env.path_to_projects, env.project_name)):
        with prefix(env.activate):
            run('{} manage.py fill_db'.format(p))
    print(green(
"""
**********************
**DEMO DATA COMPLETE**
**********************
"""
    ))

# def change_project_name():
#     print(green('checking project name before renaming'))
#     local('pwd')

def rename_template_folder():
    run('mv {}/ac_template_site/ {}{}'.format(
        env.path_to_projects,
        env.path_to_projects,
        env.project_name
        ))
    print(green(
"""
****************************
**PROJECT FOLDER RENAMED****
****************************
"""
    ))


def clean():
    are_you_sure = prompt(red('ARE YOU SURE YOU WANT TO CLEAN? y/n:'))
    if are_you_sure == 'y':
        if exists(PATH_TO_PROJECT) and \
        exists('/etc/nginx/sites-available/{}_nginx'.format(env.project_name)) and \
        exists('/etc/nginx/sites-enabled/{}_nginx'.format(env.project_name)) and \
        exists('/etc/systemd/system/{}.service'.format(env.project_name)):
            try:
                sudo('rm -rf {}/'.format(env.project_name))
                sudo('rm /etc/nginx/sites-available/{}_nginx'.format(env.project_name))
                sudo('rm /etc/nginx/sites-enabled/{}_nginx'.format(env.project_name))
                sudo('systemctl stop {}.service'.format(env.project_name))
                sudo('rm /etc/systemd/system/{}.service'.format(env.project_name))
                sudo('nginx -s reload')
                local('rm {}_nginx'.format(env.project_name))
                local('rm {}.service'.format(env.project_name))
                print(green('***PROJECT_CLEANED***'))
            except Exception as e:
                print(red('ERROR: ', e))
        else:
            print(green('***PROJECT DOES NOT EXIST***'))
    else:
        print(green('***CLEANING CANCELED***'))

def deploy():
    if not exists('{}{}'.format(env.path_to_projects, env.project_name)):
        print(green('***Project folder {}{} does not exist***'.format(env.path_to_projects, env.project_name)))
        confirm = prompt('*-*-* Start new deployment? (y/n): *-*-*')
        if confirm == 'y':
            print(blue("""
************************
STARTING in 5 seconds...
************************
            """))
            for i in range(5):
                time.sleep(1)
                print(blue('...{}...'.format(i+1)))
            test()
            clone()
            rename_template_folder()
            remote_migrate()
            create_superuser()
            app_migrate('mainapp')
            fill_db_with_demo_data()
            make_configs()
            copy_systemd_config()
            copy_nginx_config()
            deploy_static()
            remote_test()
            #change secret key
            #change debug mode
            #change allowed hosts
            local('{} functional_tests.py {}'.format(p, env.domain_name))
            print(blue("""
            *********************
            DEPLOYMENT COMPLETE...
            *********************
            """))
        else:
            print(green('***NEW DEPLOYMENT CANCELLED***'))
    else:
        print(green('...Project folder exists...'))
        confirm = prompt("Update? your answer y/n:")
        if confirm == 'y':
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
        else:
            print(green('***UPDATE CANCELLED***'))

    # local('git push -u origin master')
    # #switch_debug("True", "False")
    # local('python3 manage.py collectstatic --noinput')
    # print(green('***Executing on {} as {}***'.format(unv.hosts, env.user)))
    # #switch_debug("False", "True")
