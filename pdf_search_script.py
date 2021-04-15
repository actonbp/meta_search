from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import re
import os
import glob
import io
import csv
import pandas as pd

parent_dir = "../python"

def convert(fname):
    output_string = StringIO()
    result = []
    name = []
    with open(fname, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        Text = (output_string.getvalue())
        String = "table" ##replace words searched here
        ResSearch = bool(re.search(String, Text))
        article = str(fname.split('\\', 1)[1])
        print("Processing file: " + str(article))
        name.append(str(article))
        result.append(str(ResSearch))
        in_file.close()
    dict = {'name': name, 'table': result}   ##replace words searched here
    df = pd.DataFrame(dict)  
    return(df)

pdf_files = glob.glob("%s/*.pdf" % parent_dir)

df_list = [convert(file) for file in pdf_files]

final_df = pd.concat(df_list, ignore_index = True)

final_df.to_csv("table.csv", index=False) ##replace words searched here