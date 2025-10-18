from typing_extensions import override

import barrel


# docker
# slurm
# submitter
class DockerSlurmSubmitter(
    barrel.Submitter[barrel.slurm.JobId, barrel.openbox.TaskId],
):
    @override
    def submit(self, args: barrel.openbox.TaskId) -> barrel.slurm.JobId:
        # TODO: ssh
        # TODO: sbatch (gives the id 777669)
        # TODO: resend and ip address (curl, Client for URL, ma non lo posso fare qui dentro?)
        # TODO: save in a file the result, and read it
        return ""


class Uniroma1SlurmSubmitter(
    barrel.Submitter[barrel.slurm.JobId, barrel.openbox.TaskId],
):
    @override
    def submit(self, args: barrel.openbox.TaskId) -> barrel.slurm.JobId:
        # TODO: run command via ssh (ie sbatch --run job.sh, or something like this)
        # TODO: ssh
        # TODO: sbatch (gives the id 777669)
        # TODO: resend and ip address (curl, Client for URL, ma non lo posso fare qui dentro?)
        # TODO: save in a file the result, and read it
        return ""
