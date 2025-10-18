#!/bin/bash

# su munge
ls /usr/sbin/ | grep munge
ls /sbin/ | grep munge
exec gosu munge /usr/sbin/munged
exec gosu slurm /usr/sbin/slurmctld -i -Dvvv
