FROM debian:trixie-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        openssh-client \
        sshpass

CMD ["sleep", "infinity"]
