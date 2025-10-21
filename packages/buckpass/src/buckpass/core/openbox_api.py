import json
import re
from typing import Any

import requests
from typing_extensions import override

from .util import OpenBoxTaskId


class URL:
    __url: str
    __TCP_MAX_PORT = 65535

    def __init__(self, host: str, port: int) -> None:
        assert 0 <= port <= self.__TCP_MAX_PORT
        assert re.match("", host)

        self.__url = f"http://{host}:{port}/bo_advice/"

    @override
    def __str__(self) -> str:
        return self.__url

    @override
    def __repr__(self) -> str:
        return self.__url


def get_suggestion(url: URL, task_id: OpenBoxTaskId):
    response: dict[str, Any] = json.loads(
        requests.post(
            f"{url}get_suggestion/",
            data={"task_id": task_id},
            timeout=100,
        ).text,
    )

    assert response["code"]
    return json.loads(response["res"])


def update_observation(
    url: URL,
    task_id: OpenBoxTaskId,
    config_dict,
    objectives,
    constraints=[],
    trial_info={},
    trial_state=0,
) -> None:
    response = json.loads(
        requests.post(
            f"{url}update_observation/",
            data={
                "task_id": task_id,
                "config": json.dumps(config_dict),
                "objectives": json.dumps(objectives),
                "constraints": json.dumps(constraints),
                "trial_state": trial_state,
                "trial_info": json.dumps(trial_info),
            },
            timeout=100,
        ).text,
    )

    assert response["code"]
