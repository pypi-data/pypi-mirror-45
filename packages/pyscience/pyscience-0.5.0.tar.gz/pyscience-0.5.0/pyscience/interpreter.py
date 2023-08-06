"""
pyscience - python science programming
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import os
import traceback
import pyscience

from pyscience import parser
from pyscience.algebra import get_variables
from pyscience.algebra.equation import Equation
from pyscience.chemistry.element import ChemicalElement
from pyscience.math import Fraction, div, MATH_FUNCTIONS
from pyscience.units import Units

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory


def get_args(args: dict) -> str:
    result = ''
    for val in args.keys():
        result += val + '=' + args[val] + ','
    return result[:-1]


class PyscienceInterpreter:

    def __init__(self):
        self._globals = dict()
        self.history_file = os.path.expanduser('~/.pyscience_history')
        self.session = PromptSession(history=FileHistory(self.history_file))

        # Variables
        for variable in get_variables('x y z a b c n m l'):
            self._globals[variable.name] = variable

        self._globals['Eq'] = Equation

        # Chemical element
        self._globals['Ce'] = ChemicalElement

        # Fractions
        self._globals['F'] = Fraction

        # Units
        self._globals['Units'] = Units()

        # Math
        self._globals['Div'] = div
        for func in MATH_FUNCTIONS:
            self._globals[func] = MATH_FUNCTIONS[func]

    def input(self) -> str:
        return self.session.prompt('> ')

    @staticmethod
    def print_exception():
        type_, value, tb = sys.exc_info()
        list_ = traceback.format_tb(tb, None) + traceback.format_exception_only(type_, value)

        if pyscience.DEBUG:
            print('Traceback (most recent call last):')
            print(''.join(list_[:-1]))
        print(list_[-1][:-1])

        del tb

    def exec_function(self, cmd):
        func = None
        code = cmd

        if ':' in cmd:
            code = cmd[:cmd.index(':')]
            func = cmd[cmd.index(':'):]

        try:
            code = parser.expand(code)
        except SyntaxError as e:
            print('SyntaxError:', e)
            return

        if func:
            if func.startswith(':'):
                func_name = func.split()[0][1:]
                values = func[len(func_name) + 1:].replace(' ', '')
                args = {}
                if values:
                    for val in values.split(','):
                        name, value = val.split('=')
                        args[name] = value
                        if not value:
                            print(f'Error: value of {name} not specified')
                            return

                if func_name == "clear":
                    with open(self.history_file, 'w') as fd:
                        fd.write('')

                    print("Session clean")
                else:
                    code = '(' + code + ').' + func_name + '(' + get_args(args) + ')'

        if pyscience.DEBUG:
            print(f'eval: "{code}"')

        try:
            if code:
                result = eval(code, self._globals)
                if pyscience.DEBUG:
                    print('result type:', type(result))
                    print('result repr:', repr(result))
                print(result)
        except:
            self.print_exception()
