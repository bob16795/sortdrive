#!/usr/bin/env python
import os
import glob
import subprocess


def check(j):
    if (j.decode("utf-8").split('.')[-1]) != j.decode("utf-8"):
        return types.get(j.decode("utf-8").split('.')[-1], None)
    else:
        return types[None].get(j.decode("utf-8").split('/')[-1], None)


paths = ["/root/disk.d/new"]
types = {
        "pdf": "/root/disk.d/doc/pdf/",
        "odt": "/root/disk.d/doc/wrd/",
        "doc": "/root/disk.d/doc/wrd/",
        "docx": "/root/disk.d/doc/wrd/",
        "ods": "/root/disk.d/doc/xls/",
        "xlsx": "/root/disk.d/doc/xls/",
        "xls": "/root/disk.d/doc/xls/",
        "png": "/root/disk.d/pix/Unsorted/",
        "gif": "/root/disk.d/pix/gif/",
        "jpg": "/root/disk.d/pix/Unsorted/",
        "jpe": "/root/disk.d/pix/Unsorted/",
        "jpeg": "/root/disk.d/pix/Unsorted/",
        "part": "rm ",
        "4tc": "rm ",
        "xref": "rm ",
        "tmp": "rm ",
        "pyc": "rm ",
        "pyo": "rm ",
        "fls": "rm ",
        "vrb": "rm ",
        "fdb_latexmk": "rm ",
        "bak": "rm ",
        "swp": "rm ",
        "aux": "rm ",
        "log": "rm ",
        "synctex(busy)": "rm ",
        "lof": "rm ",
        "out": "rm ",
        "snm": "rm ",
        "toc": "rm ",
        "bcf": "rm ",
        "xml": "rm ",
        "gz":  "/root/disk.d/doc/arc/",
        "blg": "rm ",
        "bbl": "rm ",
        "zip": "/root/disk.d/doc/arc/",
        "exe": "/root/disk.d/exc/",
        "msi": "/root/disk.d/exc/",
        "jar": "/root/disk.d/exc/",
        "sh":  "/root/disk.d/exc/",
        "apk": "/root/disk.d/pho/apk/",
        "7z":  "/root/disk.d/doc/arc/",
        "iso": "/root/disk.d/doc/disks/",
        "img": "/root/disk.d/doc/disks/",
        "idx": "rm ",
        "ilg": "rm ",
        "ind": "rm ",
        "txt": "/root/disk.d/doc/man/",
        "html": "/root/disk.d/doc/man/",
        "md":  "/root/disk.d/doc/man/",
        "ms":  "/root/disk.d/doc/src/",
        "tex": "/root/disk.d/doc/src/msc/",
        "mu":  "/root/disk.d/doc/src/msc/",
        "bib": "/root/disk.d/doc/cit/",
        "nes": "/root/disk.d/rom/nes/",
        "smc": "/root/disk.d/rom/snes/",
        "sfc": "/root/disk.d/rom/snes/",
        "blend": "/root/disk.d/doc/3d/",
        "blend1": "rm ",
        None:  {
            "LICENSE": "/root/disk.d/doc/man",
            "1": "rm ",
            }
        }


def process_dir(i):
    for j in glob.glob(i + "/*"):
        j = j.encode("utf-8")
        if os.path.isdir(j.decode("utf-8")):
            process_dir(j.decode("utf-8"))
            if os.listdir(j.decode("utf-8")) == []:
                os.rmdir(j.decode("utf-8"))
        if os.path.isfile(j.decode("utf-8")):
            if ".git" not in j.decode("utf-8"):
                checked = check(j)
                if checked is not None:
                    checked = os.path.expanduser(checked)
                    if not checked == "rm ":
                        j = j.replace('\'', '\\\'')
                        if j.decode("utf-8") != checked+j.decode("utf-8").split('/')[-1]:
                            print("mkdir -p '{}'".format(checked))
                            subprocess.call("mkdir -p '{}'".format(checked), shell=True)
                        print("mv '{}' '{}'".format(j.decode("utf-8"), checked+j.decode("utf-8").split('/')[-1]))
                        subprocess.call(("mv '{}' '{}'".format(j.decode("utf-8"),checked+j.decode("utf-8").split('/')[-1])), shell=True)
                    else:
                        print(checked+"'"+j.decode("utf-8") +"'")
                        subprocess.call(checked+"'"+j.decode("utf-8") +"'", shell=True)


for i in paths:
    i = os.path.expanduser(i)
    process_dir(i)
print "files sorted"
