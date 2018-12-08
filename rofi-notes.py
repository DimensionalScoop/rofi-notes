#!/bin/python3
import sys
import os
import dynmen as d
from os import listdir
from os.path import isfile, join
import subprocess

path = "/home/elayn/Projects/rofi-notes/notes/"
params={"lines" : 10 ,
"bw" : 3,
"separator-style" : None,
"hide_scrollbar" : True,
"padding" : 10,
"opacity" : 95,
"sidebar-mode" : True,
"width" : 25,
"terminal" : "lxterminal",
"color-enabled" : True,
"color_window" : "#333333, #333333, #444444",
"color_normal" : "#333333, #dddddd, #444444, #c5dbab, #333333",
"color_active" : "#333333, #dddddd, #444444, #c5dbab, #333333",
"color_urgent" : "#333333, #fda626, #444444, #fda626, #333333"}
rofi = d.new_rofi(**params)

def call_menu(list=[],prompt=None):
    if prompt is not None:
        rofi.prompt=prompt
    else:
        rofi.prompt=None
    try:
        res = rofi(list)
        return res
    except d.MenuError:
        return None

def get_files():
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        if f.find(".")!=-1:
            yield ".".join(f.split('.')[:-1])
        else:
            yield f

def open_in_vim(file, start_at_line="1"):
    os.system('xfce4-terminal --geometry +350+200 --command="vim +'+start_at_line+ " " + path + file+'"')


def grep(pattern):
    result = subprocess.run(['grep -nri "'+path+'" -e "'+pattern+'"'], stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    lines = result.stdout.decode().split('\n')

    res = {}
    for l in lines:
        if l=="": continue
        split = l.split(':')
        file,line,expr = split[0],split[1],":".join(split[2:])
        file = file.split('/')[-1]
        term = ".".join(file.split('.')[:-1])+'\t'+ expr
        res[term] = [".".join(file.split('.')[:-1]),line]
    return res


def open_note():
    files = get_files()
    selection = call_menu(files,"notes")
    if selection is not None:
        open_in_vim(selection.selected+".adoc")


def open_as_pdf():
    files = get_files()
    selection = call_menu(files,"notes")
    if selection is not None:
        os.system('asciidoctor -r asciidoctor-pdf -b pdf  -a icons=font -a allow-uri-read -D "/tmp/" '+path+selection.selected+ ".adoc")
        os.system('mupdf /tmp/'+selection.selected+'.pdf')


def open_grep():
    selection = call_menu(prompt="grep")
    if selection is None: return
    search_res = grep(selection.selected)
    res = call_menu(search_res)
    if res is None: return
    open_in_vim(res.value[0]+".adoc",res.value[1])

def open_proj():
    pass

try:
    if sys.argv[1]=="grep":
        open_grep()
    elif sys.argv[1]=="pdf":
        open_as_pdf() 
    else:
        open_note()
except:
    open_note()
