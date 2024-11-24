import pandas as pd
import argparse
import os



parser = argparse.ArgumentParser(
    description='For each line of a xlsx file, compile a typst document with collumns as keys an collumns  arguments.'
)

parser.add_argument(
    "typst_file",
    help="The typst (.typ) file to compile"
)

parser.add_argument(
    "table_file",
    help="The table file to read. Can be a .csv, .xlsx, .xls, .json, .html or .parquet file."
)

parser.add_argument(
    "-o",
    "--output",
    help="Output folder.",
    default="~/Desktop/new/"
)

parser.add_argument(
    '-n',
    '--name',
    help="Column by which each file fill take it's name."
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true'
)

args = parser.parse_args()


def output_dir_format(output_dir:str):
    if output_dir[-1] != '/':
        output_dir += '/'
    return output_dir

def escape_char(value: str) -> str:
    # Escape characters for Python
    value = value.replace("\\", "\\\\").replace("'", "\\'").replace("\"", "\\\"")
    
    # Escape characters for Bash
    value = value.replace("$", "\\$").replace("`", "\\`").replace("!", "\\!")
    
    return value

def typ_arg_input(key, value) -> str:
    key = escape_char(key)
    value = escape_char(str(value))
    return '--input ' + '\"' + key + '\"' + '=' + '\"' + str(value) + '\"'

def typst_compile_line(keys:list[str], values:list[str], typst_file: str, output_file:str|None) -> str:
    output_file = '\"' + escape_char(output_file) + '\"'
    typst_file = '\"' + escape_char(typst_file) + '\"'
    command = 'typst compile'
    arg_inputs_list = [typ_arg_input(key, value) for key, value in zip(keys, values) if str(value) not in ['nan','NaN']]
    arg_inputs = ''
    for arg_input in arg_inputs_list:
        arg_inputs += arg_input + ' '
    

    return command + ' ' + arg_inputs + typst_file + ' ' + output_file


def load_file(file_path: str) -> pd.DataFrame:
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension == '.xlsx' or file_extension == '.xls':
        return pd.read_excel(file_path)
    elif file_extension == '.json':
        return pd.read_json(file_path)
    elif file_extension == '.html':
        return pd.read_html(file_path)[0]
    elif file_extension == '.parquet':
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

# Example usage
file_path = 'example.xlsx'
df = load_file(file_path)
print(df.head())

def main():
    
    df = load_file(args.xlsx_file)
    df = df.to_dict(orient='records')

    args.output = output_dir_format(args.output)
    try:
        os.mkdir(args.output)
        print(f"Nested directories '{args.output}' created successfully.")
    except FileExistsError:
        print(f"One or more directories in '{args.output}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{args.output}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


    typst_file = args.typst_file
    output_file = args.output


    list_compile = [typst_compile_line(dict_line.keys(), dict_line.values(), typst_file, output_file + str(enum) + '.pdf') for enum, dict_line in enumerate(df)]
    for line in list_compile:
        if not args.verbose:
            print(line)
        os.system(line)

if __name__ == "__main__":

    main()
