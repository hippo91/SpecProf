"""
A module implementing the SharedObjectAnalyser class
"""
from __future__ import print_function
import os
import logging
import subprocess
from src.colored_logger import ColoredLoggerAdapter

LOGGER = logging.getLogger("SpecProf.shared_library_analysis")
LOGGER.setLevel(logging.DEBUG)
ADAPTER = ColoredLoggerAdapter(LOGGER)


def _exec_and_log(cmd, encoding='iso-8859-1'):
    """
    Execute the command in a subprocess and log the error or the success

    :param cmd: command to execute
    :type cmd: str
    :param encoding: encoding of the output string
    :type encoding: str
    :return: the result of the command
    :rtype: str
    """
    ADAPTER.info("Call of command : < {:s} >".format(cmd))
    try:
        output_bytes = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as error:
        ADAPTER.error("""The command {:s} doesn't succeed!"""
                      """ Return code is : {:d}""".format(cmd, error.returncode))
        ADAPTER.error("{:s}".format(error.output))
        raise
    ADAPTER.info("Command succeed!")
    return output_bytes.decode(encoding).split(os.linesep)


class SharedObjectAnalyser(object):
    """
    A class to analyse contents of a shared object
    """
    def __init__(self, path_to_so):
        """
        :param path_to_so: path to the shared object
        :type path_to_so: str
        """
        self.__path_to_so = self._check_path(os.path.expanduser(path_to_so))
        self.__symbols = self._get_symbol_names()
        self.__language = self._determine_language()
        self.__mangling_map = self._get_symbol_unmangled_map()

    @property
    def language(self):
        """
        Language pty accessor

        :return: language of the library
        :rtype: str
        """
        return self.__language

    @staticmethod
    def _check_path(path):
        """
        Check that the path given corresponds to an existing file with '.so' extension

        :param path: path to test
        :type path: str
        :raise IOError:
                - if the path doesn't exist
                - if it is not a regular file
                - if file extension is not .so
        """
        ADAPTER.info("Checking path : {:s} ...".format(path))
        if not os.path.exists(path):
            msg = "The path {:s} is not an existing file!".format(path)
        elif not os.path.isfile(path):
            msg = "The path {:s} exists but is not a file!".format(path)
        elif not os.path.splitext(path)[1] == ".so":
            msg = "The file under {:s} doesn't seem to be a shared object (.so file)".format(path)
        else:
            ADAPTER.info("Path seems to correspond to a shared object")
            return path
        ADAPTER.error(msg)
        raise IOError(msg)

    def _get_symbol_unmangled_map(self):
        """
        Return a mapping between mangled and unmangled symbols in the shared
        object libraray

        :return: the mapping between mangled and unmangled symbols
        :rtype: dict
        """
        ADAPTER.info("Trying to compute mapping between mangled and unmangled symbols "
                     "in the shared object")
        res = {}
        for _sym in self.__symbols:
            if _sym and self.__language == "c++":
                cmd = "c++filt -it {:s}".format(_sym)
                output_str = _exec_and_log(cmd)
                if output_str[0] != _sym:
                    res[_sym] = output_str[0]
            else:
                res[_sym] = _sym
        return res

    def _get_symbol_names(self):
        """
        Get the symbol name in the shared object thanks to nm utility

        :return: the list of symbols found in the shared object
        :rtype: list
        """
        ADAPTER.info("Trying to get symbol names for the shared object...")
        cmd = "nm {:s}".format(self.__path_to_so)
        output_str = _exec_and_log(cmd)
        return [line.split(' ')[-1] for line in output_str]

    def print_mangling_map(self):
        """
        Print the mapping of mangled and unmangled symbol on sys.stdout
        """
        for key, value in self.__mangling_map.items():
            print("{:s} <==> {:s}".format(key, value))

    def ask_for_symbol(self):
        """
        Ask the user which symbol is relevant.

        :return: a triplet symbol/unmangled name of the symbol/return type
        :rtype: (symbol, unmangled_name, return type)
        """
        self.print_mangling_map()
        answer = raw_input("""Among all the preceeding symbols which one if of interest?"""
                           + os.linesep)
        rtype = raw_input("""For the selected symbol what is the associated return type?""")
        return (answer, self.__mangling_map[answer], rtype)

    def _determine_language(self):
        """
        Try to determine if the library is a C or C++ one

        :return: the language used to build the shared library ('c'|'c++')
        """
        ADAPTER.info("Trying to determine the language (c or c++) of the shared object...")
        cmd = "ldd {:s}".format(self.__path_to_so)
        output_str = _exec_and_log(cmd)
        for lib in output_str:
            lib = lib.lstrip()
            if lib.startswith('libstdc++'):
                ADAPTER.info("The shared library seems to be a C++ one!")
                return 'c++'
        ADAPTER.info("The shared library seems to be a C one!")
        return 'c'


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.INFO)
    my_analyser = SharedObjectAnalyser("""~/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                                       """XVOF_NP/xvof/element/vnr_internal_energy_evolution.so""")
    my_analyser.ask_for_symbol("solve")
