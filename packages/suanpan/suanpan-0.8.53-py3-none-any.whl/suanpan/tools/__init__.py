# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.docker import DockerComponent


class ToolComponent(DockerComponent):
    ENABLED_BASE_SERVICES = {"dw", "storage"}
