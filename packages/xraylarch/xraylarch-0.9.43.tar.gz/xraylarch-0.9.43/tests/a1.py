import os

from utils import LarchSession

session = LarchSession()
symtable = session.symtable

def runscript(fname, dirname='.'):
    origdir = os.path.abspath(os.getcwd())
    dirname = os.path.abspath(dirname)
    os.chdir(dirname)
    with open(fname, 'r') as fh:
        text = fh.read()
    session.error = []
    session.run(text)
    os.chdir(origdir)


    print(session._larch.error)
    print(session._larch.show_errors())

runscript('u.lar', dirname='../examples/xafs/')
