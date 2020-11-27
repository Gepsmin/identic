#Onur Sefa Özçıbık
#2017400222

import os
import argparse
import hashlib



dictionary = {} #stores values for -cn option
hexed_dictionary = {} #stores values for -c option
name_dictionary = {} #stores values for -n option
root_hashes = {} #intermediate storage
directoy_sizes = {} #intermediate storage

#argparse library operations to parse input
parser = argparse.ArgumentParser(description="You can not hide from your own shadow")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d",help="Search for directories", action="store_true", default=False)
group.add_argument("-f",help="Search for files", action="store_true", default= True)
parser.add_argument("dirs", metavar="Directories", nargs='*', type=str, default=["."])
parser.add_argument("-c", help="Contents are the same", action="store_true", default=False)
parser.add_argument("-n", help="Names are the same", action="store_true", default=False)
parser.add_argument("-s", help="Duplicates are listed in descending order of size", action="store_true", default=False)



args = parser.parse_args()

#helper function to find the size of a directory
def get_size(path):
    if path in directoy_sizes:
        return directoy_sizes[path]
        
    
    for root, directories, files in os.walk(path):
        total_size = 0
        file_size = 0
        directory_size = 0
        for filename in files:
            file_location = os.path.join(path, filename)
            file_size += os.path.getsize(file_location)
        for directory in directories:
            directory_location = os.path.join(path, directory)
            if directory_location in directoy_sizes:
                directory_size += directoy_sizes[directory_location]
            else:
                this_size = get_size(directory_location)
                directoy_sizes.update({directory_location:this_size})
                directory_size += this_size
        total_size = directory_size + file_size
        directoy_sizes.update({root:total_size})
        return total_size



# -f -cn operations
def name_hash_files():
    for filename in files:
        file_location = os.path.join(root, filename)
        file_hash = hashlib.sha256()
        with open(file_location, 'rb') as f:
            fb = f.read()
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read()
        hh = file_hash.hexdigest()
        if hh in dictionary:
            if filename in dictionary[hh]:
                dictionary[hh][filename].add(file_location)
            else:
                dictionary[hh].update({filename: {file_location}})
        else:
            dictionary.update({hh: {filename:{file_location}}})

#-d -cn operations
def name_hash_directories():
    roots = root.split("\\")
    root_name = roots[len(roots)-1]
    for filename in files:
        file_location= os.path.join(root,filename)
        file_hash = hashlib.sha256()
        with open(file_location, 'rb') as f:
            fb = f.read()
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read()
        hh = file_hash.hexdigest()
        if root in root_hashes:
            root_hashes[root].append(hh)
        else:
            root_hashes.update({root: [hh]})
    
    d = os.path.dirname(root)
    l = []
    s = ''
    if root in root_hashes:
        l = root_hashes[root]
        l.sort()
        for a in l:
            s = s + a
    s_hash = hashlib.sha256()
    s_hash.update(s.encode("utf-8"))
    ss = s_hash.hexdigest()
    if d:
        if d in root_hashes:
            root_hashes[d].append(ss)
        else:
            root_hashes.update({d:[ss]})
    
    if ss in dictionary:
        if root_name in dictionary[ss]:
            dictionary[ss][root_name].add(root)
        else:
            dictionary[ss].update({root_name: {root}})
    else:
        dictionary.update({ss:{root_name:{root}}})

#-f -c operations
def hash_files():
    for filename in files:
        file_location= os.path.join(root,filename)
        file_hash = hashlib.sha256()
        with open(file_location, 'rb') as f:
            fb = f.read()
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read()
        hh = file_hash.hexdigest()
        if hh in hexed_dictionary:
            hexed_dictionary[hh].add(file_location)
        else:
            hexed_dictionary.update({hh:{file_location}})

#-d -c operations
def hash_directories():
    for filename in files:
        file_location= os.path.join(root,filename)
        file_hash = hashlib.sha256()
        with open(file_location, 'rb') as f:
            fb = f.read()
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read()
        hh = file_hash.hexdigest()
        if root in root_hashes:
            root_hashes[root].append(hh)
        else:
            root_hashes.update({root: [hh]})
    
    d = os.path.dirname(root)
    l = []
    s = ''
    if root in root_hashes:
        l = root_hashes[root]
        l.sort()
        for a in l:
            s = s + a
    s_hash = hashlib.sha256()
    s_hash.update(s.encode("utf-8"))
    ss = s_hash.hexdigest()
    if d:
        if d in root_hashes:
            root_hashes[d].append(ss)
        else:
            root_hashes.update({d:[ss]})
    
    if ss in hexed_dictionary:
        hexed_dictionary[ss].add(root)
    else:
        hexed_dictionary.update({ss:{root}})

#-f -n operations
def name_files():
    for filename in files:
        file_location = os.path.join(root, filename)
        if filename in name_dictionary:
            name_dictionary[filename].add(file_location)
        else:
            name_dictionary.update({filename:{file_location}})
        
#-d -n operations
def name_directories():
    roots = root.split("\\")
    root_name = roots[len(roots)-1]
    if root_name in name_dictionary:
        name_dictionary[root_name].add(root)
    else:
        name_dictionary.update({root_name:{root}})

#traversing the directories
#the main operation runs from here
#it uses appropriate function to traverse and get true data from them
BLOCK_SIZE = 65536
if not (args.c or args.n):
    print("Please select -n or -c")
else:
    for params in args.dirs:
        path = os.path.abspath(params)

        for root, directories, files in os.walk(path, topdown=False):
            if args.d:
                if args.n and args.c:
                    name_hash_directories()
                elif args.n:
                    name_directories()
                elif args.c:
                    hash_directories()
                else:
                    print("Please select -n or -c")
            else:
                if args.n and args.c:
                    name_hash_files()
                elif args.n:
                    name_files()
                elif args.c:
                    hash_files()
                else:
                    print("Please select -n or -c")    

        


