# -*- coding: utf-8 -*-
"""scratchrelaxtv module.

scratchrelaxtv (anagram of extract-hcl-vars) is a Terraform development
convenience tool that extracts vars from HCL and creates an HCL variables file
with the extracted vars. The point is to make creating Terraform modules
easier.

Example:
    Help using the scratchrelaxtv CLI can be found by typing the following::

        $ scratchrelaxtv --help
"""

import logging
import logging.config
import os
import re


__version__ = "0.1.2"
EXIT_OKAY = 0
EXIT_NOT_OKAY = 1

logging.config.fileConfig(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf'))
logger = logging.getLogger(__name__)        # pylint: disable=invalid-name


def remove_prefix(text, prefix):
    """Remove prefix from a string."""
    return text[text.startswith(prefix) and len(prefix):]


class VarExtractor():
    """
    A class that extracts variables from Terraform HCL files to make creating
    Terraform modules easier.
    """

    def __init__(self, args):
        """Instantiate"""

        self.args = args
        self.tf_vars = []
        self.tf_lists = []
        self.log_arguments()

    def log_arguments(self):
        """Log all the attributes of this run."""
        logger.info("input file: %s", self.args.input)
        logger.info("output file: %s", self.args.output)

        if self.args.force:
            logger.info("forcing overwrite of output file")
        else:
            logger.info("not forcing overwrite of output file")

        if self.args.asc:
            logger.info("ordering output file ascending")
        elif self.args.desc:
            logger.info("ordering output file descending")
        else:
            logger.info("not ordering output file")

    def _find_non_existing_filename(self):
        index = 1
        while True:
            if self.args.force or not os.path.isfile(self.args.output):
                return
            filename, file_extension = os.path.splitext(self.args.output)
            pattern = re.compile(r'(.*)\.(\d+)')
            search = pattern.search(filename)
            if search:
                filename = search.group(1)
                index = int(search.group(2)) + 1
            self.args.output = ''.join([
                filename, '.', str(index), file_extension])
            index += 1

    def write_file(self):
        """Output vars to .tf file."""
        self._find_non_existing_filename()
        with open(self.args.output, "w", encoding='utf_8') as file_handle:
            for tf_var in self.tf_vars:
                file_handle.write('variable "')
                file_handle.write(remove_prefix(tf_var, "var."))
                file_handle.write('" {\n')
                file_handle.write('  description = ""\n')
                if tf_var in self.tf_lists:
                    file_handle.write('  type        = "list"\n')
                    file_handle.write('  default     = []\n')
                else:
                    file_handle.write('  type        = "string"\n')
                    file_handle.write('  default     = ""\n')
                file_handle.write('}\n\n')

    def extract(self):
        """Extract vars from .tf file."""
        with open(self.args.input) as file_handle:
            entire_file = file_handle.read()

            interpol_pattern = re.compile(r'(\[")?\$\{([^\}]*)\}("\])?')
            interpolations = interpol_pattern.findall(entire_file)

            # According to Hashicorp re valid var names:
            # "A name must start with a letter and may contain only letters,
            # digits, underscores, and dashes."
            var_pattern = re.compile(r'\b(var\.[a-zA-Z][a-zA-Z0-9_-]*)\b')
            tf_vars = []
            tf_lists = []
            for interpolation in interpolations:
                new_vars = var_pattern.findall(interpolation[1])
                tf_vars += new_vars
                if interpolation[0]:  # see if it looks like a list
                    tf_lists += new_vars

            tf_vars = list(dict.fromkeys(tf_vars))
            tf_lists = list(dict.fromkeys(tf_lists))

            if self.args.asc:
                tf_vars.sort()
            elif self.args.desc:
                tf_vars.sort(reverse=True)

            self.tf_vars = tf_vars
            self.tf_lists = tf_lists

        self.write_file()

        return EXIT_OKAY
