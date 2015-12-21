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
            if not os.path.exists('/etc/picamsupervisor/monitor.conf'):
                directory = '/etc/picamsupervisor/'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                config_path = os.path.join(os.getcwd(), "config", "monitor.conf")
                shutil.copyfile(config_path, os.path.join(directory, "monitor.conf"))

            # Copy init.d script
            print "Copying init.d scripts"

            init_d_script_path = os.path.join(os.getcwd(), "scripts", "alarm-signal-monitor")
            init_d_script_dest_path = os.path.join("/etc/init.d/", "alarm-signal-monitor")

            shutil.copyfile(init_d_script_path, init_d_script_dest_path)

            # Set privileges on the script
            code = os.system("chmod 755 /etc/init.d/alarm-signal-monitor")
            if code != 0:
                print "Setting script privileges failed with exit code: %s" % code
                exit(1)

            # Create symbolic link to monitor daemon
            print "Adding symlink to daemon's directory"

            link_target_path = os.path.join(self.install_lib, "alarm_signal_monitor")

            if not os.path.exists('/usr/local/picamsupervisor'):
                print "Creating directory: /usr/local/picamsupervisor"
                os.makedirs('/usr/local/picamsupervisor')
                print "Directory created"

            try:
                os.symlink(link_target_path, "/usr/local/picamsupervisor/alarm_signal_monitor")
            except Exception, e:
                print "Symlink already exists"
            else:
                print "Symlink added successfully"

            # Adding alarm signal monitor daemon to system services registry
            print "Adding daemon to system services registry"
            update_rc_command = "update-rc.d alarm-signal-monitor defaults"
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


setup(name='alarm_signal_monitor',
      version='1.0',
      description='Pi Cam Supervisor Alarm Signal Monitor service',
      author='Bartosz Zawadka',
      author_email='kontakt@bartoszzawadka.pl',
      packages=['alarm_signal_monitor'],
      cmdclass={'install': PostInstall})
