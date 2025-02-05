#!/usr/bin/env python3

# ----------------------------------- System - Import Function -----------------------------------
def system_import_func():

    global Gtk, GLib, subprocess, os, platform, pkg_resources

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import subprocess
    import os
    import platform
    try:                                                                                      # "pkg_resources" module may not be installed on some systems. This package is installed if "setuptools" is installed.
        import pkg_resources
    except ModuleNotFoundError:
        pass


    global Config
    import Config


# ----------------------------------- System - System GUI Function -----------------------------------
def system_gui_func():

    # System tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SystemTab.ui")

    # System tab GUI objects
    global grid8101
    global button8101
    global label8101, label8102, label8103, label8104, label8105, label8106, label8107, label8108, label8109, label8110
    global label8111, label8112, label8113, label8114, label8115, label8116, label8117, label8118, label8119, label8120
    global label8121, label8122

    # System tab GUI objects - get
    grid8101 = builder.get_object('grid8101')
    button8101 = builder.get_object('button8101')
    label8101 = builder.get_object('label8101')
    label8102 = builder.get_object('label8102')
    label8103 = builder.get_object('label8103')
    label8104 = builder.get_object('label8104')
    label8105 = builder.get_object('label8105')
    label8106 = builder.get_object('label8106')
    label8107 = builder.get_object('label8107')
    label8108 = builder.get_object('label8108')
    label8109 = builder.get_object('label8109')
    label8110 = builder.get_object('label8110')
    label8111 = builder.get_object('label8111')
    label8112 = builder.get_object('label8112')
    label8113 = builder.get_object('label8113')
    label8114 = builder.get_object('label8114')
    label8115 = builder.get_object('label8115')
    label8116 = builder.get_object('label8116')
    label8117 = builder.get_object('label8117')
    label8118 = builder.get_object('label8118')
    label8119 = builder.get_object('label8119')
    label8120 = builder.get_object('label8120')
    label8121 = builder.get_object('label8121')
    label8122 = builder.get_object('label8122')


    # System tab GUI functions
    def on_button8101_clicked(widget):                                                        # "Refresh" button
        system_initial_func()


    # System tab GUI functions - connect
    button8101.connect("clicked", on_button8101_clicked)


