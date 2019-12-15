"""
setup.py for httpie-nifcloud-authv4.
"""
from setuptools import setup

try:
    import multiprocessing
except ImportError:
    pass

try:
    import pypandoc

    long_description = pypandoc.convert("README.md", "rst")
except ImportError:
    long_description = open("README.md").read()

setup(
    name="httpie-nifcloud-authv4",
    description="AWS/NIFCLOUD auth v4 plugin for HTTPie.",
    version="0.0.2",
    author="kzmake",
    author_email="kazu.0516.k0n0f@gmail.com",
    license="MIT",
    url="https://github.com/kzmake/httpie-nifcloud-authv4",
    download_url="https://github.com/kzmake/httpie-nifcloud-authv4",
    py_modules=["httpie_nifcloud_authv4"],
    zip_safe=False,
    long_description=long_description,
    entry_points={
        "httpie.plugins.auth.v1": [
            "httpie_aws_authv4 = httpie_nifcloud_authv4:AWSv4AuthPlugin",
            "httpie_nifcloud_authv4 = httpie_nifcloud_authv4:NIFCLOUDv4AuthPlugin",
        ]
    },
    install_requires=["httpie>=1.0.3", "aws-requests-auth>=0.4.2"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
)
