"""
File-like trace bufffer that sends to gitlab
"""


class TraceProxy(object):
    """
    Handle sending trace from the runner to gitlab
    """

    def __init__(self, runner, job):
        self.runner = runner
        self.job = job
        self.offset = 0
        self.emulator_job = None

    def write(self, data):
        """
        Log the given data to the server
        :param data:
        :return:
        """
        if hasattr(data, "encode"):
            data = data.encode()
        self.offset = self.runner.trace(self, data, offset=self.offset)

    def flush(self):
        """
        Flush the buffer
        :return:
        """
        pass

    def close(self):
        """
        Close the buffer
        :return:
        """
        pass
