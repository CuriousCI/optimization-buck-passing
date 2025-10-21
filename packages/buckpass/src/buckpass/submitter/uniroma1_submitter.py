"""submit a job with slurm via ssh to uniroma1 CS department cluster."""

from buckpass.core import Submitter
from buckpass.core.util import OpenBoxTaskId, SlurmJobId
from typing_extensions import override


class Uniroma1Submitter(
    Submitter[SlurmJobId, OpenBoxTaskId],
):
    """submit a job with slurm via ssh to uniroma1 CS department cluster."""

    @override
    def submit(self, args: OpenBoxTaskId) -> SlurmJobId:
        return ""
