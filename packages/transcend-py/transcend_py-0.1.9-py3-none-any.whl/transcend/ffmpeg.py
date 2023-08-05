# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import urllib
from collections import namedtuple
from threading import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from vital.debug import logg

from .cli import *
from .exceptions import FastStartError
from . import faststart


__all__ = 'Ffmpeg',


FfmpegResult = namedtuple('FfmpegResult', 'stdout stderr')


def _process_stdout(stdout_queue, stdout, STDOUT):
    try:
        std = stdout_queue.get_nowait()
        if stdout is not None:
            std = stdout(std)
        if std is not None:
            STDOUT += std
    except Empty:
        pass

    return STDOUT


class Ffmpeg(Runnable):
    '''
    -loglevel loglevel  set logging level
    -v loglevel         set logging level
    -report             generate a report
    -max_alloc bytes    set maximum size of a single allocated block
    -y                  overwrite output files
    -n                  never overwrite output files
    -ignore_unknown     Ignore unknown stream types
    -stats              print progress report during encoding
    -max_error_rate ratio of errors (0.0: no errors, 1.0 max errors)
    -bits_per_raw_sample number  set the number of bits per raw sample
    -vol volume         change audio volume (256=normal)
    '''
    __slots__ = 'input', '_opts', '_with_schedtool', 'BIN'
    OPT = [
        Flag('y', 'overwrite'),
        Flag('n', 'never_overwrite'),
        Flag('h', 'help'),
        Flag('ignore_unknown'),
        Flag('stats', 'show_stats'),
        Flag('generate_report', 'report'),
        ByteOpt('max_alloc'),
        BoundedOpt(
            'max_error_rate', lower=0.0, upper=1.0, cast=float
        ),
        IntOpt('bits_per_raw_sample', 'bits_per_sample'),
        IntOpt('vol', 'volume'),
        OneOfOpt(
            'loglevel',
            choices=(
                "quiet",
                "panic",
                "fatal",
                "error",
                "warning",
                "info",
                "verbose",
                "debug",
                "trace"
            )
        )
    ]

    def __init__(
        self,
        input=None,
        with_schedtool=False,
        bin=None,
        *opt,
        **opts
    ):
        super(Ffmpeg, self).__init__(*(list(opt) + self.OPT), **opts)
        self.BIN = bin or os.path.join(os.path.expanduser('~'), 'bin/ffmpeg')
        self._with_schedtool = with_schedtool
        self.open(input)

    def open(self, input):
        if input is None:
            pass
        elif input.startswith('s3://'):
            pass
        elif input.startswith('ftp://'):
            pass
        elif input.startswith('sftp://'):
            pass
        elif input.startswith('http://'):
            pass
        else:
            input = humanfriendly.parse_path(input)
        self.input = input

    def get_input(self):
        if self.input is not None:
            for opt in self.input.live_opts:
                for x in opt.to_proc():
                    yield x

    SCHED_CMD = ['sudo', 'schedtool', '-R', '-p', '99', '-e']

    def get_cmd(self, *outputs):
        if self._with_schedtool:
            for cmd in self.SCHED_CMD:
                yield cmd
        for cmd in super(Ffmpeg, self).get_cmd():
            yield cmd
        for cmd in self.get_input():
            yield cmd
        for output in outputs:
            for opt in output.live_opts:
                for step in opt:
                    yield str(step)

    def get_pretty_cmd(self, *outputs):
        if self._with_schedtool:
            for cmd in self.SCHED_CMD:
                yield cmd
        for cmd in super(Ffmpeg, self).get_cmd():
            yield cmd
        for cmd in self.get_input():
            yield cmd
        for output in outputs:
            yield '\\\n'
            for opt in output.live_opts:
                for step in opt:
                    yield str(step)

    @staticmethod
    def _handle_stdout(stdout, queue):
        ''' bytes from the stdout pipe pass through here '''
        for line in iter(stdout.readline, b''):
            # line == line of bytes from stdout
            queue.put_nowait(line)
        stdout.close()

    def handle_stdout(self, stdout):
        """ @stdout: listens to stdout pipe
            -> :class:Queue
        """
        q = Queue()
        t = Thread(target=self._handle_stdout, args=(stdout, q))
        t.daemon = True
        t.start()
        return q

    def _get_stream_iterator(self, proc, no_faststart):
        # return self.input.iter_body()
        if not no_faststart:
            try:
                fs = faststart.FastStart()
                stream = fs.from_stream(self.input.body)
                proc.stdin.write(next(stream))
            except FastStartError as e:
                def _stream(fs):
                    fs.cache.seek(0)
                    yield fs.cache.read()
                    for data in fs.iter_stream():
                        yield data
                stream = _stream(fs)
        else:
            stream = self.input.iter_body()

        return stream

    def _exec_pipe(self, *outputs, stdout=None, stderr=None,
                   no_faststart=False):
        builtin_modules = sys.builtin_module_names
        proc = subprocess.Popen(
            self.get_cmd(*outputs),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds='posix' in builtin_modules
        )

        stdout_queue = self.handle_stdout(proc.stdout)
        stderr_queue = self.handle_stdout(proc.stderr)
        STDERR = b''
        STDOUT = b''
        stream = self._get_stream_iterator(proc, no_faststart)

        while proc.poll() is None:
            if not proc.stdin.closed:
                try:
                    proc.stdin.write(next(stream))
                except StopIteration:
                    proc.stdin.close()
                except BrokenPipeError:
                    # NEEDS A HANDLER
                    proc.stdin.close()
                except:
                    continue

            # ts.protocol.Pipe outputs to stdout
            # mp4 muxer does not support non seekable output
            STDOUT = _process_stdout(stdout_queue, stdout, STDOUT)
            STDERR = _process_stdout(stderr_queue, stderr, STDERR)

        #: Finishes off the thread queues
        time.sleep(1.0)
        while not stdout_queue.empty():
            STDOUT = _process_stdout(stdout_queue, stdout, STDOUT)
        while not stderr_queue.empty():
            STDERR = _process_stdout(stderr_queue, stderr, STDERR)

        return FfmpegResult(STDOUT, STDERR)

    def _exec_native(self, *outputs, stdout=None, stderr=None):
        builtin_modules = sys.builtin_module_names
        proc = subprocess.Popen(
            self.get_cmd(*outputs),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds='posix' in builtin_modules
        )

        STDOUT, STDERR = proc.communicate()

        return FfmpegResult(STDOUT, STDERR)

    def save(self, *outputs, stdout=None, stderr=None):
        logg('\n',
             subprocess.list2cmdline(self.get_pretty_cmd(*outputs))
        ).log('Executing')

        if hasattr(self.input, 'body'):
            result = self._exec_pipe(*outputs, stdout=stdout, stderr=stderr)
        else:
            result = self._exec_native(*outputs, stdout=stdout, stderr=stderr)

        try:
            self.input.close()
        except AttributeError:
            pass

        return result

    run = save
