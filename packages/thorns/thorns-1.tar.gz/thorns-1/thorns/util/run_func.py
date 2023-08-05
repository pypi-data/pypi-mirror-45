#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import time
import socket
import sys
import imp

try:
    import cPickle as pickle
except ImportError:
    import pickle

from thorns.util.maps import _FuncWrap

def main():
    socket_fname = sys.argv[1]
    s = socket.socket(socket.AF_UNIX)
    s.connect(socket_fname)


    ### receive function and data from the parent
    f = s.makefile('rb')
    data = pickle.load(f)
    f.close()

    ### unpack the data
    module_name, func_name, args = data
    mod = imp.load_source("mod", module_name)
    func = getattr(mod, func_name)


    ### run function
    wrap = _FuncWrap(func)
    result = wrap(args)


    ### send results to the parent
    f = s.makefile('wb')
    pickle.dump(result, f, -1)
    f.close()


    ### cleanup
    s.close()



if __name__ == "__main__":
    main()
