# Copyright 2017-2018 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import logging
import os

import click

from guild import version as guild_version
from guild import click_util

from .check import check
from .compare import compare
from .download import download
from .export import export
from .help import help
from .import_ import import_
from .index import index
from .init import init
from .install import install
from .label import label
from .models import models
from .operations import operations
from .package import package
from .packages import packages
from .push import push
from .remotes import remotes
from .resources import resources
from .run import run
from .runs import runs
from .search import search
from .serve import serve
from .shell import shell
from .stop import stop
from .sync import sync
from .tensorboard import tensorboard
from .tensorflow import tensorflow
from .train import train
from .uninstall import uninstall
from .view import view

try:
    _home = os.environ["CONDA_PREFIX"]
except KeyError:
    try:
        _home = os.environ["VIRTUAL_ENV"]
    except KeyError:
        _home = os.path.expanduser("~")

DEFAULT_GUILD_HOME = os.path.join(_home, ".guild")

@click.group(cls=click_util.Group)
@click.version_option(
    version=guild_version(),
    prog_name="guild",
    message="%(prog)s %(version)s"
)
@click.option(
    "-C", "cwd", metavar="PATH",
    help=(
        "Use PATH as current directory for referencing guild "
        "files (guild.yml)."),
    default=".")
@click.option(
    "-H", "guild_home", metavar="PATH",
    help="Use PATH as Guild home (default is {}).".format(DEFAULT_GUILD_HOME),
    default=DEFAULT_GUILD_HOME,
    envvar="GUILD_HOME")
@click.option(
    "--debug", "log_level",
    help="Log more information during command.",
    flag_value=logging.DEBUG)

@click_util.use_args

def main(args):
    """Guild AI command line interface."""
    from . import main_impl
    main_impl.main(args)

main.add_command(check)
main.add_command(compare)
main.add_command(download)
main.add_command(export)
main.add_command(help)
main.add_command(import_)
main.add_command(index)
main.add_command(init)
main.add_command(install)
main.add_command(label)
main.add_command(models)
main.add_command(operations)
main.add_command(package)
main.add_command(packages)
main.add_command(push)
main.add_command(remotes)
main.add_command(resources)
main.add_command(run)
main.add_command(runs)
main.add_command(search)
main.add_command(serve)
main.add_command(shell)
main.add_command(stop)
main.add_command(sync)
main.add_command(tensorboard)
main.add_command(tensorflow)
main.add_command(train)
main.add_command(uninstall)
main.add_command(view)
