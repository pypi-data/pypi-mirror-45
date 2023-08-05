# -*- coding: utf-8 -*-
import io
import pathlib
from awstools import S3Manager
from vital.cache import cached_property
from ..cli import *
from ._protocol import Protocol
from .pipe import Pipe
from .file import FileIn


__all__ = 'S3In', 'S3Out', 'S3BytesIn', 'S3FileIn', 'S3OptimalIn'


class _S3(Pipe):
    """
    `S3 input/output protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    @bucket: (#str) name of the S3 bucket to pull the file from or put the
        file to
    @filename: (#str) name of the file to pull or output to and from S3
    @put_opt: (#dict) keyword arguments to pass to boto.client.put_object
    """
    NUMBER = 0

    def __init__(self, *opt, **opts):
        """ @endpoint: (#str) e.g. s3://your.bucket/path/to/vid.mp4 """
        super().__init__(*opt, **opts)
        self.manager = S3Manager()

    @staticmethod
    def parse_endpoint(endpoint):
        endpoint = endpoint.split('s3://', 1)[1]
        return endpoint.split('/', 1)


class S3In(_S3):
    NUMBER = 0

    def __init__(self, endpoint, *opt, buffer_size=1024 * 1024 * 24, **opts):
        """ @endpoint: (#str) e.g. s3://your.bucket/path/to/vid.mp4 """
        self.bucket, self.filename = self.parse_endpoint(endpoint)
        self.buffer = buffer_size
        super().__init__(*opt, **opts)

    @cached_property
    def body(self):
        return self.manager.get_file(self.bucket, self.filename).get()['Body']

    def iter_body(self):
        while True:
            chunk = self.body.read(self.buffer)
            if not len(chunk):
                break
            yield chunk


class S3FileIn(FileIn):
    NUMBER = 0

    def __init__(
        self,
        s3_endpoint,
        local_path,
        *opt,
        **opts
    ):
        """ @endpoint: (#str) e.g. s3://your.bucket/path/to/vid.mp4 """
        self.bucket, filename = _S3.parse_endpoint(s3_endpoint)
        self.path = pathlib.Path(local_path)
        self.path.parent.mkdir(0o744, parents=True, exist_ok=True)

        super().__init__(str(self.path), *opt, **opts)
        self.manager = S3Manager()
        self.manager.client.download_file(self.bucket, filename, str(self.path))

    def close(self):
        self.path.unlink()


class S3BytesIn(S3In):
    NUMBER = 0

    @cached_property
    def body(self):
        body = io.BytesIO()
        self.manager.client.download_fileobj(self.bucket, self.filename, body)
        body.seek(0)
        return body

    def iter_body(self):
        self.body.seek(0)

        while True:
            chunk = self.body.read(self.buffer)
            if not len(chunk):
                break
            yield chunk


def S3OptimalIn(
    s3_endpoint,
    local_path,
    *args,
    bytes_thresh=1024 * 1024 * 24,
    file_thresh=1024 * 1024 * 240,
    **kwargs
):
    s3 = _S3()
    bucket, key = s3.parse_endpoint(s3_endpoint)
    response = s3.manager.client.head_object(Bucket=bucket, Key=key)
    size = response['ContentLength']

    if size >= bytes_thresh:
        if size >= file_thresh:
            print(f'*** Writing S3 to file first [{local_path}] ***')
            return S3FileIn(s3_endpoint, local_path, *args, **kwargs)
        else:
            print('*** Writing S3 to BytesIO object first ***')
            return S3BytesIn(s3_endpoint, *args, **kwargs)
    else:
        print('*** Streaming S3 through pipe ***')
        return S3In(s3_endpoint, *args, **kwargs)


class S3Out(_S3):
    NUMBER = 1

    def __init__(self, endpoint, put_opt=None, *opt, **opts):
        """ @endpoint: (#str) e.g. s3://your.bucket/path/to/vid.mp4 """
        self.bucket, self.filename = self.parse_endpoint(endpoint)
        self.put_opt = put_opt
        super().__init__(*opt, **opts)

    def put(self, body):
        return self.manager.upload_stream(
            self.bucket,
            self.filename,
            body,
            **self.put_opt
        )


class S3Pipe(_S3):
    pass
