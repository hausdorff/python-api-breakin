# Scripts that I used to break into a hidden Python API

I, along with my friends Alison Kaptur and Zack Maril, were trying to get something in a dynamic graph visualization (specifically Ubigraph) to work exactly as it had in a demo I saw on YouTube. Upon reading the docs, we saw that they had forgotten to document some of their API. "No problem," we thought. "We'll just drop in with PDB and call `dir` on the graph object `G`."

We tried this and was greeted with this pleasant message:

    (Pdb) dir(G)
    *** Fault: <Fault -506: "Method 'ubigraph.__dir__' not defined">

They deleted the builtin `dir`! What? We disassembled to see what was going on:

    (Pdb) dis.dis(G)
    Disassembly of __call__:
    1224           0 LOAD_FAST                0 (self)
                  3 LOAD_ATTR                0 (_Method__send)
                  6 LOAD_FAST                0 (self)
                  9 LOAD_ATTR                1 (_Method__name)
                 12 LOAD_FAST                1 (args)
                 15 CALL_FUNCTION            2
                 18 RETURN_VALUE        

    Disassembly of __getattr__:
    1222           0 LOAD_GLOBAL              0 (_Method)
                  3 LOAD_FAST                0 (self)
                  6 LOAD_ATTR                1 (_Method__send)
                  9 LOAD_CONST               1 ('%s.%s')
                 12 LOAD_FAST                0 (self)
                 15 LOAD_ATTR                2 (_Method__name)
                 18 LOAD_FAST                1 (name)
                 21 BUILD_TUPLE              2
                 24 BINARY_MODULO       
                 25 CALL_FUNCTION            2
                 28 RETURN_VALUE        

    Disassembly of __init__:
    1219           0 LOAD_FAST                1 (send)
                  3 LOAD_FAST                0 (self)
                  6 STORE_ATTR               0 (_Method__send)

    1220           9 LOAD_FAST                2 (name)
                 12 LOAD_FAST                0 (self)
                 15 STORE_ATTR               1 (_Method__name)
                 18 LOAD_CONST               0 (None)
                 21 RETURN_VALUE        

So not only had they deleted `dir`, they'd deleted everything except these three methods.

We tried some other things. For example, we tried following the debugger deep into the code, hoping it would reveal something about the structure of the code. It turns out that the Python code wraps an RPC layer, so we could only go so far into the code.

We ended up simply generating all possible methods names 3 words long and trying them all. The code for this approach is found in `attack.py`. We started with the UNIX dictionary, but that was too big. So then we scraped all the words from the website, uniq'd them, and ran that instead.

In the end we did uncover some methods we weren't previously aware of.

# Directory structure

`test.py` implements some neat demos which Zack Maril and I wrote to check out the functionality of Ubigraph. Remove calls to `pdb` to run it!

`attack.py` executes the dictionary attack to find hidden methods.

`data` is our unprocessed scrape of the words from the Ubigraph site.

`data_uniqd` is our processed scrape of the words from the site.

# LICENSE

Dear sweet Jesus, I hope you have the good sense to not use any of this anywhere important. BUT, if you really insist, this is all released under the MIT license, which basically says you have to note that I'm author in the source where you add code I wrote.