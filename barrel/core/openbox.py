import json
from enum import Enum
from typing import Any

import requests


class TrialState(Enum):
    SUCCESS = 0
    FAILED = 1
    TIMEOUT = 2
    MEMOUT = 3


TaskId = str


def get_suggestion(base_url: str, task_id: TaskId):
    response: dict[str, Any] = json.loads(
        requests.post(
            base_url + "get_suggestion/",
            timeout=19000,
            data={"task_id": task_id},
        ).text,
    )

    assert response["code"]
    return json.loads(response["res"])


def update_observation(
    base_url: str,
    task_id: TaskId,
    config_dict,
    objectives,
    constraints=[],
    trial_info={},
    trial_state=0,
) -> None:
    response = json.loads(
        requests.post(
            base_url + "update_observation/",
            data={
                "task_id": task_id,
                "config": json.dumps(config_dict),
                "objectives": json.dumps(objectives),
                "constraints": json.dumps(constraints),
                "trial_state": trial_state,
                "trial_info": json.dumps(trial_info),
            },
        ).text,
    )

    assert response["code"]
