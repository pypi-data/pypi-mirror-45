"""
Call gitlab-emulator's code to execute a job
"""
import os
import tempfile
import subprocess
import requests

from .trace import TraceProxy


def get_variable(job, name, default=None):
    """
    Get a named variable from a job
    :param job:
    :param name:
    :param default:
    :return:
    """
    for var in job["variables"]:
        if var["key"] == name:
            return var["value"]
    return default


def run(runner, job):
    """
    Execute the given job here using gitlab-emulator
    :param runner: the runner object
    :param job: the job response from the server
    :return:
    """
    from gitlabemu import configloader
    from gitlabemu import logmsg
    from gitlabemu import errors

    trace = TraceProxy(runner, job)

    logmsg.FATAL_EXIT = False

    tempdir = tempfile.mkdtemp(dir=runner.builds)
    build_dir = os.path.join(tempdir, get_variable(job, "CI_PROJECT_PATH"))
    build_dir_abs = os.path.abspath(build_dir)
    os.makedirs(build_dir)

    # clone the git repo defined in the job
    git = job["git_info"]

    trace.write(subprocess.check_output([
        "git", "clone", git["repo_url"], build_dir
    ], cwd=tempdir, stderr=subprocess.STDOUT))

    # checkout the ref to build
    trace.write(subprocess.check_output([
        "git", "checkout", "-f", get_variable(job, "CI_BUILD_REF")
    ], cwd=build_dir_abs, stderr=subprocess.STDOUT))

    # load the config
    ci_file = os.path.join(build_dir_abs,  get_variable(job, "CI_CONFIG_PATH"))
    os.environ["CI_COMMIT_SHA"] = get_variable(job, "CI_COMMIT_SHA")  # work around bug in gitlab-emulator
    config = configloader.read(ci_file)

    # populate real vars
    for var in job["variables"]:
        name = var["key"]
        config["variables"][name] = var["value"]

    emulator_job = configloader.load_job(config, job["job_info"]["name"])
    trace.emulator_job = emulator_job
    emulator_job.stdout = trace

    try:
        emulator_job.run()
    except errors.GitlabEmulatorError:
        # the job failed
        emulator_job.abort()
        return False
    except requests.HTTPError:
        emulator_job.abort()
        return False

    # job passed
    return True
