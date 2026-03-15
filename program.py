import re
import sys

def transpile_latex_to_python(input_file, output_file):
    with open(input_file, 'r') as f:
        latex_content = f.read()

    # Find all \newcommand{\func}[n]{...} patterns
    pattern = r'\\newcommand\{\\([a-zA-Z]+)\}\[(\d+)\]\{(.*?)\}'
    functions = re.findall(pattern, latex_content, re.DOTALL)

    with open(output_file, 'w') as f:
        # Write Python math libraries
        f.write("# Auto-generated Python functions from LaTeX\n")
        f.write("import math\n")
        f.write("import numpy as np\n\n")

        count = 0
        for func_name, num_args, body in functions:
            # Clean up the body: remove \ and replace LaTeX math with Python
            body = body.replace('\\', '')
            body = body.replace('^', '**')
            body = body.replace('{', '(').replace('}', ')')
            body = body.replace('\n', ' ').strip()

            # Generate Python function
            args = ', '.join([f'x{i+1}' for i in range(int(num_args))])
            f.write(f"def {func_name}({args}):\n")
            f.write(f"    return {body}\n\n")
            count += 1

        # Write final comment with count
        f.write(f"# Transpiled {count} functions from LaTeX\n")

    print(f"Transpiled {count} functions to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py input.latex output.py")
        sys.exit(1)
    transpile_latex_to_python(sys.argv[1], sys.argv[2])
