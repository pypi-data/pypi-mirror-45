import os

def get_resfile(code):
    return os.path.join(os.path.dirname(__file__), 'res', code+'.res')  

def get_resblocks(resfile):
    with open(resfile) as f:
        r = [[word.strip() for word in line.replace(";","").split(",")] for line in f.readlines()]

    idx_head, idx_begin, idx_end = [], [], []
    for i, x in enumerate(r):
        if x == ['begin']:
            idx_head.append(i-1)
            idx_begin.append(i+1)
        if x == ['end']:
            idx_end.append(i)

    blocks = []
    for h, b, e in zip(idx_head,idx_begin,idx_end):
        blocks.append(dict(
            type  = r[h][2], # input/output
            name  = r[h][0], # InBlock/Outblock name
            occurs= True if "occurs" in r[h] else False, # occurs boolean
            args  = [x[1] for x in r[b:e]]))
    return blocks

def query_blocks(code,key,value):
    resfile = get_resfile(code)
    blocks  = get_resblocks(resfile)
    return [block for block in blocks if block[key] == value]

def get_input(code):
    return query_blocks(code=code, key="type", value="input")

def get_output(code):
    return query_blocks(code=code ,key="type", value="output")