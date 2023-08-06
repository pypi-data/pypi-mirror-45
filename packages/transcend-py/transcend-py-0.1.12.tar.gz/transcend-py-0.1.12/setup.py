#!/usr/bin/python3 -S
import os
import sys
import uuid
from setuptools import setup


def compat(min_version):
    ''' @min_version: (#str) minimum version number formatted like |2.7|
            or |2.7.6|
        -> (#bool) |True| if the system version is at least @min_version
    '''
    return sys.version_info >= tuple(map(int, min_version.split('.')))


PKG = 'transcend'
PKG_NAME = 'transcend-py'
PKG_VERSION = '0.1.12'

pathname = os.path.dirname(os.path.realpath(__file__))


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return (line for line in lineiter if line and not line.startswith("#"))


install_reqs = parse_requirements(pathname + "/requirements.txt")

setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    description='High performance video and audio transcoding for aliens.',
    author='Jared Lunde',
    author_email='jared.lunde@gmail.com',
    url='https://github.com/jaredlunde/transcend',
    license="MIT",
    install_requires=list(install_reqs),
    packages=[
        'transcend',
        'transcend.codec',
        'transcend.codec.audio',
        'transcend.codec.subtitle',
        'transcend.codec.video',
        'transcend.format',
        'transcend.format.streaming',
        'transcend.preset',
        'transcend.preset.audio',
        'transcend.preset.subtitle',
        'transcend.preset.video',
        'transcend.preset.video.streaming',
        'transcend.protocol',
        'transcend.protocol.input',
        'transcend.protocol.output',
        'transcend.utils',
    ]

)
