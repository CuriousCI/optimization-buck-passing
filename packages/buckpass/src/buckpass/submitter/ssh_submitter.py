"""sbatch via ssh."""

import subprocess

from typing_extensions import override

from buckpass.core import Submitter
from buckpass.core.util import OpenBoxTaskId, SlurmJobId


class SshSubmitter(
    Submitter[SlurmJobId, OpenBoxTaskId],
):
    """sbatch via ssh."""

    @override
    def submit(self, args: OpenBoxTaskId) -> SlurmJobId:
        stdout: str = subprocess.run(
            [
                "/usr/bin/sshpass",
                "-p",
                "root",
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "slurmctld",
                f'""sbatch /data/src/job.sh {args}""',
            ],
            check=False,
            capture_output=True,
        ).stdout.decode()

        # `sbatch` prints "Submitted batch job 781422" to stdout
        return "".join(filter(str.isnumeric, stdout))
