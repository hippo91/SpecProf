# -*- coding: iso-8859-1 -*-
from __future__ import print_function

"""
A module implementing the FunctionWrapperWriter class
"""
import logging
import subprocess
import os
import jinja2
import re
from sys import stderr
from colored_logger import ColoredLoggerAdapter

logger = logging.getLogger("SpecProf.function_wrapper_writer")
logger.setLevel(logging.DEBUG)
adapter = ColoredLoggerAdapter(logger)

PATH_TO_TEMPLATES = os.path.join(os.path.dirname(__file__), "jinja_templates")
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(PATH_TO_TEMPLATES),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)


class FunctionWrapperWriter(object):
    """
    A class that creates a c or c++ file that wrapps the call to a specific function inside a shared object
    """
    def __init__(self, target_library, path_to_working_dir, language='c'):
        """
        :param target_library: path to the library to wrap
        :param path_to_working_dir: path to the directory where sources are generated and compiled
        :param language: chosen language (should be the same that the one used to build the target library)
        :type target_library: str
        :type path_to_working_dir: str
        :type language: str ('c'|'cpp'|'c++')
        """
        self._target_library = target_library
        if language not in ['c', 'cpp', 'c++']:
            msg = "Available languages are C ('c') or C++ ('cpp'|'c++')"
            adapter.error(msg)
            raise ValueError(msg)
        if os.path.isdir(path_to_working_dir):
            self._path_to_working_dir = path_to_working_dir
        else:
            msg = "The path {:s} is not a directory!".format(path_to_working_dir)
            adapter.error(msg)
            raise IOError(msg)
        self._language = language
        #
        if self._language == 'c':
            self._src_filename = os.path.splitext(os.path.basename(self._target_library))[0] + "_wrapper.c"
        elif self._language in ['cpp', 'c++']:
            self._src_filename = os.path.splitext(os.path.basename(self._target_library))[0] + "_wrapper.cpp"
        self._src_file_path = os.path.join(self._path_to_working_dir, self._src_filename)

    def write_src_file(self, function_symbol, function_signature, namespace=None, opt_includes=None):
        """
        Write c file wrapper using jinja and template
        
        :param function_symbol: symbol of the function to wrap
        :type function_symbol: str
        :param function_signature: signature of the function to wrap
        :type function_signature: str
        :param opt_includes: optional includes
        :type opt_includes: list
        """
        if self._language == "c":
            template = JINJA_ENVIRONMENT.get_template('template_cfile.c')
        elif self._language in ['c++', 'cpp']:
            template = JINJA_ENVIRONMENT.get_template('template_cppfile.cpp')
        r_type, class_name, func_name, func_params = split_function_prototype(function_signature)
        func_full_decl = class_name
        if not func_full_decl.endswith("::"):
            func_full_decl += "::"
        if func_full_decl == "::":
            func_full_decl = ""
        template_values = {'opt_includes': opt_includes,
                           'func_signature': function_signature,
                           'target_library': self._target_library,
                           'target_symbol': function_symbol,
                           'return_type': r_type,
                           'namespace': namespace,
                           'func_name': func_name,
                           'class_name': class_name,
                           'func_full_decl': func_full_decl,
                           'func_params': func_params,
                           'func_params_names': ", ".join(get_function_parameters_names(func_params))}
        adapter.info("Writing file with following parameters : ")
        adapter.info("Optional includes : '{:s}'".format(template_values['opt_includes']))
        adapter.info("Function signature : '{:s}'".format(template_values['func_signature']))
        adapter.info("Target library : '{:s}'".format(template_values['target_library']))
        adapter.info("Target symbol : '{:s}'".format(template_values['target_symbol']))
        adapter.info("Function return type : '{:s}'".format(template_values["return_type"]))
        adapter.info("Class name : {:s}".format(template_values['class_name']))
        adapter.info("Function name : '{:s}'".format(template_values['func_name']))
        adapter.info("Function full declaration : '{:s}'".format(template_values['func_full_decl']))
        adapter.info("Function parameters : '{:s}'".format(template_values['func_params']))
        adapter.info("Function parameters names : '{:s}'".format(template_values['func_params_names']))
        with open(self._src_file_path, 'w') as fo:
            fo.write(template.render(template_values))
            
    def compile_src_file(self, std="c++11"):
        """
        Compile the src file into a shared object that will wrap the call to the function
        of the original library
        """
        shared_object_name = os.path.splitext(self._src_filename)[0] + ".so"
        common_opts = "-D_GNU_SOURCE  -g -Wall -shared -fPIC -ldl {:s} -o {:s}".format(self._src_filename,
                                                                                       shared_object_name)
        if self._language == 'c':
            cmd = " ".join(["gcc", common_opts])
        else:
            cmd = " ".join(["g++", "-std={:s}".format(std), "-fpermissive", common_opts])
        saved_dir = os.getcwd()
        os.chdir(self._path_to_working_dir)
        try:
            msg = "Launching command :\n{:s}".format(cmd)
            adapter.info(msg)
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as sub_error:
            adapter.error("Problem encountered when executing command : {:s}".format(cmd))
            adapter.error("Return code : {:d}".format(sub_error.returncode))
            adapter.error("Available output : {:s}".format(sub_error.output))
            raise StandardError("Compilation failed!")
        finally:
            os.chdir(saved_dir)
        adapter.info("Compilation terminated successfully")
        print("To launch your program with the wrapper library intercepting original one type :")
        ld_preload = os.path.join(self._path_to_working_dir, shared_object_name)
        print("LD_PRELOAD={:s} /path/to/your/program".format(ld_preload))
        print("Bye!")


