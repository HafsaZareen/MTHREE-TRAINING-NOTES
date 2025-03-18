import os
checkpath=os.path.exists("test_dir")
if not checkpath:
    os.mkdir("test_dir")
else:
    print("not present")
