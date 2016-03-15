"""DPCS client implementation.

Simplest usage:
sudo python -m [parent_directory_name].demon start
"""
from __future__ import print_function
from os import path
import time

from daemon import runner
from requests import get
from requests import post
from requests import RequestException

from .mock import sample_report


SERVER_ADDRESS = "http://private-a6e53-dpcs.apiary-mock.com/"


class DPCSDaemon():
    """Wrapper over DPCS client functionality."""

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/dpcs.pid'
        self.pidfile_timeout = 5

    def _handle_request_error(self, exception, dpcs_message):
        print(dpcs_message)
        print(exception.response.text)

    def run(self):
        first_sent = False

        while True:

            # Mock - sends every ten seconds a simple message.

            # First report is sent immediately so that a developer
            # doesn't have to wait
            if first_sent:
                time.sleep(10)
            else:
                first_sent = True

            api_description_url = SERVER_ADDRESS + "vd1/paths/"
            try:
                response = get(api_description_url)
            except RequestException as e:
                self._handle_request_error(
                    e, "DPCS couldn't get api description"
                )
                continue

            api_paths = response.json()
            crash_report_url = SERVER_ADDRESS + api_paths["crash-reports"]
            headers = {
              'Content-Type': 'text/json'
            }

            try:
                response = post(crash_report_url,
                                headers=headers,
                                data=sample_report)
            except RequestException as e:
                self._handle_request_error(
                    e, "DPCS coudln't post crash information"
                )
                continue

            script = response.json()['crash_report_ack'][
                                     'solution']['shell_script']

            home = path.expanduser("~")
            scripts_directory = path.join(home, '.local/share/dpcs/')

            # Check if directory exists, create if not
            # Create a script file (using unique id)

            print("DPCS might have found a solution to your problem!")
            print("The script produced by DPCS is available in ")
            print(script)

            print(home)

app = DPCSDaemon()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
