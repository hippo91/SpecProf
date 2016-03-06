# -*- coding: iso-8859-1 -*-
'''
A module implementing the SharedObjectAnalyser class
'''
import os
import logging
import subprocess

logger = logging.getLogger(__name__)

class SharedObjectAnalyser(object):
    """
    A class to analyse contents of a shared object
    """
    def __init__(self, path_to_so):
        """
        :param path_to_so: path to the shared object
        :type path_to_so: str
        """
        self._path_to_so = self._checkPath(os.path.expanduser(path_to_so))
        self._symbols = self._getSymbolNames()

    @staticmethod
    def _checkPath(path):
        """
        Check that the path given corresponds to an existing file with '.so' extension
        
        :param path: path to test
        :type path: str
        :raise IOError: 
                - if the path doesn't exist
                - if it is not a regular file
                - if file extension is not .so  
        """
        logger.info("Checking path ...")
        if not os.path.exists(path):
            msg = "The path {:s} is not an existing file!".format(path)
        elif not os.path.isfile(path):
            msg = "The path {:s} exists but is not a file!".format(path)
        elif not os.path.splitext(path)[1] == ".so":
            msg = "The file under {:s} doesn't seem to be a shared object (.so file)".format(path)
        else:
            logger.info("Path seems to correspond to a shared object")
            return path
        logger.error(msg)
        raise IOError(msg)
    
    def _getSymbolNames(self):
        """
        Get the symbol name in the shared object thanks to nm utility
        
        :return: the list of symbols found in the shared object
        :rtype: list
        """
        logger.info("Trying to get symbol names for the shared object...")
        try:
            cmd = "nm {:s}".format(self._path_to_so)
            logger.info("Call of command : %s", cmd)
            output_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as error:
            logging.error("The command %s doesn't succeed! Return code is : %d", cmd, error.returncode)
            logging.error("%s", error.output)
            raise
        logger.info("Command succeed!")
        output_str = output_bytes.decode("iso-8859-1").split(os.linesep)
        return [line.split(' ')[-1] for line in output_str]

    def askForSymbol(self, func_name):
        """
        Ask the user which symbol is relevant in all symbols matching the function name
        
        :param func_name: name of the fonction to monitor
        :type func_name: str 
        """
        potential_targets = [symb for symb in self._symbols if symb.find(func_name) != -1]
        target = raw_input("""Among all the following symbols which one is of interests?"""
                            """{:s}{:s}{:s}""".format(os.linesep, ":".join(potential_targets), os.linesep))
        if len(target.split()) != 1:
            raise ValueError("Please select only one symbol!")
        return target
        
        
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.INFO)
    my_analyser = SharedObjectAnalyser("""~/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                                       """XVOF_NP/xvof/element/vnr_internal_energy_evolution.so""")
    my_analyser.askForSymbol("solve")