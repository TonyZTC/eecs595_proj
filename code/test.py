import ast
import astunparse
import re

f = open("./code.txt",encoding = "utf-8")
tree = ast.parse(f.read(), type_comments=False)
for node in ast.walk(tree):
    # let's work only on functions & classes definitions
    if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        continue

    if not len(node.body):
        continue

    if not isinstance(node.body[0], ast.Expr):
        continue

    if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
        continue

    # Uncomment lines below if you want print what and where we are removing
    # print(node)
    # print(node.body[0].value.s)

    node.body = node.body[1:]
# s = ast.dump(tree, annotate_fields=False, include_attributes=False)
s = astunparse.dump(tree)
# s = re.split(r'\W', s)
# s = ' '.join(s).split()
print(s)

def test():
    """
        dddddddddddddddddddddddddddddddddddddddddd
    """

    a = 0