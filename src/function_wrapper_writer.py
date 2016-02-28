# -*- coding: iso-8859-1 -*-
'''
A module implementing the FunctionWrapperWriter class
'''
import logging
import subprocess
import os
import jinja2
import re

logger = logging.getLogger(__name__)

PATH_TO_TEMPLATES = os.path.join(os.path.dirname(__file__), "jinja_templates")
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(PATH_TO_TEMPLATES),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)
FUNC_PROTO_PATTERN = "^\s*(\w+\s*\**)\s*(\w+)\s*\(.*\)"
FUNC_PROTO_PO = re.compile(FUNC_PROTO_PATTERN)

class FunctionWrapperWriter(object):
    """
    A class that creates a c file that wrapps the call to a specific function inside a shared object
    """
    def __init__(self, function_symbol):
        """
        :param function_symbol: symbol of the function to wrap
        :type function_symbol: str
        """
        self._function_symbol = function_symbol
    
    def writeCFile(self, filename, function_name):
        """
        Write c file wrapper using jinja and template
        """
        template = JINJA_ENVIRONMENT.get_template('template_cfile.c')
        opt_includes = ["""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                        """nonlinear_solver/Newton/miegruneisen.h"""]
        target_library = ("""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/XVOF_NP/xvof/"""
                         """element/vnr_internal_energy_evolution.so""")
        target_symbol = """solveVolumeEnergy"""
        target_signature = ("""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                           """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""")
        template_values = {'opt_includes': opt_includes,
                           'func_signature': target_signature,
                           'target_library': target_library,
                           'target_symbol': target_symbol}
        print template.render(template_values)

    @staticmethod
    def _getFunctionReturnType(func_prototype):
        """
        Return the return type of the function which prototype is func_prototype
        
        :param func_prototype: prototype of the function
        :type func_prototype: str
        :return: return type of the function
        :rtype: str
        """
        results = re.search(FUNC_PROTO_PO, func_prototype).groups()
        return results[0]
        
    @staticmethod
    def _getFunctionParameters(func_prototype):
        """
        Return the parameters of the function which prototype is func_prototype
        
        :param func_prototype: prototype of the function
        :type func_prototype: str
        :return: parameters of the function in the form : (type name, type name ...)
        :rtype: str  
        """
        results = re.search(FUNC_PROTO_PO, func_prototype).groups()
        return results[2]
        
    @staticmethod
    def _getFunctionParametersNames(func_parameters):
        """
        :param func_parameters: parameters of the function as return by the method _getParameters
        :type func_parmaters: str
        :return: name of the parameters of the function
        :rtype: list
        """

if __name__ == "__main__":
    target_signature = ("""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                        """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""")
    my_func_wrap = FunctionWrapperWriter(None)
    my_func_wrap.writeCFile("toto", "tata")
    print my_func_wrap._getFunctionReturnType(target_signature)
#     my_func_wrap._getFunctionParameters(target_signature)