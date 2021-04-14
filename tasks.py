import os
import sys
import subprocess
from invoke import task


@task
def black(context):
    """
    Run black - invoke black
    """
    if os.name == "nt":
        sub_popen = subprocess.Popen(
            [
                "powershell.exe",
                """&poetry run black @(Get-ChildItem -Recurse -Filter *.py| % {$_.FullName})""",
            ],
            stdout=sys.stdout,
        )
        sub_popen.communicate()
    else:
        context.run(
            """find . | grep -E "(\.py$)" | xargs poetry run black"""  # noqa: W605 pylint: disable=anomalous-backslash-in-string
        )


@task
def flake8(context):
    """
    run flake8 - invoke flake8
    """
    context.run("""poetry run flake8""")


@task
def pylint(context):
    """
    run pylint - invoke pylint
    """
    context.run("""poetry run pylint tests src *.py""")


@task
def make_requirements(context):
    """
    Update requirements.txt - invoke make-requirements
    """
    context.run("""poetry export -f requirements.txt > requirements.txt""")


@task
def ready(context):
    """
    ready code for commit
    """
    black(context)
    flake8(context)
    pylint(context)
    make_requirements(context)
