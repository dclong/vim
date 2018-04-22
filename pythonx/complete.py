import json
import os
import datetime
# import dateutil.parser

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def contains(opt, keywords):
    opt = opt[0] if type(opt)==list else opt
    for k in keywords:
        if k not in opt:
            return False
        #end if
    #end for
    return True
#end def

def complete(keywords, opts=None, file=None, adjust=True):
    if file != None:
        file = os.path.join(os.getenv("HOME"), ".vim/UltiSnips_JSON", file)
        with open(file) as infile:
            opts = json.load(infile)
        #end with
    #end if
    opts.sort(key=lambda x: x[1] if type(x) == list else 0, reverse=True)
    if keywords:
        keylist = [k.strip() for k in keywords.strip().split(" ")]
        keylist = [k.lower() for k in keylist if k != ""]
        last_key = keylist[-1]
        numbers = [str(i) for i in range(10)]
        if last_key in numbers:
            index = [i for i in range(len(opts)) if contains(opts[i], keylist[:-1])][int(last_key)]
            return one_option(opts, index, keywords, file, adjust)
        #end if
        index = [i for i in range(len(opts)) if contains(opts[i], keylist)]
        n = len(index)
        if n == 0:
            return ""
        #end if
        if n == 1:
            return one_option(opts, index[0], keywords, file, adjust)
        #end if
        return multiple_options([opts[i] for i in index])
    #end if
    return multiple_options(opts)
#edef complete

def multiple_options(opts):
    opts = [o[0] if type(o)==list else o for o in opts]
    n = len(opts)
    for i in range(n):
        if i < 10:
            opts[i] = "(" + str(i) + ") " + opts[i]
        else:
            opts[i] = "(X) " + opts[i]
        #end if
    #end for
    return "\n" + "-" * 80 + "\n    " + "\n    ".join(opts) + "\n" + "-" * 80 + "\n"
#end def

def one_option(opts, index, keywords, file, adjust):
    opt = opts[index]
    if adjust and file != None:
        time_now = datetime.datetime.now()
        # increase frequency of opts[index] 
        if type(opt) == list:
            time_last_updated = datetime.datetime.strptime(opt[2], TIME_FORMAT)
            if (time_now - time_last_updated).total_seconds() <= 30:
                # do not update frequency
                return format_option(opt, keywords)
            #end if
            opt[1] = opt[1] + 1
            opt[2] = datetime.datetime.strftime(time_now, TIME_FORMAT)
            opt = opt[0] 
        else:
            opts[index] = [opt, 1, str(time_now)]
        #end if
        # write it back to the file
        with open(file, "w") as outfile:
            json.dump(opts, outfile, indent=4)
        #end with
    #end if
    return format_option(opt, keywords)
#end def

def format_option(opt, keywords):
    if type(opt) == list:
        opt = opt[0]
    #end if
    if opt.find(": ") >= 0:
        opt = opt[:opt.index(": ")]
    #end if
    if opt.startswith(keywords):
        return opt[len(keywords):]
    #end if
    return "\n" + " " * 8 + opt
#end def
