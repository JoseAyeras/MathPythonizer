import os #required to evaluate file extension
import re #required to evaluate regular expressions from latex files
import sys #required to process number of args

#from sympy import sympify, latex
#from sympy.utilities.mathml import mathml to sympy

#generates a python function given the name of the function, the arguments inside the function, and an expression
def generate_python_function(func_name, args, expr):
    args_str = ', '.join(args)
    #args_str = ', '.join([f'x{i+1}' for i in range(int(num_args))])
    return f"def {func_name}({args_str}):\n    return {expr}\n"

def get_input_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ('.mml', '.mathml'):
        #return 'mathml'
        print("reached mml block")
        #raise ValueError("MathML not yet supported.\n")
        sys.exit("MathML not yet supported.\n")
    if ext in ('.tex', '.latex'):
        return 'latex'
    print("didn't reach latex block'")
    #raise ValueError
    sys.exit("Unsupported file type. Expected LaTeX (?.tex or ?.latex) or MathML(?.mml or ?.mathml).\n")

def parse_latex(latex_str):
    #match = re.match(r'\\?([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*=\s*(.+)', latex_str)
    #match = re.search(r'\\\[\s*([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*=\s*(.*?)\s*\\\]', latex_str)
    match = re.search(r'\\\[?([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*=\s*(.*?)\s*\\\]', latex_str)
    if not match:
        raise ValueError("Could not parse function definition from LaTeX\n")
    func_name, args, expr = match.groups()
    args = [a.strip() for a in args.split(',') if a.strip()]
    return func_name, args, expr

def read_file(input_file):
    with open(input_file, 'r') as f:
        return f.read()
    raise ValueError("Unable to open input file.\n")

def get_latex_function_patterns(latex_content):
    #pattern = r'\\newcommand\{\\([a-zA-Z]+)\}\[(\d+)\]\{(.*?)\}'
    pattern = r'\\?([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*=\s*(.*?)\s*\\\]'
    return re.findall(pattern, latex_content, re.DOTALL)

def transpile_latex_to_python(input_file, output_file):

    latex_content = read_file(input_file)
    functions = get_latex_function_patterns(latex_content)

    with open(output_file, 'w') as f:
        # Write Python math libraries
        f.write("# Auto-generated Python functions from LaTeX\n")
        f.write("import math\n")
        f.write("import numpy as np\n\n")

        count = 0
        for func_name, num_args, body in functions:
            print(f"Transpiling {body}\n")
            # Clean up the body: remove \ and replace LaTeX math with Python
            body = body.replace('\\', 'math.')
            body = body.replace('^', '**')
            body = body.replace('{', '(').replace('}', ')')
            body = body.replace('\n', ' ').strip()

            # Generate Python function
            #args = ', '.join([f'x{i+1}' for i in range(int(num_args))])
            #f.write(f"def {func_name}({args}):\n")
            #f.write(f"    return {body}\n\n")
            f.write(generate_python_function(func_name, num_args, body))
            count += 1

        # Write final comment with count
        f.write(f"# Transpiled {count} functions from LaTeX\n")

    print(f"Transpiled {count} functions to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py input.latex output.py")
        sys.exit(1)
    get_input_type(sys.argv[1])
    transpile_latex_to_python(sys.argv[1], sys.argv[2])
