#!/bin/bash

# ===== Help functions =====

function print_help {

    echo "Invalid arguments. See description below:"
    echo ""
    echo "Usage:"
    echo "sh uninstall.sh [modules...]"
    echo ""
    echo "MODULES:"
    echo "asg - Alarm signal monitor"
    echo "rs - Recorder service"
    echo "logger - Logger"
    exit 1

}

# ==========================

if [ $# -lt 1 ]
then
    print_help
fi

#script_working_dir=${PWD}

# ===== Uninstall functions =====

function remove_monitor {
    # 1. Stop service
    service alarm-signal-monitor stop

    # 2. Remove daemon script from init list
    update-rc.d alarm-signal-monitor remove

    # 3. Remove init script
    rm /etc/init.d/alarm-signal-monitor

    # 4. Remove symlink target
    rm -r "`readlink -f /usr/local/picamsupervisor/alarm_signal_monitor`"

    # 5. Remove symlink
    rm /usr/local/alarm_signal_monitor

    # WE DO NOT REMOVE CONFIG FILES OR OVERWRITE THEM
}

function remove_service {
    # 1. Remove symlink target
    # 2. Remove target

    # Remove symlink target
    rm -r "`readlink -f /usr/local/picamsupervisor/recorder_service`"

    # Remove symlink
    rm /usr/local/picamsupervisor/recorder_service

    return

}

function remove_logger {
    # Remove symlink target
    rm -r "`readlink -f /usr/local/picamsupervisor/logger`"

    # Remove symlink
    rm /usr/local/picamsupervisor/logger

    return

}
# ==========================


# ===== Arguments validation ====
for ((i=1; i<=${#@}; i++));
do
    if [ "$i" != "asg" ] && [ "$i" != "rs" ] && [ "$i" != "logger" ]
    then
        print_help
    fi
done

# ==========================

# ====== Arguments processing =====

for ((i=1; i<=${#@}; i++));
do
    case "$i" in
    asg)
        remove_monitor
        ;;
    rs)
        remove_service
        ;;
    logger)
        remove_logger
        ;;
    *)
        print_help
        ;;
    esac
done
# ==========================