import sys
import os
import pickle

import mapStorage
import mapData

for f in mapData.functions:
    theMap = f()
    ms = mapStorage.storeMap(theMap)

    filepath = "maps/" + theMap.name + ".nzmp"

    if os.path.exists(filepath):
        print("already exists")
    else:
        with open(filepath, 'wb') as fp:
            pickle.dump(ms, fp)
