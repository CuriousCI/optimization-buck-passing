import subprocess

from typing_extensions import override

from barrel.core import Submitter
from barrel.core.openbox import TaskId
from barrel.slurm import JobId


# docker
# slurm
# submitter
class DockerSlurmSubmitter(
    Submitter[JobId, TaskId],
):
    @override
    def submit(self, args: TaskId) -> JobId:
        result = subprocess.run(
            [
                "sshpass",
                "-p",
                "root",
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "slurmctld",
                f'""sbatch /data/job.sh {args}""',
            ],
            capture_output=True,
        )

        return str(result.stdout)

        # sshpass -p root ssh -o StrictHostKeyChecking=no slurmctld "sbatch /data/job.sh test"


class Uniroma1SlurmSubmitter(
    Submitter[JobId, TaskId],
):
    @override
    def submit(self, args: TaskId) -> JobId:
        # TODO: run command via ssh (ie sbatch --run job.sh, or something like this)
        # TODO: ssh
        # TODO: sbatch (gives the id 777669)
        # TODO: resend and ip address (curl, Client for URL, ma non lo posso fare qui dentro?)
        # TODO: save in a file the result, and read it
        return ""
