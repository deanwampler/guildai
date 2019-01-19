# Copyright 2017-2019 TensorHub, Inc.
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

import logging
import os
import shutil
import sys

from six.moves import shlex_quote

from guild import _api as gapi
from guild import op_util
from guild import run as runlib
from guild import var

log = logging.getLogger("guild")

class Trial(object):

    def __init__(self, batch, flags):
        self._batch = batch
        self._flags = flags
        self._run_id = runlib.mkid()
        self._trial_link = os.path.join(
            self._batch.batch_run.path, self._run_id)

    def _flag_assigns(self):
        format_val = lambda val: shlex_quote(op_util.format_flag_val(val))
        return [
            "%s=%s" % (name, format_val(self._flags[name]))
            for name in sorted(self._flags)
        ]

    @property
    def flags(self):
        return self._flags

    @property
    def initialized(self):
        return os.path.exists(self._trial_link)

    @property
    def run_deleted(self):
        return (
            os.path.exists(self._trial_link) and
            not os.path.exists(os.path.realpath(self._trial_link)))

    def init(self):
        if not os.path.exists(self._trial_link):
            trial_run = self._init_trial_run()
            os.symlink(trial_run.path, self._trial_link)

    def _init_trial_run(self):
        run_dir = os.path.join(var.runs_dir(), self._run_id)
        shutil.copytree(self._batch.proto_run.path, run_dir)
        run = runlib.Run(self._run_id, run_dir)
        run.write_attr("flags", self._flags)
        run.write_attr("label", " ".join(self._flag_assigns()))
        return run

    def run(self):
        trial_run = self._initialized_trial_run()
        if not trial_run:
            raise RuntimeError("trial not initialized - needs call to init")
        opspec = trial_run.opref.to_opspec()
        log.info("Running %s (%s)", opspec, ", ".join(self._flag_assigns()))
        try:
            gapi.run(
                restart=trial_run.id,
                cwd=os.environ["CMD_DIR"],
                extra_env={"NO_RESTARTING_MSG": "1"})
        except gapi.RunError as e:
            sys.exit(e.returncode)

    def _initialized_trial_run(self):
        if not os.path.exists(self._trial_link):
            return None
        run_dir = os.path.realpath(self._trial_link)
        run_id = os.path.basename(run_dir)
        return runlib.Run(run_id, run_dir)

class Batch(object):

    def __init__(self, batch_run):
        self.batch_run = batch_run
        self.proto_run = self._init_proto_run()

    def _init_proto_run(self):
        proto_path = self.batch_run.guild_path("proto")
        if not os.path.exists(proto_path):
            op_util.exit("missing operation proto in %s" % proto_path)
        return runlib.Run("", proto_path)

def init_batch():
    return Batch(op_util.current_run())

def print_trials(trials):
    op_util.print_trials([t.flags for t in trials])