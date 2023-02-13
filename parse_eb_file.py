import re

with open("result.txt", "r") as file:
    for line in file:
        # Check if the line starts with "* [x]" or "* [ ]"
        if re.match(r"^\ \*\ \[x\].*", line) or re.match(r"^\ \*\ \[\ ].*", line):
            # Use slicing to remove the leading "* [x] " or "* [ ] "
            line = line[line.index("*")+2:]

            # Use slicing to extract the path (starts after "$CFGS/")
            path = line[line.index("$CFGS/")+6:]

            # Use slicing to extract the module (starts after " (module: ")
            module = path[path.index(" (module: ")+10:]
            module = module[:module.index(")")]

            # The rest of the line is the path without the module information
            path = path[:path.index(" (module:")]

            # Print the extracted information
            checkmark = line[:3]
            print("Checkmark: ", checkmark)
            print("Path: ", path)
            print("Module: ", module)
        else:
            print(line)

