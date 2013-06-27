import pdb
import time
import collections
import random
import itertools
import xmlrpclib
import dis

server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G = server.ubigraph

def erdos ():
    vert_ids = range(0,1000)
    p = 0.001

    G.clear()
    pdb.set_trace()

    for id in vert_ids:
        G.new_vertex_w_id(id)

    edge_count = 0
    for i,j in itertools.combinations(vert_ids, 2):
        r = random.random()
        if r <= p:
            edge_count += 1
            id = G.new_edge(i, j)
            #G.set_edge_attribute(id, 'oriented', 'true')
            #G.set_edge_attribute(id, 'arrow', 'true')
            #G.set_edge_attribute(id, 'showstrain', 'true')
            #G.set_edge_attribute(id, 'strength', '0.0')

    print edge_count

def groupbycount (ids):
    return [len(list(li[1])) for li in itertools.groupby(sorted(ids))]

def preferential ():
    G.clear()
    size = 1000
    G.new_vertex_w_id(0)
    ids = [0]
    for i in range(1, size):
        G.new_vertex_w_id(i)
        j = random.choice(ids)
        G.new_edge(i,j)
        ids += [i,j]

    hist = groupbycount(ids)
    histprime = collections.defaultdict(lambda:0)
    for i in hist:
        histprime[i] += 1

    print sorted([(k,v) for k,v in histprime.items()])

if __name__ == '__main__':
    #preferential()
    erdos()
