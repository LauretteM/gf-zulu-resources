# -*- coding: utf-8 -*-

import os
import re
import pgf
import pydot
import subprocess
from graphviz import render

LANG_CODE="Zul"

def read_gftest_output(in_str,conc_name):
    pair_pattern = re.compile(r"\*\* [0-9]+\) ([a-zA-Z ()0-9_]+)\n"+conc_name+"> ([a-zA-Z ]+)")
    replace_pattern = re.compile(r"\* ([a-zA-Z_ 0-9]+)\n([a-zA-Z_0-9]+) : [0-9_]+ → ([a-zA-Z_0-9]+)")

    pair_iter = re.finditer(pair_pattern,in_str)
    replace_iter = re.finditer(replace_pattern,in_str)

    replacements = []
    while True:
        try:
            replace_match = next(replace_iter)
            replacements.append((replace_match.group(3),replace_match.group(1)))
        except StopIteration:
            break

    pairs = []
    number = 1
    while True:
        try:
            pair_match = next(pair_iter)
            tree = pair_match.group(1)
            lin = pair_match.group(2)
            for (a,b) in replacements:
                tree = tree.replace(a,b)
            pairs.append((str(number),tree,lin))
            number += 1
        except StopIteration:
            break
    return pairs

def generate_image(tree,grammar,filenamebase,outdirpath):

    imagepath = os.path.join(outdirpath,"images")
    try:
        os.makedirs(imagepath)
    except FileExistsError:
        pass

    expr = pgf.readExpr(tree)
    dotfilepath = os.path.join(imagepath,filenamebase+'.dot')
    pngfilename = filenamebase+'.png'
    pngfilepath = os.path.join(imagepath,pngfilename)
    dotfile = open(dotfilepath,'w')
    dotfile.write(grammar.graphvizAbstractTree(expr))
    dotfile.close()

    subprocess.run(["dot","-Tpng",dotfilepath,"-o",pngfilepath])

    return pngfilename

def generate_html(imglin_pairs):
    html_head = "<head><style>th, td { padding: 15px; font-size: x-large; } table,td { border: 1px solid black; }</style></head>"
    html_code = "<body><table>\n\t<tr>\n\t\t<th>Number</th><th>Tree</th><th>Linearisation</th>\n\t</tr>\n"
    for (number,img,lin) in imglin_pairs:
        html_code += "\t<tr>\t\t<td>%s</td><td><img src=images/%s></td><td>%s</td>\n\t</tr>" % (number,img,lin)
    html_code += "</table></body>"
    return html_head + html_code

def gftest2html(infilepath,outdirpath,grammar,lang_code):

    (indirpath,infilename) = os.path.split(infilepath)

    conc_name = grammar.abstractName+lang_code
    infilenamebase = infilename[:infilename.rindex('.')]
    outfilepath = os.path.join(outdirpath,infilenamebase + '.html')

    in_str = open(infilepath,'r').read()
    treelin_pairs = read_gftest_output(in_str,conc_name)
    print("Generating images...")
    imglin_pairs = [(number,generate_image(tree,grammar,infilenamebase+number,outdirpath),lin) for (number,tree,lin) in treelin_pairs]
    html_code = generate_html(imglin_pairs)
    print("Writing HTML...")
    outfile = open(outfilepath,'w')
    outfile.write(html_code)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help='sub-command help')

    parser_viz = subparsers.add_parser('viz_gftest', help='visualise gftest output with HTML')

    parser_viz.add_argument("input",help="file containing gftest output")
    parser_viz.add_argument("grammar",help="PGF grammar")
    parser_viz.add_argument("-d",dest="outdirpath",help="directory to save html file (default: .)")
    parser_viz.add_argument("-l",dest="lang_code",help="3-letter ISO code")

    args = parser.parse_args()

    lang_code = args.lang_code if args.lang_code else LANG_CODE

    grammar = pgf.readPGF(args.grammar)
    infilepath = args.input
    outdirpath = args.outdirpath if args.outdirpath else "."
    gftest2html(infilepath,outdirpath,grammar,lang_code)
