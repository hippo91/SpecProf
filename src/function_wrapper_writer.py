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
FUNC_PROTO_PATTERN = "^\s*(\w+\s*\**)\s*(\w+)\s*\((.*)\)"
FUNC_PARAMETER_PATTERN = "\s*(?:const)?\s*\w+\s*\**\s*(\w+)"
FUNC_PROTO_PO = re.compile(FUNC_PROTO_PATTERN)
FUNC_PARAMETER_PO = re.compile(FUNC_PARAMETER_PATTERN)

class FunctionWrapperWriter(object):
    """
    A class that creates a c file that wrapps the call to a specific function inside a shared object
    """
    def __init__(self, target_library):
        """
        :param target_library: path to the library to wrap
        :type target_library: str
        """
        self._target_library = target_library
    
    def writeCFile(self, function_symbol = "undefined", function_signature = "undefined", opt_includes = None):
        """
        Write c file wrapper using jinja and template
        
        :param function_symbol: symbol of the function to wrap
        :type function_symbol: str
        :param function_signature: signature of the function to wrap
        :type function_signature: str
        :param opt_includes: optional includes
        :type opt_includes: list
        """
        if opt_includes is not None:
            opt_includes = [opt_includes]
        template = JINJA_ENVIRONMENT.get_template('template_cfile.c')
        func_params = splitFunctionPrototype(target_signature)[2]
        func_params_names = getFunctionParametersNames(func_params)
        template_values = {'opt_includes': opt_includes,
                           'func_signature': function_signature,
                           'target_library': self._target_library,
                           'target_symbol': function_symbol,
                           'func_params': func_params,
                           'func_params_names': ", ".join(func_params_names)}
        print template.render(template_values)


def splitFunctionPrototype(func_prototype):
    """
    Return a tuple made of the :
        - return type of the function,
        - name of the function,
        - parameters list of the function
    which prototype is func_prototype
    
    :param func_prototype: prototype of the function
    :type func_prototype: str
    :return: a tuple containing the return type, the name and the parameters list of the function
    :rtype: tuple
    """
    results = re.search(FUNC_PROTO_PO, func_prototype).groups()
    return (results)
        
        
def getFunctionParametersNames(func_parameters):
    """
    :param func_parameters: parameters of the function as return by the method _getParameters
    :type func_parmaters: str
    :return: name of the parameters of the function
    :rtype: list
    """
    results = re.findall(FUNC_PARAMETER_PO, func_parameters)
    return results

if __name__ == "__main__":
    target_signature = ("""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                        """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""")
    my_func_wrap = FunctionWrapperWriter("""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/XVOF_NP/xvof/"""
                                         """element/vnr_internal_energy_evolution.so""")
    my_func_wrap.writeCFile(function_symbol="solveVolumeEnergy",
                            function_signature="""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                                               """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""",
                            opt_includes="""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                        """nonlinear_solver/Newton/miegruneisen.h""")