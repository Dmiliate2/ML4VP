import os
import shutil
import pyl3dmd

# small patch 
src = "patched/pyl3dmd.py"
dst = os.path.join(os.path.dirname(pyl3dmd.__file__), "pyl3dmd.py")

shutil.copy(src, dst)
print("Patch applied!")
