# -*- coding: utf-8 -*-
from __future__ import print_function
from os import mkdir
from os import path
from random import sample
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
import subprocess
import sys

from requests import get
from requests import post
from requests import RequestException

from systemcheck import systemcheck

EXIT_OK = 0

SERVER_ADDRESS = "http://private-a6e53-dpcs.apiary-mock.com/"


def generate_report(exit_code, stderr_output):
    """Generate a report which will be sent to the DCPS server.

    Arguments
    ---------
    exit_code : int
        The exit code of the failed process

    stderr_output : string
        The output written on stderr by the failed process

    Return
    ------
    template : dict
        The report that can be sent to the DCPS server.
    """
    template = {
        "crash_report": {
            "application": {
                # TO DO - implementation depends on the way how the daemon is
                # implemented
            },
            "system_info": {},
            "exit_code": exit_code,
            "stderr_output": stderr_output
        }
    }

    system_info = systemcheck()

    for k, v in system_info['platform'].iteritems():
        template['crash_report']['system_info'][k] = v

    return template


def handle_request_error(exception, dpcs_message):
    """Handle the exception coming from the requests library.

    Arguments
    ---------
    exception : requests.RequestException
        The request exception caught during the communication with the server.
        Can be anything from 310 to 500

    dpcs_message : string
        The message to be printed. Should describe why DPCS client failed.
    """
    print(dpcs_message, file=sys.stderr)
    print(exception.response.text, file=sys.stderr)


def rand_fname(parent_path, prefix, suffix, length=4):
    """Create a random filename for storing the solution script.

    Arguments
    ---------
    parent_path : string
        The directory where the DCPS script should be stored.

    prefix : string
        The prefix that will be added to the filename.

    suffix : string
        The suffix that will be added to the filename.
        Usually should end with '.sh'

    length : int, optional
        The length of the sequence of random
        haracters in the created filename.

    Return
    ------
    fname : string
        The new file's name.
        The file under this name is guaranteed not to exist.
    """
    chars = ascii_lowercase + ascii_uppercase + digits

    fname = path.join(parent_path,
                      prefix + ''.join(sample(chars, length)) + suffix)

    return fname if not path.exists(fname) else rand_fname(suffix, length)


def run_script(script):
    """Run the solution script.

    Arguments
    ---------
    script : string
        The script's source code.
    """
    subprocess.Popen(script, shell=True)


def save_script(script):
    """Save the solution script under user's home directory.

    Arguments
    ---------
    script : string
        The script's source code.
    """
    home = path.expanduser("~")
    scripts_directory = path.join(home, '.dpcs/')

    if not path.exists(scripts_directory):
        mkdir(scripts_directory)

    filename = rand_fname(scripts_directory,
                          'dpcs_solution_', '.sh')

    with open(filename, 'w+') as f:

        f.write(script)

        print("The script produced by DPCS is available in " +
              filename)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage python client.py '[command to check]'")
        exit(1)

    p = subprocess.Popen(sys.argv[1],
                         stderr=subprocess.PIPE,
                         shell=True)
    _, output = p.communicate()
    code = p.returncode

    print(output)

    if code != EXIT_OK:

        api_description_url = SERVER_ADDRESS + "vd1/paths/"
        try:
            response = get(api_description_url)
        except RequestException as e:
            handle_request_error(
                e, "DPCS couldn't get api description"
            )
            exit(2)

        api_paths = response.json()
        crash_report_url = SERVER_ADDRESS + api_paths["crash-reports"]
        headers = {
          'Content-Type': 'text/json'
        }

        report = generate_report(code, output)

        try:
            response = post(crash_report_url,
                            headers=headers,
                            data=report)
        except RequestException as e:
            handle_request_error(
                e, "DPCS couldn't post crash information"
            )
            exit(3)

        script = response.json()['crash_report_ack'][
                                 'solution']['shell_script']

        print("DPCS might have found a solution to your problem!")
        print("How would you like to use it?")
        resp = ''
        while resp != 'q' and resp != 'r' and resp != 's' and resp != 'p':
            resp = raw_input("(q) - ignore & quit, (r) - run, " +
                             "(s) - save, (p) - print\n")

        if resp == 's':
            save_script(script)
        elif resp == 'r':
            run_script(script)
        elif resp == 'p':
            print(script)
