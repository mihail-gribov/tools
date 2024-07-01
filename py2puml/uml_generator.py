import ast
from pathlib import Path

class UMLGenerator:
    def __init__(self, directory_path):
        self.directory = Path(directory_path)
        self.uml = '@startuml\n'
        self.all_class_bases = {}

    def visibility(self, name):
        """
        Determine the visibility of a member based on its name.
        """
        if name.startswith('__') and name.endswith('__'):
            return '~', 'private'  # Magic
        if name.startswith('__'):
            return '-', 'private'  # Private
        elif name.startswith('_'):
            return '#', 'protected'  # Protected
        else:
            return '+', 'public'  # Public

    def parse_python_file(self, file_path):
        """
        Parse a Python file to extract class and function definitions, global variables, and class inheritance.
        """
        with open(file_path, "r") as file:
            node = ast.parse(file.read(), filename=file_path.name)
        classes = []
        functions = []
        class_bases = {}
        global_vars = []
        for n in node.body:
            if isinstance(n, ast.ClassDef):
                class_name, fields, attributes, static_methods, methods, abstract_method_count = self.process_class_def(n)
                total_method_count = len(static_methods) + len(methods)
                class_type = self.determine_class_type(fields, abstract_method_count, total_method_count)
                bases = [base.id for base in n.bases if isinstance(base, ast.Name)]
                class_bases[class_name] = bases
                classes.append((
                    class_name,
                    sorted(list(set(fields)), key=lambda x: x[1]),
                    sorted(list(set(attributes)), key=lambda x: x[1]),
                    sorted(list(set(static_methods)), key=lambda x: x[1]),
                    sorted(list(set(methods)), key=lambda x: x[1]),
                    class_type,
                    bases
                ))
            elif isinstance(n, ast.FunctionDef):
                functions.append(self.process_function_def(n))
            elif isinstance(n, ast.Assign):
                global_vars.extend(self.process_global_vars(n))
        return (
            classes,
            functions,
            sorted(list(set(global_vars)), key=lambda x: x[1]),
            class_bases
        )

    def extract_fields_from_init(self, init_method):
        """
        Extract fields defined in the __init__ method of a class.
        """
        fields = []
        for stmt in init_method.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                        prefix, _ = self.visibility(target.attr)
                        fields.append((prefix, target.attr))
        return fields

    def process_class_def(self, node):
        """
        Process a class definition node to extract its components.
        """
        class_name = node.name
        methods = []
        fields = []
        attributes = []
        abstract_method_count = 0
        static_methods = []
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                prefix, method_signature, is_abstract, is_static, is_class = self.process_method_def(body_item)
                if is_abstract:
                    abstract_method_count += 1
                if is_static or is_class:
                    static_methods.append((prefix, method_signature))
                else:
                    methods.append((prefix, method_signature))

                if body_item.name == '__init__':
                    fields = self.extract_fields_from_init(body_item)

            elif isinstance(body_item, ast.AnnAssign):
                attributes.extend(self.process_attributes(body_item))
        return class_name, fields, attributes, static_methods, methods, abstract_method_count

    def process_method_def(self, body_item):
        """
        Process a method definition node to extract its signature and properties.
        """
        prefix, vis_type = self.visibility(body_item.name)
        args = ', '.join(arg.arg for arg in body_item.args.args)

        method_signature = f"{body_item.name}({args})"
        is_abstract = 'decorator_list' in body_item._fields and any(isinstance(dec, ast.Name) and dec.id == 'abstractmethod' for dec in body_item.decorator_list)
        is_static = 'decorator_list' in body_item._fields and any(isinstance(dec, ast.Name) and dec.id == 'staticmethod' for dec in body_item.decorator_list)
        is_class = 'decorator_list' in body_item._fields and any(isinstance(dec, ast.Name) and dec.id == 'classmethod' for dec in body_item.decorator_list)
        if is_abstract:
            prefix = prefix + ' {abstract}'
        elif is_static:
            prefix = prefix + ' {static}'
        return prefix, method_signature, is_abstract, is_static, is_class

    def process_attributes(self, body_item):
        """
        Process attributes of a class defined using type annotations.
        """
        attributes = []
        if isinstance(body_item.target, ast.Name):
            prefix, _ = self.visibility(body_item.target.id)
            type_annotation = self.get_type_annotation(body_item.annotation) if body_item.annotation else "Any"
            attributes.append((prefix + ' {static}', f"{body_item.target.id}: {type_annotation}"))
        return attributes

    def get_type_annotation(self, annotation):
        """
        Extract a string representation of a type annotation from the AST.
        Handles common cases like Name, Subscript, and Attribute.
        """
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.slice, ast.Index):
                return f"{self.get_type_annotation(annotation.value)}[{self.get_type_annotation(annotation.slice.value)}]"
            return f"{self.get_type_annotation(annotation.value)}[{self.get_type_annotation(annotation.slice)}]"
        elif isinstance(annotation, ast.Attribute):
            return f"{self.get_type_annotation(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Tuple):
            return f"({', '.join(self.get_type_annotation(el) for el in annotation.elts)})"
        elif isinstance(annotation, ast.List):
            return f"[{', '.join(self.get_type_annotation(el) for el in annotation.elts)}]"
        else:
            raise NotImplementedError(f"Unsupported annotation type: {type(annotation).__name__}")

    def process_fields(self, body_item):
        """
        Process fields defined using simple assignments.
        """
        fields = []
        for target in body_item.targets:
            if isinstance(target, ast.Name):
                prefix, _ = self.visibility(target.id)
                fields.append((prefix, target.id))
        return fields

    def process_function_def(self, node):
        """
        Process a function definition node to extract its signature.
        """
        args = ', '.join(arg.arg for arg in node.args.args)
        return f"{node.name}({args})"

    def determine_class_type(self, has_fields, abstract_method_count, total_method_count):
        """
        Determine the type of class (interface, abstract class, or class) based on its methods and fields.
        """
        if abstract_method_count == total_method_count and total_method_count > 0 and not has_fields:
            return 'interface'
        elif abstract_method_count > 0:
            return 'abstract class'
        return 'class'

    def format_class_info(self, class_info):
        """
        Format the information of a class for UML representation.
        """
        class_name, fields, attributes, static_methods, methods, class_type, bases = class_info
        class_str = f"  {class_type} {class_name} {{\n"
        for prefix, field in fields:
            class_str += f"    {prefix} {field}\n"
        if len(fields) and len(methods):
            class_str += "    ....\n"

        for prefix, method in methods:
            class_str += f"    {prefix} {method}\n"

        if (len(fields) or len(methods)) and (len(attributes) or len(static_methods)):
            class_str += "    __Static__\n"

        for prefix, attribute in attributes:
            class_str += f"    {prefix} {attribute}\n"

        if len(attributes) and len(static_methods):
            class_str += "    ....\n"

        for prefix, method in static_methods:
            class_str += f"    {prefix} {method}\n"

        class_str += "  }\n"
        return class_str

    def add_inheritance_relations(self):
        """
        Add inheritance relationships between classes to the UML.
        """
        for class_name, bases in self.all_class_bases.items():
            for base in bases:
                self.uml += f"{base} <|-- {class_name}\n"

    def generate_uml(self):
        """
        Generate UML for all Python files in the specified directory.
        """
        pathlist = self.directory.rglob('*.py')
        for path in pathlist:
            relative_path = path.relative_to(self.directory).with_suffix('')
            package_name = str(relative_path).replace('/', '.').replace('\\', '.')  # Handle paths for both Windows and Unix
            class_infos, function_infos, global_vars, class_bases = self.parse_python_file(path)

            self.all_class_bases.update(class_bases)
            self.uml += f'package "{package_name}" <<Frame>> #F0F0FF {{\n'
            if global_vars:
                self.uml += '  class "Global Variables" << (V,#AAAAFF) >> {\n'
                for prefix, var in global_vars:
                    self.uml += f"    {prefix} {var}\n"
                self.uml += '  }\n'
            for function_signature in function_infos:
                self.uml += f'  class "{function_signature}" << (F,#DDDD00) >> {{\n  }}\n'
            for class_info in class_infos:
                self.uml += self.format_class_info(class_info)

            self.uml += '}\n'
        self.add_inheritance_relations()
        self.uml += '@enduml'
        return self.uml

    def process_global_vars(self, node):
        """
        Process global variables defined in the module.
        """
        global_vars = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                prefix, _ = self.visibility(target.id)
                global_vars.append((prefix, target.id))
        return global_vars