import os
import re


def rename_action(args: any):
    print('--------------------')
    print(os.path.abspath(args.root) + ' :')
    print('--------------------')
    pathlist = []
    listup(args, pathlist)
    if args.tree:
        print('--------------------')
    if pathlist:
        filename_list = make_filename(args, pathlist)
        preview(filename_list)
        print('--------------------')
        if args.confirm or args.confirm_all or args.force:
            rename(args, filename_list)


def listup(args: any, pathlist, dir='.', index=1):
    path_list = []
    if args.path_list:
        path_list = args.path_list
    else:
        path_list = os.listdir(dir)

    if args.tree:
        print(dir.rjust(len(dir)+index-1) + os.path.sep)
        for path in path_list:
            if os.path.isfile(path):
                print(path.rjust(len(path)+index))

    if not (args.oldstr or args.search) and not (args.newstr or args.replace):
        return
    
    for path in path_list:
        d = os.path.relpath(os.path.join(dir, path))
        target = ''
        if args.extension:
            _, target = os.path.splitext(path)
        elif args.filename:
            target, _ = os.path.splitext(path)
        else:
            target = path

        if args.recursive and os.path.isdir(path):
            listup(args, pathlist, dir=d, index=index+1)
        if args.directory and not os.path.isdir(path):
            continue
        if args.file and not os.path.isfile(path):
            continue
        if args.match and not re.search(re.compile(args.match), path):
            continue
        if args.search and not args.search in target:
            continue
        elif args.oldstr and not args.oldstr in target:
            continue
        pathlist.append(d)


def make_filename(args, pathlist):
    filename_list = []
    for path in pathlist:
        filename = ext = target = newname = ''
        if args.extension:
            filename, target = os.path.splitext(path)
        elif args.filename:
            target, ext = os.path.splitext(path)
        else:
            target = path

        oldstr = newstr = ''
        if args.search:
            oldstr = args.search
        elif args.oldstr:
            oldstr = args.oldstr

        if args.replace:
            newstr = args.replace
        elif args.newstr:
            newstr = args.newstr

        if args.search or args.oldstr:
            newname = replace_content(target, oldstr, newstr)
        if args.expression:
            newname = substitute(target, args.expression, newstr)
        if args.upper:
            newname = upper_case(target)
        if args.lower:
            newname = lower_case(target)
        
        if args.extension:
            filename_list.append((path, filename + newname))
        elif args.filename:
            filename_list.append((path, newname + ext))
        else:
            filename_list.append((path, newname))
    return filename_list


def replace_content(path, oldstr, newstr):
    if oldstr and oldstr in path:
        return path.replace(oldstr, newstr)
    return path

def substitute(path, pattern, newstr):
    if not pattern:
        return path
    return re.sub(pattern, newstr, path)

def lower_case(path):
    return path.lower()

def upper_case(path):
    return path.upper()

def preview(filename_list):
    print('Preview:\n  Will be rename to ...\n')
    padding = 40
    for old, new in filename_list:
        if len(old) < padding:
            print(old.ljust(padding),'=>', new)
        else:
            print(old)
            print(' '.ljust(padding), '=>', new)

def rename(args, filename_list):
    print('Rename:\n  Rename to ...\n')
    confirm_all = False
    if args.confirm_all:
        confirm_all = input('Rename all ? [y/n] ').lower() == 'y'
        if not confirm_all:
            print('  There were no changes!')
            return
    elif args.force:
        confirm_all = True
    for old, new in filename_list:
        confirm = False
        if args.confirm:
            confirm = input(f'Rename "{old}" to "{new}" ? [y/n] ').lower() == 'y'
        if confirm or confirm_all:
            print(f'  {old} => {new}')
            os.rename(old, new)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("oldstr", default='', nargs='?', help="Old string; This value override from -c or -e")
    parser.add_argument("newstr", default='', nargs='?', help="New String; This value override from -r")

    group_global = parser.add_argument_group("global arguments")
    group_global.add_argument('-t', '--tree', action="store_true", help='Show target directory tree')

    group_confirm_options = parser.add_argument_group("confirm arguments")
    group_confirm_options.add_argument('-c', '--confirm', action='store_true', help='Confirm every time before rename. Enter y or n')
    group_confirm_options.add_argument('-C', '--confirm-all', action='store_true', help='Confirm before rename. Enter y or n')
    group_confirm_options.add_argument('-F', '--force', action='store_true', help='Force to rename')

    group_dir_options = parser.add_argument_group("directory arguments")
    group_dir_options.add_argument('-rt', '--root', default='./', metavar='<Directory>', help='Target directory of files to rename')
    group_dir_options.add_argument('-R', '--recursive', action='store_true', help='Recursive into sub directories')

    group_replace_options = parser.add_argument_group("replace arguments")
    group_replace_options.add_argument('-d', '--directory', action='store_true', help='Apply only to directory')
    group_replace_options.add_argument('-f', '--file', action='store_true', help='Apply only to files')
    group_replace_options.add_argument('-m', '--match', metavar='<Regex pattern>', help='Apply only to file that match pattern. Must be enclosed in double quotation when using symbols')
    group_replace_options.add_argument('-s', '--search', metavar='<Search string>', help='This string will be replace with Replace string.')
    group_replace_options.add_argument('-e', '--expression', metavar='<Regex pattern>', help='Regular expression pattern; Must be enclosed in double quotation when using symbols')
    group_replace_options.add_argument('-r', '--replace', default='', metavar='<Replace string>', help='Search string replace to this string')
    group_replace_options.add_argument('-ex', '--extension', action='store_true', help='Apply only to file extensions')
    group_replace_options.add_argument('-fn', '--filename', action='store_true', help='Apply only to file name')

    group_text_style = parser.add_argument_group("text-style arguments")
    group_text_style.add_argument('-l', '--lower', action='store_true', help='Transform path string to lower case')
    group_text_style.add_argument('-u', '--upper', action='store_true', help='Transform path string to upper case')

    parser.add_argument('path_list', nargs='*', metavar='<File path>', help='File list')

    args = parser.parse_args()

    os.chdir(args.root)
    try:
        rename_action(args)
    except KeyboardInterrupt:
        print('\n\nKeyboard Interrupt! (Ctrl + C)\n')