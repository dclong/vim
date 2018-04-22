
def junit(snip):
    if snip.opt("g:ultisnips_java_junit", "") == "3":
        snip += ""
    else:
        snip.rv += "@Test\n\t"
#end def

def nl(snip):
    if snip.opt("g:ultisnips_java_brace_style", "") == "nl":
        snip += ""
    else:
        snip.rv += " "
#end def

def get_args(group):
	import re
	word = re.compile('[a-zA-Z><.]+ \w+')
	return [i.split(" ") for i in word.findall(group) ]
#end def

def camel(word):
	return word[0].upper() + word[1:]
#end def
