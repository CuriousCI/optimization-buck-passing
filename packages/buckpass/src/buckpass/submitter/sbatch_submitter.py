"""sbatch."""

import os
import subprocess

from buckpass.core import Submitter
from buckpass.core.util import OpenBoxTaskId, SlurmJobId
from typing_extensions import override


class SbatchSubmitter(
    Submitter[SlurmJobId, OpenBoxTaskId],
):
    """sbatch."""

    @override
    def submit(self, args: OpenBoxTaskId) -> SlurmJobId:
        stdout: str = subprocess.run(
            ["/usr/bin/sbatch", f"{os.getenv('HOME')}/job.sh", f"{args}"],
            check=False,
            capture_output=True,
        ).stdout.decode()

        # `sbatch` prints "Submitted batch job 781422" to stdout
        return "".join(filter(str.isnumeric, stdout))
