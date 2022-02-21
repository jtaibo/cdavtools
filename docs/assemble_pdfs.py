#!/usr/bin/python3
#

from PyPDF2 import PdfFileMerger
import os
import sys

if len(sys.argv) > 1:
    search_dir = sys.argv[1]
else:
    search_dir = "."

merger = PdfFileMerger()

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith(".pdf"):
             #pdfs.append( os.path.join(root, file)) )
             merger.append( os.path.join(root, file) )


#for pdf in pdfs:
#    merger.append(pdf)

merger.write("storyboard.pdf")
merger.close()