# ----------------------------------- System - Initial Function -----------------------------------
def system_initial_func():

    # Get OS name, version, version code name and OS based on information
    os_name = "-"                                                                             # Initial value of "os_name" variable. This value will be used if "os_name" could not be detected.
    os_based_on = "-"
    os_version = "-"
    with open("/etc/os-release") as reader:
        os_release_output_lines = reader.read().strip().split("\n")
    for line in os_release_output_lines:
        if line.startswith("NAME="):
            os_name = line.split("NAME=")[1].strip(' "')
            continue
        if line.startswith("VERSION="):
            os_version = line.split("VERSION=")[1].strip(' "')
            continue
        if line.startswith("ID_LIKE="):
            os_based_on = line.split("ID_LIKE=")[1].strip(' "').title()
            continue
    if os_based_on == "Debian":
        debian_version = "-"
        with open("/etc/debian_version") as reader:
            debian_version = reader.read().strip()
        os_based_on = os_based_on + " (" + debian_version + ")"
    if os_based_on == "Ubuntu":
        ubuntu_version = "-"
        for line in os_release_output_lines:
            if line.startswith("UBUNTU_CODENAME="):
                ubuntu_version = line.split("UBUNTU_CODENAME=")[1].strip(' "')
                break
        os_based_on = os_based_on + " (" + ubuntu_version + ")"

    # Get os family
    os_family = platform.system()
    if os_family == "":
        os_family = "-"

    # Get kernel release (base version of kernel)
    kernel_release = platform.release()
    if kernel_release == "":
        kernel_release = "-"

    # Get kernel version (package version of kernel))
    kernel_version = platform.version()
    if kernel_version == "":
        kernel_version = "-"

    # Get current Python version (Python which is running this code)
    current_python_version = platform.python_version()

    # Get CPU architecture
    cpu_architecture = platform.processor()
    if cpu_architecture == "":
        cpu_architecture = platform.machine()
        if cpu_architecture == "":
            cpu_architecture = "-"

    # Get computer vendor, model, chassis information
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
            computer_vendor = reader.read().strip()
    except FileNotFoundError:
        computer_vendor = "-"
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/product_name") as reader:
            computer_model = reader.read().strip()
    except FileNotFoundError:
        computer_model = "-"
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/chassis_type") as reader:
            computer_chassis_type_value = reader.read().strip()
    except FileNotFoundError:
        computer_chassis_type_value = 2

    # For more information about computer chassis types, see: "https://docs.microsoft.com/en-us/previous-versions/tn-archive/ee156537(v=technet.10)"
    # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
    computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                   10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                   17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                   22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC"}
    computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]

    # Get host name
    with open("/proc/sys/kernel/hostname") as reader:
        host_name = reader.read().strip()

    # Get number of monitors
    current_screen = label8101.get_toplevel().get_screen()
    number_of_monitors = current_screen.get_n_monitors()

    # Get human and root user usernames and UIDs which will be used for determining username when "pkexec_uid" is get.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])
    # Get current username
    current_user_name = os.environ.get('SUDO_USER')                                           # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                             # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                    # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Try to get windowing system. This value may be get as "None" if the application is run with root privileges. This value will be get by reading information of processes if it is get as "None".
    windowing_system = os.environ.get('XDG_SESSION_TYPE')
    if windowing_system != None:                                                              # "windowing_system" is get as "None" if application is run with root privileges.
        windowing_system = windowing_system.capitalize()

    # Try to get current desktop environment. This value may be get as "None" if the application is run with root privileges. This value will be get by reading information of processes if it is get as "None".
    current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')                       # This command may give Gnome DE based DEs as "[DE_name]:GNOME". For example, "Budgie:GNOME" value is get on Budgie DE.
    if current_desktop_environment == None:
        current_desktop_environment = "-"                                                     # Set an initial string in order to avoid errors in case of undetected current desktop environment (DE).

    # Define initial value of "windowing_system"
    if windowing_system == None:
        windowing_system = "-"

    supported_desktop_environments_dict = {"xfce4-session":"XFCE", "gnome-session-b":"GNOME", "cinnamon-session":"X-Cinnamon",
                                           "mate-session":"MATE", "plasmashell":"KDE", "lxqt-session":"LXQt", "lxsession":"LXDE",
                                           "budgie-panel":"Budgie", "dde-desktop":"Deepin"}    # First values are process names of the DEs, second values are names of the DEs. Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.

    # Define initial value of "window_manager"
    window_manager = "-"
    supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome"]

    # Define initial value of "current_display_manager"
    supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}    # First values are process names of the display managers, second values are names of the display managers.
    current_display_manager = "-"                                                             # Set an initial string in order to avoid errors in case of undetected current display manager.

    # Try to detect windowing system, window manager, current desktop environment and current display manager by reading process names and other details.
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
    for pid in pid_list:
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + pid + "/comm") as reader:
                process_name = reader.read().strip()
        except FileNotFoundError:
            continue
        # Get windowing system information
        if windowing_system == "-":
            if process_name.lower() == "xorg":
                windowing_system = "X11"
            if process_name.lower() == "xwayland":
                windowing_system = "Wayland"
        # Get window manager information
        if window_manager == "-":
            if process_name.lower() in supported_window_managers_list:
                try:
                    with open("/proc/" + pid + "/status") as reader:                          # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        proc_pid_status_lines = reader.read()
                except FileNotFoundError:
                    continue
                real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                if process_username == current_user_name:
                    window_manager = process_name.lower()
        # Get current display manager information
        if current_display_manager == "-":
            if process_name in supported_display_managers_dict:
                try:
                    with open("/proc/" + pid + "/status") as reader:                          # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        proc_pid_status_lines = reader.read()
                except FileNotFoundError:
                    continue
                real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                if process_username == "root":                                                # Display manager processes are owned by root user.
                    current_display_manager = supported_display_managers_dict[process_name]
        # Get current desktop environment information
        if current_desktop_environment == "-" or current_desktop_environment == "GNOME":      # "current_desktop_environment == "GNOME"" check is performed in order to detect if current DE is "Budgie DE". Because "budgie-panel" process is child process of "gnome-session-b" process.
            if process_name in supported_desktop_environments_dict:
                try:
                    with open("/proc/" + pid + "/status") as reader:                          # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        proc_pid_status_lines = reader.read()
                except FileNotFoundError:
                    continue
                real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                if process_username == current_user_name:
                    current_desktop_environment = supported_desktop_environments_dict[process_name]

    # Get current desktop environment version
    current_desktop_environment_version = "-"                                                 # Set initial value of the "current_desktop_environment_version". This value will be used if it could not be detected.
    if current_desktop_environment == "XFCE":
        try:
            current_desktop_environment_version_lines = (subprocess.check_output(["xfce4-panel", "--version"], shell=False)).decode().strip().split("\n")
            for line in current_desktop_environment_version_lines:
                if "xfce4-panel" in line:
                    current_desktop_environment_version = line.split(" ")[1]
        except FileNotFoundError:
            pass
    if current_desktop_environment == "GNOME" or current_desktop_environment == "zorin:GNOME" or current_desktop_environment == "ubuntu:GNOME":
        try:
            current_desktop_environment_version_lines = (subprocess.check_output(["gnome-shell", "--version"], shell=False)).decode().strip().split("\n")
            for line in current_desktop_environment_version_lines:
                if "GNOME Shell" in line:
                    current_desktop_environment_version = line.split(" ")[-1]
        except FileNotFoundError:
            pass
    if current_desktop_environment == "X-Cinnamon" or current_desktop_environment == "CINNAMON":
        try:
            current_desktop_environment_version = (subprocess.check_output(["cinnamon", "--version"], shell=False)).decode().strip().split(" ")[-1]
        except FileNotFoundError:
            pass
    if current_desktop_environment == "MATE":
        try:
            current_desktop_environment_version = (subprocess.check_output(["mate-about", "--version"], shell=False)).decode().strip().split(" ")[-1]
        except FileNotFoundError:
            pass
    if current_desktop_environment == "KDE":
        try:
            current_desktop_environment_version = (subprocess.check_output(["plasmashell", "--version"], shell=False)).decode().strip()
        except FileNotFoundError:
            pass
    if current_desktop_environment == "LXQt":
        try:
            current_desktop_environment_version_lines = (subprocess.check_output(["lxqt-about", "--version"], shell=False)).decode().strip()
            for line in current_desktop_environment_version_lines:
                if "liblxqt" in line:
                    current_desktop_environment_version = line.split()[1].strip()
        except FileNotFoundError:
            pass
    if current_desktop_environment == "Budgie" or current_desktop_environment == "Budgie:GNOME":
        try:
            current_desktop_environment_version = (subprocess.check_output(["budgie-desktop", "--version"], shell=False)).decode().strip().split("\n")[0].strip().split(" ")[-1]
        except FileNotFoundError:
            pass

    # Determine package types used on the system. This information will be used for getting number of installed packages on the system.
    apt_packages_available = "-"                                                              # Initial value of the variable.
    rpm_packages_available = "-"
    pacman_packages_available = "-"
    number_of_installed_apt_or_rpm_or_pacman_packages = "-"
    number_of_installed_flatpak_packages = "-"
    try:
        apt_packages_available = (subprocess.check_output(["dpkg", "-s", "python3"], shell=False)).decode().strip()    # Check if "python3" is installed in order to determine package type of the system.
        if "Package: python3" in apt_packages_available:
            number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
            number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_apt_packages} (APT)'
    except (FileNotFoundError, subprocess.CalledProcessError) as me:                          # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
        apt_packages_available = "-"
    if apt_packages_available == "-":
        try:
            rpm_packages_available = (subprocess.check_output(["rpm", "-q", "python3"], shell=False)).decode().strip()
            if rpm_packages_available.startswith("python3-3."):
                number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
                number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")    # Differentiate empty line count
                number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_rpm_packages} (RPM)'
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            rpm_packages_available = "-"
    if apt_packages_available == "-" and rpm_packages_available == "-":
        try:
            pacman_packages_available = (subprocess.check_output(["pacman", "-Q", "python3"], shell=False)).decode().strip()
            if pacman_packages_available.startswith("python 3."):
                number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")    # Differentiate empty line count
                number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_pacman_packages} (pacman)'
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            pacman_packages_available = "-"

    # Get number of installed Flatpak packages (and runtimes)
    try:
        flatpak_packages_available = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
        number_of_installed_flatpak_packages = len(flatpak_packages_available) - flatpak_packages_available.count("")    # Differentiate empty line count
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        number_of_installed_flatpak_packages = "-"

    # Get number of installed Python packages (including built-in packages)
    try:                                                                                      # "pkg_resources" module may not be installed on some systems. This package is installed if "setuptools" is installed.
        number_of_installed_python_packages = len([d.project_name for d in pkg_resources.working_set])
    except NameError:
        number_of_installed_python_packages = "-"


    # Set label texts to show information
    label8101.set_text(f'{os_name} - {os_version}')
    label8102.set_text(f'{computer_vendor} - {computer_model}')
    label8103.set_text(os_name)
    label8104.set_text(os_version)
    label8105.set_text(os_family)
    label8106.set_text(os_based_on)
    label8107.set_text(kernel_release)
    label8108.set_text(kernel_version)
    label8109.set_text(f'{current_desktop_environment} ({current_desktop_environment_version})')
    label8110.set_text(windowing_system)
    label8111.set_text(window_manager)
    label8112.set_text(current_display_manager)
    label8113.set_text(computer_vendor)
    label8114.set_text(computer_model)
    label8115.set_text(computer_chassis_type)
    label8116.set_text(host_name)
    label8117.set_text(cpu_architecture)
    label8118.set_text(f'{number_of_monitors}')
    label8119.set_text(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')
    label8120.set_text(f'{number_of_installed_flatpak_packages}')
    label8121.set_text(f'{number_of_installed_python_packages}')
    label8122.set_text(f'{current_python_version}')


# ----------------------------------- System - Run Function -----------------------------------
def system_run_func(*args):

    GLib.idle_add(system_initial_func)
