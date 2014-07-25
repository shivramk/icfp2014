from os import listdir
from os.path import join, exists
from subprocess import Popen, PIPE

def run_one(infile, stdout, stderr):
    p = Popen(["python", "lispcompiler.py", join('tests', infile)], 
            stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout_ = p.stdout.read().strip()
    stderr_ = p.stderr.read().strip()
    if stdout_ != stdout:
        print "Test %s failed" % (infile)
        print "Expected: \n%s\nGot: \n%s\n" % (stdout, stdout_)
    elif stderr_ != stderr:
        print "Test %s failed" % (infile)
        print "Expcected: \n%s\n, Got: \n%s\n" % (stderr, stderr_)
    else:
        print "Test '%s' passed" % (infile)

def get_contents(fname, ext1, ext2):
    fname = join('tests', fname.replace(ext1, ext2))
    if exists(fname):
        with open(fname) as f:
            return f.read().strip()
    return ""

def main():
    for i in listdir('tests'):
        if not i.endswith('.lisp'):
            continue
        stdout = get_contents(i, '.lisp', '.out')
        stderr = get_contents(i, '.lisp', '.err')
        run_one(i, stdout, stderr)

if __name__ == "__main__":
    main()
