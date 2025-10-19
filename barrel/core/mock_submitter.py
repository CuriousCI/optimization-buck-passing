from typing_extensions import override

from barrel.core import JobId, Submitter
from barrel.core.openbox import TaskId
from barrel.slurm import JobId


class MockSubmitter(Submitter[JobId, TaskId]):
    job_id: int

    def __init__(self) -> None:
        super().__init__()
        self.job_id = 0

    @override
    def submit(self, args: TaskId) -> JobId:
        # TODO: ssh
        # TODO: sbatch (gives the id 777669)
        # TODO: resend and ip address (curl, Client for URL, ma non lo posso fare qui dentro?)
        # TODO: save in a file the result, and read it
        self.job_id += 1
        return JobId(self.job_id)