#printing
#size comparison
if args.s and (args.c or (args.c and args.n)):
    c = {}
    cn = {}
    #size comperison for -d
    if args.d:
        l = []
        if args.c and args.n:
            for hashe in dictionary:
                for name in dictionary[hashe]:
                    if len(dictionary[hashe][name]) <= 1:
                        break
                    length = 0
                    strings = []
                    string = ''
                    for a in dictionary[hashe][name]:
                        if length == 0:
                            length = get_size(a)
                        strings.append(a)
                    strings.sort()
                    for dir_string in strings:
                        if string == '':
                            string = dir_string + '\t' + str(length)
                        else:
                            string = string + '\n' + dir_string + '\t' + str(length)

                    if length in cn:
                        if name in cn[length]:
                            cn[length][name].append(string)
                        else:
                            cn[length].update({name: [string]})
                    else:
                        cn.update({length:{name:[string]}})

        else:
            for s in hexed_dictionary:
                if len(hexed_dictionary[s]) > 1:
                    length = 0
                    strings = []
                    string = ''
                    for a in hexed_dictionary[s]:
                        if length == 0:
                            length = get_size(a)
                        strings.append(a)
                        
                    strings.sort()
                    for dir_string in strings:
                        if string == '':
                            string = dir_string + '\t' + str(length)
                        else:
                            string = string + '\n' + dir_string + '\t' + str(length)
                    
                    if length in c:
                        c[length].append(string)
                    else:
                        c.update({length:[string]})

    #size comparison for -f
    elif args.f:
        l = []
        if args.c and args.n:
            for hashe in dictionary:
                for name in dictionary[hashe]:
                    if len(dictionary[hashe][name]) <= 1:
                        break
                    length = 0
                    strings = []
                    string = ''
                    for a in dictionary[hashe][name]:
                        if length == 0:
                            length = os.path.getsize(a)
                        strings.append(a)
                    strings.sort()
                    for dir_string in strings:
                        if string == '':
                            string = dir_string + '\t' + str(length)
                        else:
                            string = string + '\n' + dir_string + '\t' + str(length)

                    if length in cn:
                        if name in cn[length]:
                            cn[length][name].append(string)
                        else:
                            cn[length].update({name: [string]})
                    else:
                        cn.update({length:{name:[string]}})


        else:
            for s in hexed_dictionary:
                if len(hexed_dictionary[s]) > 1:
                    length = 0
                    strings = []
                    string = ''
                    for a in hexed_dictionary[s]:
                        if length == 0:
                            length = os.path.getsize(a)
                        strings.append(a)
                    strings.sort()
                    for dir_string in strings:
                        if string == '':
                            string = dir_string + '\t' + str(length)
                        else:
                            string = string + '\n' +  dir_string + '\t' + str(length)

                    if length in c:
                        c[length].append(string)
                    else:
                        c.update({length: [string]})

#decision of output order for -cn -s
    if args.n and args.c:
        lst = []
        for x in cn.keys():
            lst.append(x)
        lst.sort(reverse=True)

        for length in lst:
            lstlst = []
            for name in cn[length].keys():
                lstlst.append(name)
            lstlst.sort()

            for name in lstlst:
                lstlstlst = []
                for string in cn[length][name]:
                    lstlstlst.append(string)
                lstlstlst.sort()

                for result in lstlstlst:
                    print(result)
                    print()
#decision of output order for -c -s
    elif args.c:
        lst = []
        for x in c.keys():
            lst.append(x)
        lst.sort(reverse=True)

        for length in lst:
            if len(c[length]) == 1:
                print(c[length][0])
                print()
            else:
                lstlst = []
                for ssss in c[length]:
                    lstlst.append(ssss)
                lstlst.sort()

                for ss in lstlst:
                    print(ss)
                    print()
#desicions for not comparing the sizes
else:
    n = []
    cn = {}
    c = []
    if args.c and args.n:
        for s in dictionary:
            for x in dictionary[s]:
                ds = []
                string = ''
                if len(dictionary[s][x]) > 1:
                    for a in dictionary[s][x]:
                        ds.append(a)
                    ds.sort()

                    for d in ds:
                        if string == '':
                            string = d
                        else:
                            string = string + '\n' + d
                    
                    if x in cn:
                        cn[x].append(string)
                    else:
                        cn.update({x:[string]})

            
    elif args.n:
        for s in name_dictionary:
            if len(name_dictionary[s]) > 1:
                n.append(s)

    elif args.c:
        for s in hexed_dictionary:
            if len(hexed_dictionary[s]) > 1:
                c.append(s)
    
#printing in right order 
    if args.c and args.n:
        lst = []
        for x in cn.keys():
            lst.append(x)
        lst.sort()
        
        for name in lst:
            strings = []
            if len(cn[name]) == 1:
                print(cn[name][0])
                print()
            else:
                for string in cn[name]:
                    strings.append(string)
                strings.sort()

                for s in strings:
                    print(s)
                    print()


    elif args.n:
        n.sort()
        for x in n:
            l = []
            for a in name_dictionary[x]:
                l.append(a)
            l.sort()
            
            for result in l:
                print(result)
            print()
    
    elif args.c:
        results = []
        for x in c:
            result_part = ''
            l = []
            for a in hexed_dictionary[x]:
                l.append(a)
            l.sort()

            for r in l:
                if result_part == '':
                    result_part = r
                else:
                    result_part = result_part + '\n' + r
            results.append(result_part)
        
        results.sort()
        for m in results:
            print(m)
            print()
        
