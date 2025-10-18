FROM debian:trixie-slim

COPY services/slurm.conf /etc/slurm/slurm.conf

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        systemd \
        libmunge-dev \
        libmunge2 \
        munge \
        slurm-wlm \
        gosu

RUN /usr/sbin/mungekey
# RUN dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key \
#     && chown munge:munge /etc/munge/munge.key \
#     # && chown -R munge:munge /var/log/munge \
#     && chmod 400 /etc/munge/munge.key


RUN ls -la /var/log/

COPY services/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

    # && chmod 755 /var/log/munge -R \
# CMD /usr/sbin/munged && /usr/sbin/slurmctld -i -Dvvv


# RUN apt-get install -y slurm-wlm
    # && systemctl enable munge
    # && systemctl start munge
    # && /usr/sbin/slurmctld -i -Dvvv

        # git \
        # build-essential \
        # python3 \
    # && /sbin/create-munge-key

# RUN ls /sbin | grep munge
# /usr/sbin/munged --key-file ~/slurmConfDir/munge.key
    # && groupadd -r --gid=990 slurm \
    # && useradd -r -g slurm --uid=990 slurm \
    # && /sbin/create-munge-key \
    # && /usr/bin/munged --key-file


# if [ "$1" = "slurmctld" ]
# then
#     echo "---> Starting the MUNGE Authentication service (munged) ..."
#     gosu munge /usr/sbin/munged
#
#     echo "---> Waiting for slurmdbd to become active before starting slurmctld ..."
#
#     until 2>/dev/null >/dev/tcp/slurmdbd/6819
#     do
#         echo "-- slurmdbd is not available.  Sleeping ..."
#         sleep 2
#     done
#     echo "-- slurmdbd is now active ..."
#
#     echo "---> Starting the Slurm Controller Daemon (slurmctld) ..."
#     if /usr/sbin/slurmctld -V | grep -q '17.02' ; then
#         exec gosu slurm /usr/sbin/slurmctld -Dvvv
#     else
#         exec gosu slurm /usr/sbin/slurmctld -i -Dvvv
#     fi
# fi


# if [ "$1" = "slurmd" ]
# then
#     echo "---> Starting the MUNGE Authentication service (munged) ..."
#     gosu munge /usr/sbin/munged
#
#     echo "---> Waiting for slurmctld to become active before starting slurmd..."
#
#     until 2>/dev/null >/dev/tcp/slurmctld/6817
#     do
#         echo "-- slurmctld is not available.  Sleeping ..."
#         sleep 2
#     done
#     echo "-- slurmctld is now active ..."
#
#     echo "---> Starting the Slurm Node Daemon (slurmd) ..."
#     exec /usr/sbin/slurmd -Dvvv
# fi
