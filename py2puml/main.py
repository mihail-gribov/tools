import argparse
from uml_generator import UMLGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate UML from Python source code.')
    parser.add_argument('directory_path', type=str, help='Path to the directory containing Python source files.')
    parser.add_argument('output_file_path', type=str, help='Path to the output file where UML will be saved.')

    args = parser.parse_args()

    uml_generator = UMLGenerator(args.directory_path)
    uml_output = uml_generator.generate_uml()

    with open(args.output_file_path, 'w') as file:
        file.write(uml_output)

    print(f"PlantUML code has been saved to {args.output_file_path}")
