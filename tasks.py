import os
import sys
import subprocess
from invoke import task


@task
def black(c):
    """
        Run black - invoke black
    """
    if os.name == "nt":
        p = subprocess.Popen(
            [
                "powershell.exe",
                """&poetry run black @(Get-ChildItem -Recurse -Filter *.py| % {$_.FullName})""",
            ],
            stdout=sys.stdout,
        )
        p.communicate()
    else:
        c.run("""find . | grep -E "(\.py$)" | xargs poetry run black""")  # noqa: W605


@task
def flake8(c):
    """
        run flake8 - invoke flake8
    """
    c.run("""poetry run flake8""")


@task
def make_requirements(c):
    """
        Update requirements.txt - invoke make-requirements
    """
    c.run("""poetry export -f requirements.txt > requirements.txt""")


@task
def ready(c):
    black(c)
    flake8(c)
    make_requirements(c)
