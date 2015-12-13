from distutils.core import setup
from distutils.command.install import install
import os
import shutil


def check_package_exists():
    if os.path.exists("/etc/picamsupervisor/monitor.conf") and os.path.exists("/usr/local/picamsupervisor/alarm_signal_monitor"):
        return True
    else:
        return False


class PostInstall(install):
    def run(self):
        try:
            install.run(self)

            if check_package_exists():
                print "Package already exists - please uninstall before updating"
                print "Exiting"
                return

            # Copy config file
            if not os.path.exists('/etc/picamsupervisor/recorder.conf'):
                directory = '/etc/picamsupervisor/'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                config_path = os.path.join(os.getcwd(), "config", "recorder.conf")
                shutil.copyfile(config_path, os.path.join(directory, "recorder.conf"))

            # Create symbolic link to monitor daemon
            print "Adding symlink to daemon's directory"

            link_target_path = os.path.join(self.install_lib, "recorder_service")

            if not os.path.exists('/usr/local/picamsupervisor'):
                print "Creating directory: /usr/local/picamsupervisor"
                os.makedirs('/usr/local/picamsupervisor')
                print "Directory created"

            try:
                os.symlink(link_target_path, "/usr/local/picamsupervisor/recorder_service")
            except Exception, e:
                print "Symlink already exists"
            else:
                print "Symlink added successfully"

            print "Installation finished successfully"
            exit(0)
        except Exception, e:
            print "Installation failed"
            print e
            exit(1)


setup(name='alarm_signal_monitor',
      version='1.0',
      description='Pi Cam Supervisor Alarm Signal Monitor service',
      author='Bartosz Zawadka',
      author_email='kontakt@bartoszzawadka.pl',
      packages=['alarm_signal_monitor'],
      cmdclass={'install': PostInstall})