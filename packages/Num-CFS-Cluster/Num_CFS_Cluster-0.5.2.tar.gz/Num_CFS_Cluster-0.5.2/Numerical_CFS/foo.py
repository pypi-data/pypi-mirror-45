import numpy as np
foo = np.array([[1,2,3],[11,22,32]])
with open('file'+'_2' +".csv", 'ab') as abc:
    np.savetxt(abc, foo, delimiter=",)
