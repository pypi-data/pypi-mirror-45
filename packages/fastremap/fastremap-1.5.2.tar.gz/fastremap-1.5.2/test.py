import fastremap
import numpy as np 

data = np.random.randint(0, 150, (512,512,512), dtype=np.uint32)
msk = { i:1 for i in list(range(150)) }
# x= fastremap.remap(data, msk, preserve_missing_labels=True)
x = fastremap.mask(data, msk)
print(x)
# @profile
# def run():
#   x = np.ones( (512,512,512), dtype=np.uint32, order='C')
#   x += 1
#   print(x.strides, x.flags)
#   y = np.asfortranarray(x)
#   print(x.strides, x.flags)

#   print("done.")

# run()