"""
AWS/NIFCLOUD auth v4 plugin for HTTPie.
"""
import os
import sys
import time
import binascii
import re

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from httpie.status import ExitStatus
from httpie.plugins import AuthPlugin

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

__version__ = "0.1.0"
__author__ = "kzmake"
__licence__ = "MIT"

AWS_ACCESS_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_KEY = "AWS_SECRET_ACCESS_KEY"

NIFCLOUD_ACCESS_KEY = "NIFCLOUD_ACCESS_KEY_ID"
NIFCLOUD_SECRET_KEY = "NIFCLOUD_SECRET_ACCESS_KEY"

ACCESS_KEY = "ACCESS_KEY_ID"
SECRET_KEY = "SECRET_ACCESS_KEY"


def fatal_plugin_error(message):
    print(message, file=sys.stderr)
    sys.exit(ExitStatus.PLUGIN_ERROR)


def parse(pattern, domain):
    m = re.search(pattern, domain)

    if m:
        return m.groupdict()

    raise ValueError("ERROR: failed to parse")


class AWSAuth(object):
    def __init__(self, access_key, secret_key, region=None, service=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.service = service

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        if self.access_key is None:
            fatal_plugin_error(f"ERROR: Missing {AWS_ACCESS_KEY} in environment")
        if self.secret_key is None:
            fatal_plugin_error(f"ERROR: Missing {AWS_SECRET_KEY} in environment")

        try:
            host = (
                r.headers.get("Host").decode("utf-8")
                if "Host" in r.headers
                else urlparse(r.url).netloc
            )

            if self.region is None or self.service is None:
                p = parse(
                    r"(?P<service>[^\.]+)\.(?P<region>[^\.]+)\.amazonaws\.com", host
                )
                self.region = p["region"]
                self.service = p["service"]

        except Exception as error:
            fatal_plugin_error(f"ERROR: {error}")
            raise

        auth = AWSRequestsAuth(
            aws_access_key=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_host=host,
            aws_region=self.region,
            aws_service=self.service,
        )

        return auth.__call__(r)


class NIFCLOUDAuth(object):
    def __init__(self, access_key, secret_key, region=None, service=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.service = service

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        if self.access_key is None:
            fatal_plugin_error(f"ERROR: Missing {AWS_ACCESS_KEY} in environment")
        if self.secret_key is None:
            fatal_plugin_error(f"ERROR: Missing {AWS_SECRET_KEY} in environment")

        try:
            host = (
                r.headers.get("Host").decode("utf-8")
                if "Host" in r.headers
                else urlparse(r.url).netloc
            )

            if self.region is None or self.service is None:
                p = parse(
                    r"(?P<region>[^\.]+)\.(?P<service>.+)\.api\.nifcloud\.com", host
                )
                self.region = p["region"]
                self.service = p["service"]

        except Exception as error:
            fatal_plugin_error(f"ERROR: {error}")
            raise

        auth = AWSRequestsAuth(
            aws_access_key=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_host=host,
            aws_region=self.region,
            aws_service=self.service,
        )

        return auth.__call__(r)


class AWSv4AuthPlugin(AuthPlugin):
    """
    AWS auth v4 plugin for HTTPie.
    """

    name = "AWS auth v4"
    auth_type = "aws"
    description = "Sign requests using the AWS Signature Version 4 signature method"
    auth_require = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        access_key = None
        secret_key = None
        region = None
        service = None

        # from arguments:
        examples = """
        examples:
        -a region/service
        -a access_key:secret_key
        -a access_key:secret_key:region/service
        -a access_key:secret_key:region:service
        """
        if self.raw_auth is not None:
            a = self.raw_auth.split(":")
            if len(a) == 1:
                rs = a[0].split("/")
                if len(rs) == 2:
                    region, service = rs[0], rs[1]
                else:
                    fatal_plugin_error(f"ERROR: arguments\n\n{examples}")
            elif len(a) == 2:
                access_key, secret_key = a[0], a[1]
            elif len(a) == 3:
                rs = a[2].split("/")
                if len(rs) == 2:
                    region, service = rs[0], rs[1]
                else:
                    fatal_plugin_error(f"ERROR: arguments\n\n{examples}")
                access_key, secret_key = a[0], a[1]
            elif len(a) == 4:
                access_key, secret_key, region, service = a[0], a[1], a[2], a[3]
            else:
                fatal_plugin_error(f"ERROR: arguments\n\n{examples}")

        # from environment variables: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
        access_key = (
            os.environ.get(AWS_ACCESS_KEY) if access_key is None else access_key
        )
        access_key = os.environ.get(ACCESS_KEY) if access_key is None else access_key
        secret_key = (
            os.environ.get(AWS_SECRET_KEY) if secret_key is None else secret_key
        )
        secret_key = os.environ.get(SECRET_KEY) if secret_key is None else secret_key

        return AWSAuth(
            access_key=access_key, secret_key=secret_key, region=region, service=service
        )


class NIFCLOUDv4AuthPlugin(AuthPlugin):
    """
    NIFCLOUD auth v4 plugin for HTTPie.
    """

    name = "NIFCLOUD auth v4"
    auth_type = "nifcloud"
    description = (
        "Sign requests using the NIFCLOUD Signature Version 4 signature method"
    )
    auth_require = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        access_key = None
        secret_key = None
        region = None
        service = None

        # from arguments:
        examples = """
        examples:
        -a region/service
        -a access_key:secret_key
        -a access_key:secret_key:region/service
        -a access_key:secret_key:region:service
        """
        if self.raw_auth is not None:
            a = self.raw_auth.split(":")
            if len(a) == 1:
                rs = a[0].split("/")
                if len(rs) == 2:
                    region, service = rs[0], rs[1]
                else:
                    fatal_plugin_error(f"ERROR: arguments\n\n{examples}")
            elif len(a) == 2:
                access_key, secret_key = a[0], a[1]
            elif len(a) == 3:
                rs = a[2].split("/")
                if len(rs) == 2:
                    region, service = rs[0], rs[1]
                else:
                    fatal_plugin_error(f"ERROR: arguments\n\n{examples}")
                access_key, secret_key = a[0], a[1]
            elif len(a) == 4:
                access_key, secret_key, region, service = a[0], a[1], a[2], a[3]
            else:
                fatal_plugin_error(f"ERROR: arguments\n\n{examples}")

        # from environment variables: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
        access_key = (
            os.environ.get(NIFCLOUD_ACCESS_KEY) if access_key is None else access_key
        )
        access_key = os.environ.get(ACCESS_KEY) if access_key is None else access_key
        secret_key = (
            os.environ.get(NIFCLOUD_SECRET_KEY) if secret_key is None else secret_key
        )
        secret_key = os.environ.get(SECRET_KEY) if secret_key is None else secret_key

        return NIFCLOUDAuth(
            access_key=access_key, secret_key=secret_key, region=region, service=service
        )
