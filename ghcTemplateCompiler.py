import sys
import re

lableMarkerRE = re.compile(';\s*(\\$[a-zA-Z]*)')

def compile(inFile):
    progTemplate = open(inFile).readlines()
    
    lablesMap = buildLabels(progTemplate)
    
    for line in map(lambda line: replaceLables(lablesMap, line.strip()), progTemplate):
        print line
    
def replaceLables(lablesMap, line):
    for lable, lineNo in lablesMap.iteritems():
        line = line.replace(lable, str(lineNo))
        
    return line

def buildLabels(progTemplate):
    lineNo = 0
    lablesMap = {}
    
    for line in progTemplate:
        match = lableMarkerRE.match(line.strip())
        if match != None:
            lablesMap[match.group(1)] = lineNo
        
        if len(line.strip()) != 0 and not line.strip().startswith(';'):
            lineNo += 1
            
    return lablesMap

def main():
    if len(sys.argv) != 2:
        print "usage: ghcTemplateCompiler.py <infile.ghc.template>"
        sys.exit(1)

    compile(sys.argv[1])

if __name__ == "__main__":
    main()
