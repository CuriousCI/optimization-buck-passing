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
        gosu \
        openssh-server

RUN mkdir -p /run/munge \
    && chown -R munge:munge /run/munge \
    && echo "PermitRootLogin yes\nPasswordAuthentication yes" > /etc/ssh/sshd_config 

RUN mkdir -p /etc/sysconfig/slurm \
        /var/spool/slurmd \
        /var/run/slurmd \
        /var/run/slurmdbd \
        /var/lib/slurmd \
        /var/log/slurm \
        /data \
    && touch /var/lib/slurmd/node_state \
        /var/lib/slurmd/front_end_state \
        /var/lib/slurmd/job_state \
        /var/lib/slurmd/resv_state \
        /var/lib/slurmd/trigger_state \
        /var/lib/slurmd/assoc_mgr_state \
        /var/lib/slurmd/assoc_usage \
        /var/lib/slurmd/qos_usage \
        /var/lib/slurmd/fed_mgr_state \
    && chown -R slurm:slurm /var/*/slurm* 

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

COPY services/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["sleep", "infinity"]
