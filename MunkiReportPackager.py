#!/usr/bin/python
#
# Copyright 2015 Arjen van Bochoven
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for MunkiReportPackager class"""

from __future__ import absolute_import

import os
import stat
import subprocess

import plistlib
from autopkglib import Processor, ProcessorError

__all__ = ["MunkiReportPackager"]


class MunkiReportPackager(Processor):
    """Creates a package."""
    description = __doc__
    input_variables = {
        "pathname": {
            "required": True,
            "description": "Path to the install script.",
        },
        "version": {
            "required": False,
            "description": "A preferred version"
        },
        "baseurl": {
            "required": True,
            "description": "URL for a Munkireport packager script.",
        }
    }
    output_variables = {
        "pkg_path": {
            "description": "The created package.",
        }
    }

    def main(self):

        # Make script executable
        st = os.stat(self.env["pathname"])
        os.chmod(self.env["pathname"], st.st_mode | stat.S_IEXEC)

        # Packagedir
        packagedir = os.path.join(self.env["RECIPE_CACHE_DIR"], "downloads")
        # Result plist
        resultplist = os.path.join(self.env["RECIPE_CACHE_DIR"],
                                   "result.plist")
        # BaseURL
        baseurl = self.env.get("baseurl")
        if not baseurl.endswith("/"):
            baseurl = baseurl + "/"
        args = [
            self.env["pathname"], "-b", baseurl, "-i", packagedir, "-r",
            resultplist
        ]

        preferred_version = self.env.get("version")
        if preferred_version:
            args = args + ["-v", preferred_version]

        # Call script.
        try:
            proc = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err_out) = proc.communicate()
        except OSError as err:
            raise ProcessorError(
                "The downloaded script contains errors, please check \
%s. (Error code %d: %s)" % (self.env["pathname"], err.errno, err.strerror))
        if proc.returncode != 0:
            raise ProcessorError("creating package for %s failed: %s" %
                                 (self.env["pathname"], err_out))

        if not os.path.isfile(resultplist):
            raise ProcessorError("no result plist found, run against " \
            "Munkireport 2.5.3 or higher")

        # Get package path from resultplist
        result = plistlib.readPlist(resultplist)
        self.output("Created package %s" % result["pkg_path"])
        self.env["pkg_path"] = result["pkg_path"]


if __name__ == '__main__':
    PROCESSOR = MunkiReportPackager()
    PROCESSOR.execute_shell()
