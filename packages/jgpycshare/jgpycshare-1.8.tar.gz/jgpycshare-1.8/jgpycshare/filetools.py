import os
import requests 

def downfiles(durl,fielpath=None):
    if fielpath is None or len(fielpath) > 0:
        fielpath = durl
    print("downloading with requests",fielpath,durl)
    mkdir(os.path.dirname(fielpath) )

    r = requests.get(durl) 
    with open(fielpath, "wb") as code:
        code.write(r.content)


def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False