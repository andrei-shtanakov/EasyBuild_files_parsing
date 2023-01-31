import argparse
import os
from pyparsing import Word, alphas, ZeroOrMore, Suppress, Optional, nums, Literal, restOfLine

parser = argparse.ArgumentParser()


set_builddependencies = set()
set_dependencies = set()


#module_comment = Optional(("#") + Word(alphas + "-" + "_" + nums + "." + "/" + " " + "(" + ")" + "[" + "]" + "{" + "}" + ":" + "," + "'" + '"' + "=" + "+" + "-" + "*" + "/" + "%" + "&" + "|" + "^" + "~" + "<" + ">" + "!" + "?" + "@" + "#" + "$" + "`" + ";" ))
module_comment = Optional(Literal("#") + restOfLine)
module_name = Suppress("('") + Word(alphas + "-" + "_" + nums + "+" + "." + "/") + Suppress("'")
module_version = Suppress("'") + Optional("%") + Word(alphas + nums + "." + "-" + "_" + "%" + "(" + ")") + Suppress("'")
module_eb_version = Suppress("version") + Suppress("=") + Suppress("'") + Word(alphas + nums + "." + "-" + "_" + "%") + Suppress("'")
# versionsuffix = '-Python-%(pyver)s'
# ('matplotlib', '2.1.2', versionsuffix),
module_eb_versionsuffix = Suppress("versionsuffix") + Suppress("=") + Suppress("'") + Word(alphas + nums + "%" + "." + "-" + "_" + "(" + "%" + ")") + Suppress("'")
module_local_version = Word(alphas + nums + "." + "-" + "_" + "+" + "~")
module_ext = Optional(Suppress(",") + module_version)
module_true = Optional(Suppress(",") + Suppress("True"))
#    ('Eigen', '3.3.4', '', SYSTEM)
module_SYSTEM = Optional(Suppress(",") + Suppress("SYSTEM")) 

mod = (module_name + Suppress(",") + module_version + module_ext + module_SYSTEM + module_true)
mod_local = (module_name + Suppress(",") + module_local_version + module_ext + module_SYSTEM + module_true)
mod_versionsuffix = (module_name + Suppress(",") + module_version + module_eb_version + module_eb_versionsuffix + module_ext + module_SYSTEM + module_true)
mod_version_version = (module_name + Suppress(",") + module_eb_version + module_eb_versionsuffix + module_ext + module_SYSTEM + module_true)
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
                with open(filename, 'r') as file:
                    contents = file.read()
                    vesion = ""
                    versionsuffix = ""
                    lines = contents.split('\n')
                    for line in lines:
                        first = line.split(' ')
                        if first[0] == 'version':
                            line = line.replace('"', "'")
                            try:
                                version = module_version.parseString(line)[0]
                            except:
                                version = "ERROR"
                        elif first[0] == 'versionsuffix':
                            line = line.replace('"', "'")
                            try:
                                versionsuffix = module_eb_versionsuffix.parseString(line)[0]
                            except:
                                versionsuffix = "ERROR"
                        elif first[0] == 'builddependencies':
                            convert_string = ""
                            if (len(first) > 3):
                                try:
                                    for s in module_builddependencies.parseString(line).asList():
                                        convert_string += s + "-"
                                    set_builddependencies.add(convert_string[:-1])
                                except:
                                    set_builddependencies.add("ERRPR")
                            else:
                                builddependencies = True
                        elif first[0] == 'dependencies':
                            convert_string = ""
                            if (len(first) > 3):
                                try:
                                    for s in module_dependencies.parseString(line).asList():
                                        convert_string += s + "-"
                                    set_dependencies.add(convert_string[:-1])
                                except:
                                    set_dependencies.add("ERROR")
                            else:
                                dependencies = True
                        if first[0] == ']' and builddependencies:
                            builddependencies = False
                        elif first[0] == ']' and dependencies:
                            dependencies = False
                        if first[0] == '}' and builddependencies:
                            builddependencies = False
                        elif first[0] == '}' and dependencies:
                            dependencies = False
                        if builddependencies:
                            if first[0] != 'builddependencies':
                                convert_string = ""
                                comment = module_comment.parseString(line)
                                if comment:
                                    continue
                                else:
                                    try:
                                        for s in mod.parseString(line).asList():
                                            convert_string += s + "-"
                                        set_builddependencies.add(convert_string[:-1])
                                    except:
                                        try:
                                            for s in mod_local.parseString(line).asList():
                                                convert_string += s + "-"
                                            set_builddependencies.add(convert_string[:-1])
                                        except:
                                            try:
                                                for s in mod_versionsuffix.parseString(line).asList():
                                                    convert_string += s + "-"
                                                set_builddependencies.add(convert_string[:-1])
                                            except:
                                                pass
                        elif dependencies:
                            if first[0] != 'dependencies':
                                convert_string = ""
                                comment = module_comment.parseString(line)
                                if comment:
                                    continue
                                else:
                                    try:
                                        for s in mod.parseString(line).asList():
                                            convert_string += s + "-"
                                        set_dependencies.add(convert_string[:-1])
                                    except:
                                        try:
                                            for s in mod_local.parseString(line).asList():
                                                convert_string += s + "-"
                                            set_dependencies.add(convert_string[:-1])
                                        except:
                                            try:
                                                for s in mod_versionsuffix.parseString(line).asList():
                                                    convert_string += s + "-"
                                                set_dependencies.add(convert_string[:-1])
                                            except:
                                                set_dependencies.add("ERROR")
    return set_builddependencies, set_dependencies

set_builddependencies, set_dependencies =   get_list_of_dependencies(search_dir)




#print ("Build dependencies:")
#print(set_builddependencies)
#print ("Dependencies:")
#print(set_dependencies)

new_builddependencies = set_builddependencies.difference(set_dependencies)
new_dependencies = set_dependencies.difference(set_builddependencies)
print ("Build dependencies without dependencies:")
new_list = list(new_builddependencies)
new_list.sort()
print(new_list)
print(len(new_builddependencies))
#print ("Dependencies without build dependencies:")
#print(new_dependencies)