def split_function_prototype(func_prototype):
    """
    Return a tuple made of the :
        - return type of the function,
        - class name,
        - name of the function,
        - parameters list of the function

    :param func_prototype: prototype of the function
    :type func_prototype: str
    :return: a tuple containing the return type, the class name,  the name of the function
     and the parameters list of the function
    :rtype: tuple

    >>> test_proto = "void testWithoutMoveCtor(const move_semantics_test::VectorWithMoveSem& vec_a"
    >>> test_proto += ",const move_semantics_test::VectorWithMoveSem& vec_b)"
    >>> split_function_prototype(test_proto) #doctest:+NORMALIZE_WHITESPACE
    ('void ', '', '', 'testWithoutMoveCtor',
    'const move_semantics_test::VectorWithMoveSem& vec_a,const move_semantics_test::VectorWithMoveSem& vec_b')
    >>> test_proto = "double & *  VectorWithoutMoveSem::computeSum("
    >>> test_proto += "const move_semantics_test::VectorWithMoveSem& vec_a)"
    >>> split_function_prototype(test_proto)
    ('double & *  ', 'VectorWithoutMoveSem', 'computeSum', 'const move_semantics_test::VectorWithMoveSem& vec_a')
    """
    r_type, class_name, func_name = [''] * 3
    param_extractor_pattern = r"^(.*)\s*\((.*)\)"
    param_extractor_po = re.compile(param_extractor_pattern)
    left_part_splitter_pattern = r"^\s*(\w+\s*[\*\s*&]*)?\s*(.*)"
    left_part_splitter_po = re.compile(left_part_splitter_pattern)
    left_part, parameters = re.search(param_extractor_po, func_prototype).groups()
    r_type, all_names = re.search(left_part_splitter_po, left_part).groups()
    all_names = all_names.lstrip(":")
    try:
        class_name, func_name = [s.strip() for s in all_names.split("::")]
    except ValueError:
        func_name = all_names.strip()
    return r_type.strip(), class_name, func_name, parameters


def get_function_parameters_names(func_parameters):
    """
    :param func_parameters: parameters of the function as return by the method _getParameters
    :type func_parameters: str
    :return: name of the parameters of the function
    :rtype: list

    >>> test_params = "MieGruneisenParameters_t *params"
    >>> get_function_parameters_names(test_params)
    ['params']
    >>> test_params = "const size_t pb_size"
    >>> get_function_parameters_names(test_params)
    ['pb_size']
    >>> test_params = "const double const * specific_volume"
    >>> get_function_parameters_names(test_params)
    ['specific_volume']
    >>> test_params = "const double const *internal_energy, double* pressure, double* gamma_per_vol, double* c_son"
    >>> get_function_parameters_names(test_params)
    ['internal_energy', 'pressure', 'gamma_per_vol', 'c_son']
    >>> test_params = "const move_semantics_test::VectorWithMoveSem& vec_a"
    >>> test_params += ",const move_semantics_test::VectorWithMoveSem& vec_b"
    >>> get_function_parameters_names(test_params)
    ['vec_a', 'vec_b']
    """
    func_paramater_pattern = "\s*(?:const)?\s*\w+(?:\:\:\w+)?\s*(?:const)?\s*[\*|\&]*\s*(\w+)"
    func_paramater_po = re.compile(func_paramater_pattern)
    results = re.findall(func_paramater_po, func_parameters)
    return results

if __name__ == "__main__":
    target_signature = ("""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                        """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""")
    my_func_wrap = FunctionWrapperWriter("""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/XVOF_NP/xvof/"""
                                         """element/vnr_internal_energy_evolution.so""", "/tmp/test")
    my_func_wrap.write_src_file(
        function_symbol="solveVolumeEnergy",
        function_signature="""void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume,"""
                           """ const double internal_energy, double* pressure, double* gamma_per_vol, double* c_son)""",
        opt_includes=["""/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/"""
                      """nonlinear_solver/Newton/miegruneisen.h"""])
    my_func_wrap.compile_src_file()
