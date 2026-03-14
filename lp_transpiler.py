import os #required to evaluate file extension
import re #required to evaluate regular expressions from latex files

from sympy import sympify, latex
from sympy.utilities.mathml import mathml to sympy

def get_input_type(file_path):
    ext = os.path.splittext(file_path)[1].lower()
    if ext in ('.mml', '.mathml'):
        return 'mathml'
    if ext in ('.tex', '.latex'):
        return 'latex'
    raise ValueError("Unsupported file type.")
