import datetime
import http.server
import json
import socketserver
import sys

import buckpass
from openbox.artifact.remote_advisor import RemoteAdvisor

from example import SPACE

policy: (
    None
    | buckpass.BatchPolicy[
        buckpass.util.SlurmJobId,
        buckpass.util.OpenBoxTaskId,
    ]
) = None


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        print(body)
        request: dict[str, str] = json.loads(body.decode("utf-8"))
        assert policy

        policy.update(
            (
                request["worker_id"],
                buckpass.batch_policy.WorkerEvent[request["event"]],
            ),
        )

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        _ = self.wfile.write(b"{}")

        if policy.is_terminated():
            sys.exit(0)


def main() -> None:
    remote_advisor: RemoteAdvisor = RemoteAdvisor(
        config_space=SPACE,
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
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", 8080), RequestHandler) as httpd:
        global policy
        policy = buckpass.BatchPolicy(
            args=buckpass.util.OpenBoxTaskId(remote_advisor.task_id),
            max_runs=buckpass.IntGTZ(100),
            batch_size=buckpass.IntGTZ(3),
            submitter=buckpass.SshSubmitter(),
        )
        httpd.serve_forever()


if __name__ == "__main__":
    main()

# _ = buckpass.BurstPolicy(
#     args=buckpass.openbox_api.TaskId(remote_advisor.task_id),
#     batch_size=buckpass.IntGEZ(100),
#     submitter=buckpass.SshSubmitter(),
# )
