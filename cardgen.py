#!/usr/bin/env python
from cheetah.Template import Template
import re, sys, optparse

template = 'template.tex'
# Doesn't support multi-line titles... Might convert to ANTLR later
# to support easier modification.
# http://www.antlr.org
re_text = r'^(.+):$\n((?:\n?.+)+)\n*'
rec = re.compile(re_text, re.MULTILINE)

# Eat stderr
class Discarder(object):
    def write(self, text):
        pass

def fillTemplate(cards):
    # get rid of cheetah stderr output
    temp = sys.stderr
    sys.stderr = Discarder()
    
    output = str(Template(file=template, searchList = { 'cards': cards }))
    
    # restore stderr
    sys.stderr = temp
    
    return output

def compileFromString(instring):
    iterator = rec.finditer(instring)
    return fillTemplate(iterator)

def compile(infile, outfile):
    instring = infile.read()
    output = compileFromString(instring)
    outfile.write(output)
    
def fileHandledExec(func, infile=None, outfile=None):
    if func is None:
        return
        
    if infile is None:
        infile = sys.stdin
    else:
        infile = open(infile, 'r')
    
    if outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(outfile, 'w')
        
    func(infile, outfile)
    
    if infile is not sys.stdin:
        infile.close()
        
    if outfile is not sys.stdout:
        outfile.close()
    
def main():
    p = optparse.OptionParser()
    p.add_option('-i', '--input', help='Card definition file')
    p.add_option('-o', '--output', help='Output File')
    options, args = p.parse_args()
        
    fileHandledExec(compile, options.input, options.output)
    
if __name__ == '__main__':
    main()