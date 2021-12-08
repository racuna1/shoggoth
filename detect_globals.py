from pycparser import parse_file, c_ast
from pycparser.c_ast import *
import sys

sys.path.extend(['.', '..'])

class DeclVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.current_parent = None
        self.foundGlobal = False

    def generic_visit(self, node):
        """
            Here we override the generic visit node of the AST to
            include a link to the parent node. This will allow us
            to determine whether a declaration's parent is a FileAST,
            which in a sense represents global scope. If it is, we
            know it's a global variable.
        """
        oldparent = self.current_parent
        self.current_parent = node
        for c in node:
            self.visit(c)
        self.current_parent = oldparent

        name = node.__class__.__name__
        parent = self.current_parent.__class__.__name__

    def visit_Decl(self, node):
        disallowed = ["ArrayDecl", "TypeDecl"]
        node_type = node.type.__class__.__name__
        p_node_type = self.current_parent.__class__.__name__
        # print("%s (%s) parent is %s" % (node_type, node.name, p_node_type))
        if(node_type in disallowed and node.name != "_Value" and p_node_type == "FileAST"):
            self.foundGlobal = True


def detect_globals(filename):
    ast = parse_file(filename, use_cpp=True,
                     cpp_path='gcc',
                     cpp_args=['-E', r'-I/autograder/pycparser/utils/fake_libc_include'])

    dv = DeclVisitor()
    dv.visit(ast)
    return dv.foundGlobal

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(detect_globals(filename))
    else:
        print("No filename specified")