import argparse
import os
from pyparsing import Word, alphas, ZeroOrMore, Suppress, Optional, nums, Literal, restOfLine

parser = argparse.ArgumentParser()


set_builddependencies = set()
set_dependencies = set()


#module_comment = Optional(("#") + Word(alphas + "-" + "_" + nums + "." + "/" + " " + "(" + ")" + "[" + "]" + "{" + "}" + ":" + "," + "'" + '"' + "=" + "+" + "-" + "*" + "/" + "%" + "&" + "|" + "^" + "~" + "<" + ">" + "!" + "?" + "@" + "#" + "$" + "`" + ";" ))
module_comment = Optional(Literal("#") + restOfLine)
module_name = Suppress("('") + Word(alphas + "-" + "_" + nums + "+") + Suppress("'")
module_version = Suppress("'") + Word(alphas + nums + "." + "-" + "_") + Suppress("'")
module_local_version = Word(alphas + nums + "." + "-" + "_" + "+" + "~")
module_ext = Optional(Suppress(",") + module_version)
module_true = Optional(Suppress(",") + Suppress("True"))
module_SYSTEM = Optional(Suppress(",") + Suppress("SYSTEM")) 

mod = (module_name + Suppress(",") + module_version + module_ext + module_SYSTEM + module_true)
mod_local = (module_name + Suppress(",") + module_local_version + module_ext + module_SYSTEM + module_true)
module_dependencies = Suppress("dependencies") + Suppress("=") + Suppress("[") + mod
module_builddependencies = Suppress("builddependencies") + Suppress("=") + Suppress("[") + mod

#parser.add_argument('filename', help='The name of the file to parse')
parser.add_argument('root_dir', help='The direcrory with EasyConfig files')

args = parser.parse_args()

#filename = args.filename
search_dir = args.root_dir




def get_list_of_dependencies(search_dir):
    builddependencies = False
    dependencies = False
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file[-3:] == ".eb":
                filename = os.path.join(root, file)
                print (filename)
                with open(filename, 'r') as file:
                    contents = file.read()
                    lines = contents.split('\n')
                    for line in lines:
                        first = line.split(' ')
                        if first[0] == 'builddependencies':
                            convert_string = ""
                            if (len(first) > 3):
                                for s in module_builddependencies.parseString(line).asList():
                                    convert_string += s + "-"
                                set_builddependencies.add(convert_string[:-1])
                            else:
                                builddependencies = True
                        elif first[0] == 'dependencies':
                            convert_string = ""
                            if (len(first) > 3):
                                for s in module_dependencies.parseString(line).asList():
                                    convert_string += s + "-"
                                set_dependencies.add(convert_string[:-1])
                            else:
                                dependencies = True
                        if first[0] == ']' and builddependencies:
                            builddependencies = False
                        elif first[0] == ']' and dependencies:
                            dependencies = False
                        if builddependencies:
                            if first[0] != 'builddependencies':
                                convert_string = ""
                                print (line)
                                comment = module_comment.parseString(line)
                                if comment:
                                    continue
                                else:
                                    try:
                                        for s in mod.parseString(line).asList():
                                            convert_string += s + "-"
                                        set_builddependencies.add(convert_string[:-1])
                                        print(convert_string[:-1])
                                    except:
                                        for s in mod_local.parseString(line).asList():
                                            convert_string += s + "-"
                                        set_builddependencies.add(convert_string[:-1])
                                        print(convert_string[:-1])
                        elif dependencies:
                            if first[0] != 'dependencies':
                                convert_string = ""
                                comment = module_comment.parseString(line)
                                if comment:
                                    continue
                                else:
                                    for s in mod.parseString(line).asList():
                                        convert_string += s + "-"
                                    set_dependencies.add(convert_string[:-1])
                                    print(convert_string[:-1])
    return set_builddependencies, set_dependencies

set_builddependencies, set_dependencies =   get_list_of_dependencies(search_dir)




print ("Build dependencies:")
print(set_builddependencies)
print ("Dependencies:")
print(set_dependencies)
