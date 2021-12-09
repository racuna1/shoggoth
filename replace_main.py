__author__ = "Oluwamayowa Esan"

#------------------#
#                  #
#    javascript    #  <- do not allow out of
#                  #     the box
#------------------#

import re
import sys
import os
import json

# Here's the AST approach. The problem with this is that it utilizes fake headers 
# (see https://eli.thegreenplace.net/2015/on-parsing-c-type-declarations-and-fake-headers/)
# This isn't a problem going from C code to an AST. The problem arises when translating back 
# to C code. pycparser includes all of the fake headers it used to generate the AST. This 
# leads to redefined variables in the C code and causes compilation to fail. The alternative 
# approach is to do a simple regex search on each file within the submission, which is what I did.
# I'm keeping it around in case it proves useful later on.

# from pycparser import c_ast, parse_file, c_generatord
# class MainModifier(c_ast.NodeVisitor):
#     def visit_FuncDef(self, node):
#         if(node.decl.name == "main"):
#             node.decl.type.type.declname = "entry"
#             node.decl.name = "entry"
#             print(node.decl.coord)

# def save_new_ast(ast, filepath):
#     generator = c_generator.CGenerator()
#     c_code = generator.visit(ast)
#     with open(filepath, 'wt') as f:
#         f.write(c_code)


# def rename_ast_main(filepath):
#     ast = parse_file(filename,
#                      use_cpp=True,
#                      cpp_path='gcc',
#                      cpp_args=r'-Iutils/fake_libc_include')
#     mm = MainModifier()
#     mm.visit(ast)
#     save_new_ast(ast, filepath)

# def rename_from_ast():
#     if len(sys.argv) > 1:
#         rename_ast_main(sys.argv[1])
#     else:
#         print("Please provide a path to the file containing the main function")


def search_dir(dir):
    for root, dirs, files in os.walk(dir):

        # if not files:
        #     return

        c_files = list(filter(lambda f: re.match('.*\.c$', f), files))

        for cf in c_files:
            path = '/'.join((root, cf))
            result = rename_main(path)
            if result:
                return

        # recursively search
        for path in dirs:
            search_dir(root + path)


def rename_main(filename):
    print(filename)
    with open(filename, 'r') as file:
        file_data = file.read()

    regex = 'int (main)\((?P<args>.*)\)'
    match = re.search(regex, file_data)

    if not match:
        print("main not found")
        return False

    file_data = re.sub(regex, 'int submission_main(%s)' %
                           match.group("args"), file_data)

    with open(filename, 'w') as file:
        file.write(file_data)
    return True


if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)
        
    search_dir(config["submission_location"])
