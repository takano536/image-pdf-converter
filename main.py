import argparse
import glob
import os
import sys
import itertools
import functools
import re
import img2pdf
from PIL import Image


def pause():
    print('\nPress enter key to quit...', end='')
    input()
    sys.exit(1)


class ParserHelpOnError(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.stderr.write('\nerror: %s\n' % message)
        pause()


parser = ParserHelpOnError(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    'input',
    nargs='*',
    help='input file or directory'
)
parser.add_argument(
    '-o', '--output_filename',
    help='output pdf filename'
)
parser.add_argument(
    '--output_folder',
    help='save the output in a certain folder'
)
parser.add_argument(
    '-e', '--exclude',
    nargs='*',
    help='exclude file, directory or extension \n'
    'selecting an extension, prefix it with dot at the beginning'
)
parser.add_argument(
    '--sort',
    choices=['folder', 'file', 'date', 'ext', 'file-desc', 'folder-desc', 'date-desc', 'ext-desc'],
    default='folder',
    help='how to sort files (default=folder)'
)
parser.add_argument(
    '-r', '--recursive',
    action='store_true',
    help='recursively get input files'
)
args = parser.parse_args()
if args.exclude is None:
    args.exclude = []
if len(args.input) == 0:
    parser.error('the following arguments are required: input')


FULL_WIDTH = ''.join(chr(0xff01 + i) for i in range(94))
HALF_WIDTH = ''.join(chr(0x21 + i) for i in range(94))
FULL2HALF = str.maketrans(FULL_WIDTH, HALF_WIDTH)
SYMBOL_REGEX = '[\\u3000 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
INVALID_CHAR_REGEX = '[\\/:*?"<>|]'


def is_image(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True


def natural_sort_cmp(a_str: str, b_str: str, ext_cmp: bool):
    def divide(string: str):
        substr = list()
        string = string.translate(FULL2HALF)
        string = [s.replace(os.sep, '/') for s in string]
        groups = itertools.groupby(string, lambda char: 1 if char.isdigit() else -1 if re.match(SYMBOL_REGEX, char) else 0)
        for _, group in groups:
            substr.append(''.join(group))
        return substr

    if ext_cmp and os.path.splitext(a_str)[1] != os.path.splitext(b_str)[1]:
        return 1 if os.path.splitext(a_str)[1] > os.path.splitext(b_str)[1] else -1

    a_dir_str, b_dir_str = divide(os.path.split(a_str)[0]), divide(os.path.split(b_str)[0])
    if len(a_dir_str) != len(b_dir_str):
        return 1 if len(a_str) > len(b_str) else -1

    a_str, b_str = divide(a_str), divide(b_str)
    rep_cnt = 0
    for (a_substr, b_substr) in zip(a_str, b_str):
        a_swap, b_swap = False, False
        if re.match(SYMBOL_REGEX, a_substr) and a_str[rep_cnt + 1].isdigit():
            a_str[rep_cnt], a_str[rep_cnt + 1] = a_str[rep_cnt + 1], a_str[rep_cnt]
            a_substr = a_str[rep_cnt]
            a_swap = True
        if re.match(SYMBOL_REGEX, b_substr) and b_str[rep_cnt + 1].isdigit():
            b_str[rep_cnt], b_str[rep_cnt + 1] = b_str[rep_cnt + 1], b_str[rep_cnt]
            b_substr = b_str[rep_cnt]
            b_swap = True

        if a_substr.isdigit() and b_substr.isdigit():
            a_substr = float(a_substr) - len(a_substr) * 0.1
            b_substr = float(b_substr) - len(b_substr) * 0.1

        if a_substr != b_substr:
            return 1 if a_substr > b_substr else -1

        if a_swap != b_swap:
            return 1 if b_swap else -1

        rep_cnt += 1

    if len(a_str) == len(b_str):
        return 0
    else:
        return 1 if len(a_str) > len(b_str) else -1


def input_filepaths(inputs: list, exc: list, is_recursive: bool):
    exc_ext, exc_file, exc_folder = list(), list(), list()
    for arg in exc:
        arg = arg.replace('/', os.sep)
        if arg[0] == '.':
            exc_ext.append(arg.lower())
        elif os.path.isfile(arg):
            exc_file.append(os.path.abspath(arg))
        elif os.path.isdir(arg):
            exc_folder.append(os.path.abspath(arg))

    filepaths = list()
    folders = list()
    for arg in inputs:
        arg = arg.replace('/', os.sep)
        arg = os.path.abspath(arg)
        if not os.path.exists(arg):
            continue
        if os.path.splitext(arg)[1].lower() in exc_ext:
            continue
        if arg in exc_file or arg in exc_folder:
            continue
        elif os.path.isfile(arg):
            filepaths.append(arg)
        elif os.path.isdir(arg):
            folders.append(arg)

    for folder in folders:
        for arg in glob.glob(folder + '/**/*.*' if is_recursive else folder + '/*.*', recursive=is_recursive):
            arg = arg.replace('/', os.sep)
            if not os.path.exists(arg):
                continue
            if not os.path.exists(arg):
                continue
            if os.path.splitext(arg)[1].lower() in exc_ext:
                continue
            if arg in exc_file:
                continue
            if not is_image(arg):
                continue
            if os.path.split(arg)[0] in exc_folder:
                continue
            elif os.path.isfile(arg):
                filepaths.append(arg)

    for i in range(len(filepaths)):
        filepaths[i] = os.path.abspath(filepaths[i])
    return filepaths


def sort_files(filepaths: list, method: str):
    def filename_sort(a, b):
        return natural_sort_cmp(os.path.basename(a), os.path.basename(b), False)

    def foldername_sort(a, b):
        return natural_sort_cmp(a, b, False)

    def ext_sort(a, b):
        return natural_sort_cmp(a, b, True)

    if method == 'folder-desc':
        filepaths.sort(key=functools.cmp_to_key(foldername_sort), reverse=True)
    elif method == 'file':
        filepaths.sort(key=functools.cmp_to_key(filename_sort))
    elif method == 'file-desc':
        filepaths.sort(key=functools.cmp_to_key(filename_sort), reverse=True)
    elif method == 'date' and os.name == 'nt':
        filepaths.sort(key=lambda file_path: os.path.getctime(file_path))
    elif method == 'date-desc' and os.name == 'nt':
        filepaths.sort(key=lambda file_path: os.path.getctime(file_path), reverse=True)
    elif method == 'ext':
        filepaths.sort(key=functools.cmp_to_key(ext_sort))
    elif method == 'ext-desc':
        filepaths.sort(key=functools.cmp_to_key(ext_sort), reverse=True)
    else:
        filepaths.sort(key=functools.cmp_to_key(foldername_sort))
    return filepaths


def duplicate_rename(filepath: str):
    if not os.path.exists(filepath):
        return filepath

    file_cnt = 1
    while 1:
        filepath_without_ext, file_ext = os.path.splitext(filepath)
        filepath_without_ext += ' (' + str(file_cnt) + ')'
        if not os.path.exists(filepath_without_ext + file_ext):
            break
        file_cnt += 1
    return filepath_without_ext + file_ext


def preview(filepaths: list, output_filepath: str):
    should_proceed = True
    filenames = [os.path.split(filepath)[-1] for filepath in filepaths]
    pre_dirpath = str()
    print_format = "{:" + str(len(str(len(filepaths)))) + "d}"
    for filename, filepath, cnt in zip(filenames, filepaths, range(1, len(filepaths) + 1)):
        dirpath = os.path.split(filepath)[0]
        if not dirpath == pre_dirpath:
            print('\n' + dirpath)
        pre_dirpath = dirpath

        if not is_image(filepath):
            print('page', print_format.format(cnt), ':', filename, '   Error: It is not an image file')
            should_proceed = False
        else:
            print('page', print_format.format(cnt), ':', filename)
    print('output folder ->', os.path.split(output_filepath)[0])
    if re.search(INVALID_CHAR_REGEX, os.path.split(output_filepath)[-1]):
        print('output name ->', os.path.split(output_filepath)[-1], '   Error: Contains invalid characters')
        should_proceed = False
    else:
        print('output name ->', os.path.split(output_filepath)[-1])

    return should_proceed


def convert_image_into_pdf(filepaths: list, output_filepath: str):
    with open(output_filepath, "wb") as f:
        try:
            f.write(img2pdf.convert([Image.open(file_path).filename for file_path in filepaths if is_image(file_path)]))
        except Exception as error:
            print(error)
            print("Error: An unexpected error has occurred...")
            return -1
    return 0


def main():
    filepaths = input_filepaths(args.input, args.exclude, args.recursive)
    if len(filepaths) == 0:
        print('There are no files to read...')
        return
    sorted_filepaths = sort_files(filepaths, args.sort)

    if args.output_filename is None:
        output_filename = os.path.splitext(os.path.basename(sorted_filepaths[0]))[0] + '.pdf'
    else:
        output_filename = args.output_filename if os.path.splitext(args.output_filename)[1].lower() == '.pdf' else args.output_filename + '.pdf'
    if args.output_folder is None:
        output_folder = os.path.dirname(filepaths[0])
    else:
        output_folder = args.output_folder
    output_filepath = duplicate_rename(os.path.join(output_folder, output_filename))

    should_proceed = preview(sorted_filepaths, output_filepath)
    if not should_proceed:
        print('Interrupted...')
        return

    print('\nProceed ([y]/n)? ', end='')
    ans = input()
    should_proceed = True if len(ans) != 0 and ans[0].lower() == 'y' else False
    if not should_proceed:
        return

    ret = convert_image_into_pdf(sorted_filepaths, output_filepath)
    if ret == 0:
        print('PDF has been created successfully')
    else:
        print('Failed to create PDF')


if __name__ == '__main__':
    main()
    pause()
