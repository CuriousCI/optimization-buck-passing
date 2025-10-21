import argparse
import datetime
import json
import os

import buckpass
import numpy as np
import requests
from openbox.utils.config_space import Configuration
from openbox.utils.constants import SUCCESS

from example import SPACE


def blackbox(configuration: Configuration) -> float:
    x = np.array(list(configuration.get_dictionary().values()))
    return float(x[0] * x[1] + x[1] ** 2 - x[0] ** 2 * x[1])


OPENBOX_URL: buckpass.openbox_api.URL = buckpass.openbox_api.URL(
    host="open-box",
    port=8000,
)

ORCHESTRATOR_URL = "http://orchestrator:8080/"


def main() -> None:
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    _ = argument_parser.add_argument("task_id")
    task_id: buckpass.util.OpenBoxTaskId = buckpass.util.OpenBoxTaskId(
        argument_parser.parse_args().task_id,
    )

    _ = requests.post(
        ORCHESTRATOR_URL,
        data=json.dumps(
            {"worker_id": os.getenv("SLURM_JOB_ID"), "event": "START"},
        ),
        timeout=100,
    )

    suggestion = buckpass.openbox_api.get_suggestion(
        url=OPENBOX_URL,
        task_id=task_id,
    )

    configuration = Configuration(SPACE, suggestion)

    blackbox_start_time = datetime.datetime.now(tz=datetime.UTC)
    observation = blackbox(configuration)
    blackbox_end_time = datetime.datetime.now(tz=datetime.UTC)

    trial_info = {
        "cost": (blackbox_end_time - blackbox_start_time).seconds,
        "worker_id": os.getenv("SLURM_JOB_ID"),
        "trial_info": None,
    }

    buckpass.openbox_api.update_observation(
        url=OPENBOX_URL,
        task_id=task_id,
        config_dict=suggestion,
        objectives=[observation],
        constraints=[],
        trial_info=trial_info,
        trial_state=SUCCESS,
    )

    _ = requests.post(
        ORCHESTRATOR_URL,
        data=json.dumps(
            {"worker_id": os.getenv("SLURM_JOB_ID"), "event": "END"},
        ),
        timeout=100,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, flush=True)
