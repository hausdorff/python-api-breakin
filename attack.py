from __future__ import with_statement
import keyword
import itertools
import xmlrpclib

#WORDS = "/usr/share/dict/words"
WORDS = "data_uniqd"

server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G = server.ubigraph


def testName (name):
    method_nm = '_'.join(name)
    if keyword.iskeyword(method_nm):
        return
    try:
        eval("G." + method_nm + "()")
        print "G." + method_nm
    except xmlrpclib.Fault as err:
        if err.faultCode != -506:
            print method_nm, err.faultString, err.faultCode
        #print err.faultCode, err.faultString, method_nm
    except NameError as err:
        print err

def iterate (limit):
    for i,triplet in enumerate(itertools.permutations(words, limit)):
        if i % 10000 == 0: print i
        testName(triplet)

if __name__ == '__main__':
    with open(WORDS) as f:
        words = [w.strip() for w in f.readlines()]
        #words = ["add", "new", "edge", "vertex"]
        iterate(3)
        #iterate(2)
        #iterate(1)
