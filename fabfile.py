from __future__ import with_statement
from fabric.api import env, local, run, settings

env.hosts = ['seed001.core.ams01.sn.ecg']
env.user = 'root'
application = 'seedbank'
deb_file = 'seedbank_1.0.0_all.deb'
repository = '/home/www/repositories/debian/sn'

def build():
    local('dpkg-buildpackage -b -tc')
    local('mv ~/git/%s*.deb ~/git/%s_*.changes ~/builds' % (application, application))

def repo_add():
    local('reprepro -Vb %s includedeb squeeze ~/builds/%s' % (repository, deb_file))
    
def repo_remove():
    with settings(warn_only=True):
        local('reprepro -Vb %s remove squeeze %s' % (repository, application))

def localhost():
    build()
    repo_remove()
    repo_add()

def sn_seed():
    build()
    local('scp ~/builds/%s root@mm_sn-seed001b:' % deb_file)
    local('ssh root@mm_sn-seed001b dpkg -i %s' % deb_file)

def test():
    localhost()
    run('apt-get update')
    run('apt-get --force-yes purge %s' % application)
    run('rm -rf /etc/%s' % application)
    run('apt-get --assume-yes install %s' % application)
    run('/etc/init.d/%s start' % application)


def test_remote():
    build()
    #local('scp ~/builds/%s root@sn-seed001a:' % deb_file)
    local('scp ~/builds/%s root@seed001.core.ams01.sn.ecg:' % deb_file)
    #local('ssh root@sn-seed001a rep.py -d sn-squeeze seedbank')
    #local('ssh root@sn-seed001a rep.py -a sn-squeeze %s' % deb_file)
    #local('ssh root@seed001.core.ams01.sn.ecg apt-get update')
    local('ssh root@seed001.core.ams01.sn.ecg apt-get --force-yes --assume-yes purge %s' % application)
    local('ssh root@seed001.core.ams01.sn.ecg rm -rf /etc/%s' % application)
    local('ssh root@seed001.core.ams01.sn.ecg dpkg -i %s' % deb_file)
    #local('ssh root@seed001.core.ams01.sn.ecg apt-get --assume-yes install %s' % application)
    local('ssh root@seed001.core.ams01.sn.ecg /etc/init.d/%s start' % application)
