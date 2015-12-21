from distutils.core import setup
from distutils.command.install import install
import os
import shutil


def check_package_exists():
    if os.path.exists("/etc/picamsupervisor/recorder.conf") and os.path.exists("/usr/local/picamsupervisor/recorder_service"):
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

            # Copy init.d script
            init_d_script_path = os.path.join(os.getcwd(), "scripts", "recorder-service")
            init_d_script_dest_path = os.path.join("/etc/init.d/", "recorder-service")

            shutil.copyfile(init_d_script_path, init_d_script_dest_path)

            # Set privileges on the script
            code = os.system("chmod 755 /etc/init.d/recorder-service")
            if code != 0:
                print "Setting script privileges failed with exit code: %s" % code
                exit(1)

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


            # Adding alarm signal monitor daemon to system services registry
            print "Adding daemon to system services registry"
            update_rc_command = "update-rc.d recorder-service defaults"
            exit_code = os.system(update_rc_command)

            if exit_code != 0:
                print "Registration failed with exit code: %s" % exit_code
                exit(1)
            else:
                print "Daemon registration finished successfully"

            print "Installation finished successfully"
            exit(0)
        except Exception, e:
            print "Installation failed"
            print e
            exit(1)


setup(name='recorder_service',
      version='1.0',
      description='Pi Cam Supervisor Recorder service',
      author='Bartosz Zawadka',
      author_email='kontakt@bartoszzawadka.pl',
      packages=['recorder_service'],
      cmdclass={'install': PostInstall})