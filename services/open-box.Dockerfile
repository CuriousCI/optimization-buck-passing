FROM debian:trixie-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        git \
        swig \
        build-essential

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

RUN git clone --depth=1 https://github.com/PKU-DAIR/open-box.git \
    && cd open-box \
    && echo "3.8" > .python-version \
    && echo "django==2.2.17\npymongo<4.0\nbson\npyjwt" > requirements/service.txt \
    && sed -i 's/config_advisor.save_history()/# config_advisor.save_history()/' openbox/artifact/bo_advice/views.py \
    && uv add --dev setuptools wheel \
    && uv sync --extra service \
    && echo "[database]\ndatabase_address=mongo\ndatabase_port=27017\nuser=openbox\npassword=openbox" > conf/service.conf
    # && uv run /open-box/scripts/manage_service.sh migrate 

WORKDIR /open-box
COPY services/django.sh .

CMD ["./django.sh"]

# CMD ["uv", "run", "openbox/artifact/manage.py", "migrate", "&&", "uv", "run", "openbox/artifact/manage.py", "runserver", "0.0.0.0:8000"]
