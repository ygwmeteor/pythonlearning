import os


pathdir = "F:\\11"
ig = ["d" , "e"]
print(pathdir)
for root, dirs, files in os.walk(pathdir,topdown=True):
    dirs[:] = [d for d in dirs if d not in ig]
    for file in files: 
        print(os.path.join(root,file))