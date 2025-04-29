import re
import os
import argparse
import sys


def generate_go_variable_name(lua_filename):
    """Generates an exported Go-style variable name (CamelCase) from a Lua filename."""
    base_name = os.path.basename(lua_filename)
    name_without_ext, _ = os.path.splitext(base_name)
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name_without_ext).strip("_")
    if not s:
        return "DefaultVarName"
    parts = s.split("_")
    camel_case_name = "".join(part.capitalize() for part in parts if part)
    if not camel_case_name:
        return "DefaultVarName"
    if not camel_case_name[0].isalpha():
        camel_case_name = "Var" + camel_case_name
    return camel_case_name


def convert_lua_to_go_map(lua_content, go_var_name):
    """Converts a Lua table string (specific format) to a Go map string."""
    outer_pattern = re.compile(r'\["([^"]+)"\]\s*=\s*\{([^}]+)\}')
    icon_pattern = re.compile(r'icon\s*=\s*"([^"]+)"')
    color_pattern = re.compile(r'color\s*=\s*"([^"]+)"')
    go_map_entries = []

    for match in outer_pattern.finditer(lua_content):
        lua_key = match.group(1)
        inner_content = match.group(2)
        icon_match = icon_pattern.search(inner_content)
        color_match = color_pattern.search(inner_content)
        if icon_match and color_match:
            icon = icon_match.group(1)
            color = color_match.group(1)
            go_map_entries.append(
                f'\t"{lua_key}": {{Icon: "{icon}", Color: "{color}"}},'
            )
        else:
            print(
                f"Warning: Could not find icon/color for key '{lua_key}' in source. Skipping.",
                file=sys.stderr,
            )

    if not go_map_entries:
        return None

    go_code = "package icons\n\n"
    go_code += "// Automatically generated from Lua source:\n"
    go_code += "// https://github.com/nvim-tree/nvim-web-devicons\n\n"
    go_code += f"var {go_var_name} = map[string]Style{{\n"
    go_code += "\n".join(go_map_entries)
    go_code += "\n}"
    return go_code


def process_single_file(lua_file_path, output_dir_or_file, custom_go_var_name=None):
    """Processes a single Lua file and writes the corresponding Go file."""
    print(f"Processing '{lua_file_path}'...")

    go_var_name = custom_go_var_name
    if not go_var_name:
        go_var_name = generate_go_variable_name(lua_file_path)
    elif not go_var_name[0].isupper():
        print(
            f"Warning: Provided variable name '{go_var_name}' for '{lua_file_path}' does not start uppercase. It won't be exported.",
            file=sys.stderr,
        )

    lua_base_name = os.path.basename(lua_file_path)
    default_go_filename = os.path.splitext(lua_base_name)[0] + ".go"
    default_go_filename = re.sub(r"[^a-zA-Z0-9_.]+", "_", default_go_filename).strip(
        "_"
    )
    if not default_go_filename:
        default_go_filename = "generated_icons.go"

    output_dir = "."
    go_file_path = default_go_filename

    if output_dir_or_file:
        output_spec = os.path.normpath(output_dir_or_file)
        if os.path.isdir(output_spec) or output_spec.endswith(os.path.sep):
            output_dir = output_spec
            go_file_path = os.path.join(output_dir, default_go_filename)
        else:
            output_dir = os.path.dirname(output_spec)
            go_file_path = output_spec
            if not output_dir:
                output_dir = "."

    try:
        with open(lua_file_path, "r", encoding="utf-8") as f:
            lua_content = f.read()

        is_return_structure = lua_content.strip().startswith("return {")
        content_to_parse = lua_content
        if is_return_structure:
            content_match = re.search(r"return\s*\{(.*)\}", lua_content, re.DOTALL)
            if content_match:
                content_to_parse = content_match.group(1)
        else:
            print(
                f"Warning: Input file '{lua_file_path}' doesn't start with 'return {{'. Parsing content directly.",
                file=sys.stderr,
            )

        go_code = convert_lua_to_go_map(content_to_parse, go_var_name)

        if go_code:
            if output_dir and output_dir != ".":
                os.makedirs(output_dir, exist_ok=True)

            with open(go_file_path, "w", encoding="utf-8") as f:
                f.write(go_code)
            print(
                f"  -> Successfully converted to '{go_file_path}' (variable: {go_var_name})"
            )
        else:
            print(
                f"  -> Error: No valid entries extracted from '{lua_file_path}'. No Go file generated.",
                file=sys.stderr,
            )

    except FileNotFoundError:
        print(f"Error: Input Lua file not found: '{lua_file_path}'", file=sys.stderr)
    except Exception as e:
        print(
            f"An unexpected error occurred while processing '{lua_file_path}': {e}",
            file=sys.stderr,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Convert nvim-web-devicons Lua table file(s) to Go map definitions."
    )
    parser.add_argument(
        "input_path",
        help="Path to the input Lua file or a directory containing .lua files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output file or directory. If input is a directory, this MUST be a directory.",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Explicit Go exported variable name (CamelCase). Only applicable if input_path is a single file.",
    )
    args = parser.parse_args()

    input_path = args.input_path
    output_spec = args.output
    custom_name = args.name

    if os.path.isdir(input_path):
        print(f"Input is a directory: '{input_path}'")
        if custom_name:
            print(
                "Warning: -n/--name argument is ignored when input is a directory.",
                file=sys.stderr,
            )

        output_base_dir = "."
        if output_spec:
            norm_output = os.path.normpath(output_spec)
            if os.path.exists(norm_output) and not os.path.isdir(norm_output):
                print(
                    f"Error: Output path '{output_spec}' exists but is not a directory. Cannot output multiple files.",
                    file=sys.stderr,
                )
                sys.exit(1)
            output_base_dir = norm_output

        count = 0
        for filename in os.listdir(input_path):
            if filename.endswith(".lua"):
                file_path = os.path.join(input_path, filename)
                if os.path.isfile(file_path):
                    process_single_file(file_path, output_base_dir)
                    count += 1
        if count == 0:
            print("No .lua files found in the input directory.")
        else:
            print(f"Finished processing {count} .lua file(s).")

    elif os.path.isfile(input_path):
        process_single_file(input_path, output_spec, custom_name)
    else:
        print(
            f"Error: Input path '{input_path}' not found or is not a valid file/directory.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
