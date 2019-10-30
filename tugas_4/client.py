import Pyro4
import base64
import json
import sys

namainstance = "fileserver"
try:
    namainstance = sys.argv[1]
except:
    pass

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    return fserver


def mainLoop(fileServer):
    while True:
        print("ÖPS [list, create, read, update, delete]")
        inData = input("OPS : ")
        if inData == "create":
            remoteName = input("Remote name : ")
            fileServer.create(remoteName)
        elif inData == "update":
            remoteName = input("Remote Name : ")
            localName = input("Local Name : ")
            descriptor = open(localName,'rb+')
            content = descriptor.read()
            descriptor.close()
            fileServer.update(remoteName, content)
        elif inData == "read":
            remoteName = input("Remote Name : ")
            localName = input("Local Name : ")
            descriptor = open(localName, 'w+b')
            response = fileServer.read(remoteName)
            payload = base64.b64decode(response["data"])
            descriptor.write(payload)
            descriptor.close()
        elif inData == "list":
            print(f.list())
        elif inData == "delete":
            remoteName = input("Remote Name : ")
            fileServer.delete(remoteName)
        else:
            print("OPS Not found %s" % (inData))

if __name__=='__main__':
    f = get_fileserver_object()
    mainLoop(f)
    # f.create('slide1.pdf')
    # f.update('slide1.pdf', content = open('slide1.pdf','rb+').read() )

    # f.create('slide2.pptx')
    # f.update('slide2.pptx', )

    # print(f.list())
    # d = f.read('slide1.pdf')
    # #kembalikan ke bentuk semula ke dalam file name slide1-kembali.pdf
    # open('slide1-kembali.pdf','w+b').write(base64.b64decode(d['data']))

    # k = f.read('slide2.pptx')
    # #kembalikan ke bentuk semula ke dalam file name slide2-kembali.pptx
    # open('slide2-kembali.pptx','w+b').write(base64.b64decode(k['data']))

