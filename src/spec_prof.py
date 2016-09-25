#!/usr/bin/env python2.7
"""
SpecProf, Specialized Profiler, generates a shared object that count calls and measure execution time \
 of a function defined inside a shared object

@author:     gpeillex

@copyright:  2016. All rights reserved.

@license:    GNU-GPL (V3)

@contact:
@deffield    updated: Updated

@todo: planter en cas de non argument
"""

import sys
import logging
import shared_library_analysis
import function_wrapper_writer
import os.path

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from colored_logger import ColoredLoggerAdapter

logger = logging.getLogger('SpecProf')
logger.setLevel(logging.DEBUG)
adapter = ColoredLoggerAdapter(logger)
formatter = logging.Formatter('<<-- %(asctime)s - %(name)s - %(levelname)s - %(message)s -->>')
fh = logging.FileHandler("/tmp/specprof.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


__all__ = []
__version__ = 0.1
__date__ = '2016-03-06'
__updated__ = '2016-09-23'


def _parse_docstring():
    """
    Return the name of the author, the copyright, the license
     and the short description in the docstring

    :return: the name of the author, the copyright, the license and the short description
    """
    doc_l = __import__('__main__').__doc__.split("\n")
    keywords = {'@author': "", '@copyright': "", '@license': ""}
    for line in doc_l:
        for key in keywords.keys():
            if line.startswith(key):
                keywords[key] = line.split(':')[1].strip()
    shortdesc = doc_l[1]
    return keywords['@author'], keywords['@copyright'], keywords['@license'], shortdesc


def main(argv=None):  # IGNORE:C0111
    """Command line options."""

    if argv is not None:
        sys.argv.extend(argv)

    program_author, program_copyright, program_license, program_shortdesc = _parse_docstring()
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_license = """{:s}

  Created by {:s} on {:s}.
  Copyright {:s}

  Licensed under the {:s} License

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""".format(program_shortdesc, program_author, str(__date__), program_copyright, program_license)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-o', '--origin_library', dest="origin_library", help="path to origin library",
                            required=True)
        parser.add_argument('-s', '--signature', dest="signature", metavar="FUNCTION_SIGNATURE",
                            help="signature of the function to measure", required=True)
        parser.add_argument('-w', '--path-to-working-dir', dest="wdir", metavar="PATH_TO_WORKING_DIR",
                            help="path to a directory where source file and shared object will be generated",
                            required=True)
        parser.add_argument('-i', '--optional_includes', dest="opt_inc", metavar="OPTIONAL_HEADERS",
                            help="optional headers to include in the generated src file", nargs="+")
        # Process arguments
        args = parser.parse_args()

        origin_library = os.path.expanduser(args.origin_library)
        function_signature = args.signature
        working_dir = args.wdir
        try:
            single_opt_inc = os.path.abspath(os.path.expanduser(args.opt_inc))
            optional_includes = [single_opt_inc]
        except AttributeError:
            optional_includes = [os.path.abspath(os.path.expanduser(x)) for x in args.opt_inc]

        adapter.info("Analysing the function prototype...")
        r_type, function_name, params = function_wrapper_writer.split_function_prototype(function_signature)
        adapter.info("... done.")
        adapter.info("|_> Return type is : {:s}".format(r_type))
        adapter.info("|_> Function name is : {:s}".format(function_name))
        adapter.info("|_> Parameters are : {:s}".format(params))
        adapter.info("Analysing the shared library...")
        _so_analyser =  shared_library_analysis.SharedObjectAnalyser(origin_library)
        target_symbol = _so_analyser.ask_for_symbol(function_name)
        adapter.info("... done.")
        adapter.info("Generating c file...")
        wrapper_writer = function_wrapper_writer.FunctionWrapperWriter(origin_library, working_dir,
                                                                       language=_so_analyser.language)
        wrapper_writer.write_c_file(target_symbol, function_signature, optional_includes)
        adapter.info("...done.")
        adapter.info("Compiling c file...")
        wrapper_writer.compile_src_file()
        adapter.info("...done.")
        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0

if __name__ == "__main__":
    sys.exit(main())
