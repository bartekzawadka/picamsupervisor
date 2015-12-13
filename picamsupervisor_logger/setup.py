from distutils.core import setup
from distutils.command.install import install
import os
import shutil


class PostInstall(install):
    def run(self):
        install.run(self)

        print self.install_lib

        if not os.path.exists('/usr/local/picamsupervisor'):
            print "Creating directory: /usr/local/picamsupervisor"
            os.makedirs('/usr/local/picamsupervisor')
            print "Directory created"

        link_target_path = os.path.join(self.install_lib, "picamsupervisor_logger")
        try:
            os.symlink(link_target_path, "/usr/local/picamsupervisor/logger")
        except Exception, e:
            print "Symlink already exists"
        else:
            print "Symlink added successfully"

        if not os.path.exists('/etc/picamsupervisor/log.conf'):
            directory = '/etc/picamsupervisor/'
            if not os.path.exists(directory):
                os.makedirs(directory)

            path = os.path.join(os.getcwd(), "config", "log.conf")
            shutil.copyfile(path, os.path.join(directory, "log.conf"))


setup(name='picamsupervisor_logger',
      version='1.0',
      description='Pi Cam Supervisor log utils',
      author='Bartosz Zawadka',
      author_email='kontakt@bartoszzawadka.pl',
      packages=['picamsupervisor_logger'],
      cmdclass={'install': PostInstall})
