#!/usr/bin/python
"""
A Pure Python gitlab runner
"""

import argparse
import socket

import os
import sys

import time
import yaml
from GitlabPyRunner import consts, runner, executor
from gitlabemu import logmsg


parser = argparse.ArgumentParser()
parser.add_argument("--register",
                    type=str,
                    help="Register a new runner with the server",
                    )
parser.add_argument("--regtoken",
                    type=str,
                    default=None,
                    help="Registration token for --register")

parser.add_argument("--type", type=str,
                    default="shell",
                    help="Set the runner executor eg(shell, docker)")

parser.add_argument("--shell", type=str,
                    help="Set the executor shell")

parser.add_argument("--desc", type=str,
                    help="Set the runner description")

parser.add_argument("--tag", type=str, action="append",
                    help="Add a tag when registering a runner",
                    )
parser.add_argument("--start", type=str,
                    help="Start the runner defined in the config file"
                    )

if __name__ == "__main__":
    opts = parser.parse_args()

    if opts.register:
        if not opts.desc:
            opts.desc = consts.NAME + " on " + socket.gethostname()

        if not opts.tag:
            opts.tag = ["new-python-runner-" + socket.gethostname()]

        if not opts.regtoken:
            raise RuntimeError("missing required --regtoken")

        if not opts.shell:
            opts.shell = os.getenv("COMSPEC", "/bin/sh")

        run = runner.Runner(opts.register, None)
        if opts.shell:
            os.environ["SHELL"] = opts.shell  # TODO pass this into GLE better
        run.register(opts.desc, opts.regtoken, opts.tag)

        if not run.token:
            raise RuntimeError("runner register failed")

        # save the runner config
        tosave = {
            "server": opts.register,
            "token": run.token,
            "executor": opts.type,
            "shell": opts.shell,
            "dir": os.getcwd()
        }

        with open("gitlab-runner.yml", "w") as outfile:
            yaml.dump(tosave, outfile, indent=2)

        logmsg.info("Registration complete. Config saved at '{}'".format(os.path.join(os.getcwd(),
                                                                                      "gitlab-runner.yml")))
        sys.exit(0)

    if opts.start:
        with open(opts.start, "r") as infile:
            config = yaml.load(infile, Loader=yaml.FullLoader)

        assert config

        assert "server" in config
        assert "dir" in config
        assert "executor" in config
        assert "token" in config
        assert "shell" in config

        os.chdir(config["dir"])
        extype = config["executor"]

        if extype == "shell":
            run = runner.Runner(config["server"], config["token"])
        elif extype == "docker":
            run = runner.DockerRunner(config["server"], config["token"])
        else:
            raise RuntimeError("unsupported executor type '{}'".format(extype))

        run.shell = config["shell"]
        while True:
            logmsg.info("Polling for jobs..")
            job = run.poll()
            if not job:
                time.sleep(10)
            else:
                result = executor.run(run, job)
                if result:
                    run.success(job)
                else:
                    run.failed(job)
