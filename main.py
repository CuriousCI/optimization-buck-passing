import os
import time

from openbox.artifact.remote_advisor import RemoteAdvisor
from openbox.utils.config_space import ConfigurationSpace

import barrel


def main() -> None:
    config_space = ConfigurationSpace()

    remote_advisor: RemoteAdvisor = RemoteAdvisor(
        config_space=config_space,
        server_ip="",
        port=1234,
        email="xx@xx.com",
        password=os.getenv("PASSWORD"),
        task_name="",
    )

    worker_policy = barrel.SimplePolicy(
        task_id=barrel.openbox.TaskId(remote_advisor.task_id),  # pyright: ignore[reportAny]
        pool_size=barrel.IntGEZ(4),
        submitter=barrel.DockerSlurmSubmitter(),
    )

    while True:
        time.sleep(1)
        for worker_id in worker_policy.workers():
            # TODO: ask slurm for worker info, send it to policy
            worker_policy.update(
                (worker_id, barrel.simple_policy.WorkerEventType.END),
            )


if __name__ == "__main__":
    main()
