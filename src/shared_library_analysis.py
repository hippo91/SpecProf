"""
A module implementing the SharedObjectAnalyser class
"""
import os
import logging
import subprocess
from colored_logger import ColoredLoggerAdapter

logger = logging.getLogger("SpecProf.shared_library_analysis")
logger.setLevel(logging.DEBUG)
adapter = ColoredLoggerAdapter(logger)


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

    @property
    def language(self):
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
        adapter.info("Checking path : {:s} ...".format(path))
        if not os.path.exists(path):
            msg = "The path {:s} is not an existing file!".format(path)
        elif not os.path.isfile(path):
            msg = "The path {:s} exists but is not a file!".format(path)
        elif not os.path.splitext(path)[1] == ".so":
            msg = "The file under {:s} doesn't seem to be a shared object (.so file)".format(path)
        else:
            adapter.info("Path seems to correspond to a shared object")
            return path
        adapter.error(msg)
        raise IOError(msg)
    
    def _get_symbol_names(self):
        """
        Get the symbol name in the shared object thanks to nm utility
        
        :return: the list of symbols found in the shared object
        :rtype: list
        """
        adapter.info("Trying to get symbol names for the shared object...")
        cmd = "nm {:s}".format(self.__path_to_so)
        try:
            adapter.info("Call of command : {:s}".format(cmd))
            output_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as error:
            adapter.error("The command {:s} doesn't succeed! Return code is : {:d}".format(cmd, error.returncode))
            adapter.error("{:s}".format(error.output))
            raise
        adapter.info("Command succeed!")
        output_str = output_bytes.decode("iso-8859-1").split(os.linesep)
        return [line.split(' ')[-1] for line in output_str]

    def ask_for_symbol(self, func_name, class_name=None, namespace=None):
        """
        Ask the user which symbol is relevant in all symbols matching the function name
        
        :param func_name: name of the function to monitor
        :type func_name: str 
        """
        potential_targets = {symbol for symbol in self.__symbols if symbol.find(func_name) != -1}

        if len(potential_targets) != 1:
            target = raw_input("""Among all the following symbols which one is of interests?"""
                               """{:s}{:s}{:s}""".format(os.linesep, ", ".join(potential_targets), os.linesep))
        else:
            target = potential_targets.pop()
        if len(target.split()) != 1:
            adapter.error("Please select only one symbol!")
            raise ValueError("Please select only one symbol!")
        return target

    def _determine_language(self):
        """
        Try to determine if the library is a C or C++ one

        :return: the language used to build the shared library ('c'|'c++')
        """
        adapter.info("Trying to determine the language (c or c++) of the shared object...")
        cmd = "ldd {:s}".format(self.__path_to_so)
        try:
            adapter.info("Call of command : {:s}".format(cmd))
            output_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as error:
            adapter.error("The command {:s} doesn't succeed! Return code is : {:d}".format(cmd, error.returncode))
            adapter.error("{:s}".format(error.output))
            raise
        adapter.info("Command succeed!")
        output_str = output_bytes.decode("iso-8859-1").split(os.linesep)
        for lib in output_str:
            lib = lib.lstrip()
            if lib.startswith('libstdc++'):
                adapter.info("The shared library seems to be a C++ one!")
                return 'c++'
        adapter.info("The shared library seems to be a C one!")
        return 'c'
        
        
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.INFO)
    my_analyser = SharedObjectAnalyser("""~/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                                       """XVOF_NP/xvof/element/vnr_internal_energy_evolution.so""")
    my_analyser.ask_for_symbol("solve")
