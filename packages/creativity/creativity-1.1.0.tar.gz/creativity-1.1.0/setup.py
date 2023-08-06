import random
import os
import signal
import sys
import time

from setuptools import setup, find_packages
from setuptools.command.install import install as _install

cool_videos = [
    "https://asciinema.org/a/3",
    "https://asciinema.org/a/18744",
    "https://asciinema.org/a/19919",
    "https://asciinema.org/a/20055",
    "https://asciinema.org/a/41475",
    "https://asciinema.org/a/113643",
    "https://asciinema.org/a/117813",
    "https://asciinema.org/a/147864",
    "https://asciinema.org/a/155441",
    "https://asciinema.org/a/168763",
]
def play_video():
    parent = os.getppid()
    try:
        # I'ma be real with you chief: I have no idea WHY we need to fork.
        pid = os.fork()
        if pid:
            os.waitpid(pid, 0) # This doesn't seem to work...
            raise Exception("Have a nice day.")

        # Restore FDs
        sys.stdout = open('/proc/{}/fd/1'.format(parent), sys.stdout.mode)
        sys.stderr= open('/proc/{}/fd/2'.format(parent), sys.stderr.mode)

        # Send newline before the video
        print()

        # Pick a video
        random.seed() # Appeared to have been semi-deterministic
        todays_video = random.choice(cool_videos)

        # Show the video
        from asciinema.commands.play import PlayCommand
        PlayCommand(todays_video, 3000, 1).execute()

        # Exit with a friendly message
        print()
        print("We hope you are inspired. That was {}".format(todays_video))
        print()

        # Uninstall self for repeatability
        os.system("pip uninstall --yes creativity")
        os.kill(parent, signal.SIGINT)
    except ImportError:
        pass

class install(_install):
    def run(self):
        super().run()
        play_video()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="creativity",
    version="1.1.0",
    author="Arlan Jaska",
    author_email="akjaska@gmail.com",
    description="Quick inspiration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajaska/creativity",
    packages=find_packages(),
    install_requires=["asciinema"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Artistic Software",
    ],
    cmdclass = {'install': install},
)
