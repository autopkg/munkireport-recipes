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

"""See docstring for MunkiReportUrlCreator class"""

from __future__ import absolute_import

from autopkglib import Processor, ProcessorError

__all__ = ["MunkiReportUrlCreator"]

class MunkiReportUrlCreator(Processor):
    """Provides URL to the latest update."""
    description = __doc__
    input_variables = {
        "baseurl": {
            "required": True,
            "description": "URL for a Munkireport packager script.",
        },
        "modules": {
            "required": False,
            "description":
                "Array of modules to include in the install.",
        }
    }
    output_variables = {
        "url": {
            "description": "URL for a download.",
        }
    }

    def main(self):
        """Get URL for latest version"""

        url = self.env.get("baseurl") + "/index.php?/install/modules"

        # Add modules if provided
        modules = self.env.get("modules")
        if modules:
            for module in modules:
                url = url + '/' + module
            # Format description

        self.env["url"] = url
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = MunkiReportUrlCreator()
    PROCESSOR.execute_shell()
