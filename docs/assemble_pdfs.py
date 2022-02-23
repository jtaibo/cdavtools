#!/usr/bin/python3
#

from PyPDF2 import PdfFileMerger
import os
import sys

search_dir = "."
target_doc = "assembled.pdf"

if len(sys.argv) > 1:
    search_dir = sys.argv[1]

if len(sys.argv) > 2:
    target_doc = sys.argv[2]

merger = PdfFileMerger()

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith(".pdf"):
             merger.append( os.path.join(root, file) )

merger.write(target_doc)
merger.close()
