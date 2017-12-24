import os
import sys
registry = {}

class Forker():
    def __init__(self):
        self.r = -1
        self.pids = []
        self.myid = '<parent>'

    def fork(self, myid):
        self.r = os.fork()
        if self.r != 0:
            self.pids.append(self.r)
        else:
            self.myid = myid
            self.pids = []

    def is_child(self):
        return self.r == 0

    def is_parent(self):
        return self.r != 0

    def waitfor(self):
        for i in self.pids:
            if i == -1: continue
            os.waitpid(i, 0)

    def mypid(self):
        return os.getpid()

def verify(tcond, forker, ln):
    with open(".pids/%s" % forker.mypid(), 'a+') as f:
        print("%s: %s (True?) at %d" % (forker.myid, str(tcond), ln) , file=f)


def result_mutate(v): return not v

def mutate(myid, cond_result, f):
    global registry
    if f.is_parent():
        # have we spawned this mutant before?
        if myid in registry: return cond_result

        # No we have not spawned.
        f.fork(myid)
        registry[myid] = result_mutate(cond_result) if f.is_child() else cond_result
        return registry[myid]
    else:
        # we are in a continuing execution of a child.
        # get what we replaced the thing at the child
        # originally if this was our mutation. Else just
        # return the original
        return registry.get(myid) or cond_result

