import pandas as pd
import argparse
import os



parser = argparse.ArgumentParser(
    description='Take the keys of a table and compile as many typst documents as there are rows. \
        These key=value are made available to the compiler as sys.inputs. \
        See [sys.inputs](https://typst.app/docs/reference/foundations/sys).\
        For each rows of a table, compile a typst document with an collumns keys  arguments.'
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
    '-k',
    '--keyname',
    help="Column by which each file fill take it's name.",
    default=""
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true'
)

parser.add_argument(
    '-e',
    '--extention',
    help="Type of compiled file. Typically pdf or svg.",
    default='.pdf',
    choices=['.pdf', '.svg']
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

def create_directory(output_dir:str):
    try:
        os.mkdir(output_dir)
        print(f"Directory '{output_dir}' created successfully.")
    except FileExistsError:
        print(f"Directory '{output_dir}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{output_dir}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    
    df = load_file(args.table_file)
    df.dropna(how='all', inplace=True)
    df = df.to_dict(orient='records')

    file_name_key = args.keyname
    is_verbose = args.verbose
    typst_file = args.typst_file
    extention = args.extention
    output_dir = output_dir_format(args.output)

    create_directory(output_dir)

    for enum, dict_line in enumerate(df):

        name = ""
        try:
            name = dict_line[file_name_key]
        except KeyError:
            name = os.path.splitext(os.path.basename(typst_file))[0]

        output_file = output_dir + name + "_" + str(enum) + extention

        compile_line = typst_compile_line(dict_line.keys(), dict_line.values(), typst_file, output_file)

        if not is_verbose:
            print(compile_line)

        os.system(compile_line)

if __name__ == "__main__":

    main()
