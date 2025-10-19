#!/bin/bash
set -e

if [ "$1" = "slurmctld" ]
then
    gosu munge /usr/sbin/munged
    service ssh start
    echo "root" | passwd root --stdin

    exec gosu slurm /usr/sbin/slurmctld -i -Dvvv
fi

if [ "$1" = "slurmd" ]
then
    gosu munge /usr/sbin/munged
    service ssh start
    echo "root" | passwd root --stdin

    until 2>/dev/null >/dev/tcp/slurmctld/6817
    do
        echo "-- slurmctld is not available ..."
        sleep 2
    done
    echo "-- slurmctld is now active"

    exec /usr/sbin/slurmd -Dvvv
fi

exec "$@"

# su munge
# ls /usr/sbin/ | grep munge
# ls /sbin/ | grep munge
# exec gosu munge /usr/sbin/munged
# exec gosu slurm /usr/sbin/slurmctld -i -Dvvv

# exec "$@"
