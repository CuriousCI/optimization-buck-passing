import argparse
import datetime
from os import getenv

import numpy as np
from ConfigSpace import (
    Configuration,
    ConfigurationSpace,
    UniformFloatHyperparameter,
)
from openbox.utils.constants import SUCCESS

import barrel


def blackbox(config):
    x = np.array(list(config.get_dictionary().values()))
    result = x[0] * x[1] + x[1] ** 2 - x[0] ** 2 * x[1]
    return {"objectives": [result]}


OPENBOX_URL: str = "http://open-box:8000/bo_advice/"


def main() -> None:
    townsend_params = {"float": {"x1": (-2.25, 2.5, 0), "x2": (-2.5, 1.75, 0)}}
    townsend_cs = ConfigurationSpace()
    townsend_cs.add_hyperparameters(
        [
            UniformFloatHyperparameter(e, *townsend_params["float"][e])
            for e in townsend_params["float"]
        ],
    )

    argument_parser = argparse.ArgumentParser()
    _ = argument_parser.add_argument("task_id")
    task_id: barrel.openbox.TaskId = str(argument_parser.parse_args().task_id)  # pyright: ignore[reportAny]

    config_dict = barrel.openbox.get_suggestion(
        task_id=task_id,
        base_url=OPENBOX_URL,
    )
    config = Configuration(townsend_cs, config_dict)
    observation = blackbox(config)
    start_time = datetime.datetime.now(tz=datetime.UTC)
    trial_info = {
        "cost": (datetime.datetime.now(tz=datetime.UTC) - start_time).seconds,
        "worker_id": getenv("SLURM_JOB_ID"),
        "trial_info": None,
    }

    barrel.openbox.update_observation(
        task_id=task_id,
        base_url=OPENBOX_URL,
        config_dict=config_dict,
        objectives=observation["objectives"],
        constraints=[],
        trial_info=trial_info,
        trial_state=SUCCESS,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, flush=True)
