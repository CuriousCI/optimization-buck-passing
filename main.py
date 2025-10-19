import datetime
import subprocess
import time
from http.server import BaseHTTPRequestHandler

# from barrel.core.remote_advisor_dbg import RemoteAdvisorDebug
import numpy
import requests
from ConfigSpace import Configuration, UniformFloatHyperparameter
from openbox.utils.config_space import ConfigurationSpace
from openbox.utils.constants import SUCCESS

import barrel
from barrel.core.remote_advisor_dbg import RemoteAdvisorDebug

worker_policy = None


def run_task() -> None:
    townsend_params = {"float": {"x1": (-2.25, 2.5, 0), "x2": (-2.5, 1.75, 0)}}
    townsend_cs = ConfigurationSpace()
    townsend_cs.add_hyperparameters(
        [
            UniformFloatHyperparameter(e, *townsend_params["float"][e])
            for e in townsend_params["float"]
        ],
    )

    remote_advisor: RemoteAdvisorDebug = RemoteAdvisorDebug(
        config_space=townsend_cs,
        server_ip="open-box",
        port=8000,
        email="test@test.test",
        password="testtest",
        task_name=f"test_task_{datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%d_%H:%M:%S')}",
        num_objectives=1,
        num_constraints=0,
        sample_strategy="bo",
        surrogate_type="gp",
        acq_type="ei",
        max_runs=100,
    )

    worker_policy = barrel.SimplePolicy(
        task_id=barrel.openbox.TaskId(remote_advisor.task_id),
        pool_size=barrel.IntGEZ(100),
        submitter=barrel.DockerSlurmSubmitter(),
    )


def main() -> None:
    while True:
        try:
            return run_task()
        except requests.exceptions.ConnectionError:
            time.sleep(1)


if __name__ == "__main__":
    main()

    # for worker_id in worker_policy.workers():
    #     config_dict = remote_advisor.get_suggestion()
    #     # TODO: use this as arg to blackbox
    #     config = Configuration(remote_advisor.config_space, config_dict)
    #     observation = blackbox(config)
    #     start_time = datetime.datetime.now(tz=datetime.UTC)
    #     trial_info = {
    #         "cost": (
    #             datetime.datetime.now(tz=datetime.UTC) - start_time
    #         ).seconds,
    #         "worker_id": worker_id,
    #         "trial_info": None,
    #     }
    #
    #     remote_advisor.update_observation(
    #         config_dict,
    #         observation["objectives"],
    #         [],
    #         trial_info=trial_info,
    #         trial_state=SUCCESS,
    #     )
    #
    #     worker_policy.update(
    #         (worker_id, barrel.simple_policy.WorkerEventType.END),
    #     )


# server_address = ('', 8000)
# httpd = HTTPServer(server_address, RequestHandler)
# print('Starting httpd...')
# httpd.serve_forever()
# sshpass -p root ssh -o StrictHostKeyChecking=no slurmctld

# class RequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b"Hello, World!")
#
#
# def blackbox(config):
#     x = numpy.array(list(config.get_dictionary().values()))
#     result = x[0] * x[1] + x[1] ** 2 - x[0] ** 2 * x[1]
#     return {"objectives": [result]}
