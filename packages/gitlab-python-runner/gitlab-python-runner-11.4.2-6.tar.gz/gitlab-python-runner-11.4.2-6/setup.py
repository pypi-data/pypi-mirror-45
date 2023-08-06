from distutils.core import setup
from GitlabPyRunner import consts

setup(
    name="gitlab-python-runner",
    version=consts.VERSION,
    description="Pure python gitlab-runner",
    author="Ian Norton",
    author_email="inorton@gmail.com",
    url="https://gitlab.com/cunity/gitlab-python-runner",
    packages=["GitlabPyRunner"],
    scripts=["gitlab-runner.py"],
    install_requires=["pyyaml", "requests", "gitlab-emulator==0.0.20"],
    platforms=["any"],
    license="License :: OSI Approved :: MIT License",
    long_description="Gitlab compatible runner without Go or SSH"
)
