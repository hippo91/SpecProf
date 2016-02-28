# -*- coding: iso-8859-1 -*-
'''
A module implementing the FunctionWrapperWriter class
'''
import logging
import subprocess
import os
import jinja2

logger = logging.getLogger(__name__)

class FunctionWrapperWriter(object):
    """
    A class that creates a c file that wrapps the call to a specific function
    """
    path_to_templates = os.path.join(os.path.dirname(__file__), "jinja_templates")
    jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path_to_templates),
                                           extensions=['jinja2.ext.autoescape'],
                                           autoescape=True)
    
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
        template = self.jinja_environment.get_template('template_cfile.c')
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

if __name__ == "__main__":
    my_func_wrap = FunctionWrapperWriter(None)
    my_func_wrap.writeCFile("toto", "tata")