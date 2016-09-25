#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
A module implementing the ElfSharedObjectAnalyser class
"""
from elftools.elf.elffile import ELFFile
import os
import sys


class ElfSharedObjectAnalyser(object):
    """
    This module parses the ELF shared object to retrieve symbols
    """
    def __init__(self, path_to_so):
        """
        :param path_to_so: path to the shared object to analyse
        :type path_to_so: str
        """
        self._path_to_so = path_to_so

    def get_symtab_symbols(self):
        """
        Retrieve all the symbols that have a name in the section .symtab

        :return: all the symbols that have a name in the section .symtab
        :rtype: list
        """
        return self.__get_symbols(".symtab")

    def get_dynsym_symbols(self):
        """
        Retrieve all the symbols that have a name in the section .dynsym

        :return: all the symbols that have a name in the section .dynsym
        :rtype: list
        """
        return self.__get_symbols(".dynsym")

    def get_symbol_names(self):
        """
        Retrieve all the symbols names that are in sections .symtab and .dynsym

        :return: all the symbols names that are in sections .symtab and .dynsym
        :rtype: set
        """
        return set([name for name in self.get_symtab_symbols() + self.get_dynsym_symbols()])

    def __get_symbols(self, section_name):
        """
        Retrieve all the symbols that have a name in the section which name is section_name

        :param section_name: name of the section in which symbols are looked for
        :type section_name: str
        :return: all the symbols that have a name in the section which name is section_name
        :rtype: list
        """
        try:
            with open(self._path_to_so) as fi:
                elffile = ELFFile(fi)
                sym_sec = elffile.get_section_by_name(section_name)
                return [sym.name for sym in sym_sec.iter_symbols() if sym.name]
        except IOError:
            print("Error opening file {:s} for reading!".format(self._path_to_so))

    def ask_for_symbol(self, func_name):
        """
        Ask the user which symbol is relevant in all symbols matching the function name

        :param func_name: name of the function to monitor
        :type func_name: str
        """
        potential_targets = [symbol for symbol in self.get_symbol_names() if symbol.find(func_name) != -1]
        target = raw_input("""Among all the following symbols which one is of interests?"""
                           """{:s}{:s}{:s}""".format(os.linesep, ":".join(potential_targets), os.linesep))
        if len(target.split()) != 1:
            raise ValueError("Please select one and only one symbol!")
        return target

if __name__ == "__main__":
    my_elf = ElfSharedObjectAnalyser(sys.argv[1])
    print my_elf.get_symbol_names()
    if (len(sys.argv) == 3):
        print my_elf.ask_for_symbol(sys.argv[2])

