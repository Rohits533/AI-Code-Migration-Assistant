import ast

class MigrationEngine(ast.NodeTransformer):
    """
    Applies code migrations using AST transformation.
    """
    def __init__(self, rename_map):
        self.rename_map = rename_map

    def visit_Name(self, node):
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return self.generic_visit(node)

    def visit_arg(self, node):
        if node.arg in self.rename_map:
            node.arg = self.rename_map[node.arg]
        return self.generic_visit(node)

def apply_migration(code, rename_map):
    """
    Parses code, applies transformations, and returns the new code.
    """
    try:
        tree = ast.parse(code)
        transformer = MigrationEngine(rename_map)
        new_tree = transformer.visit(tree)
        ast.fix_missing_locations(new_tree)
        return ast.unparse(new_tree)
    except SyntaxError as e:
        return f"❌ Syntax Error: {e}"
