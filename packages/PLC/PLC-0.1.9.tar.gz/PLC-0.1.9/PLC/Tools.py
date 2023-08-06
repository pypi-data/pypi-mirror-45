import shutil
import os
import docx
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer3.layout import LAParams
import io


def CreateDirectory(Path, RemoveifExist=True):
    if os.path.isdir(Path) and RemoveifExist:
        shutil.rmtree(Path)
    if not os.path.isdir(Path):
        os.mkdir(Path)
def getDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
def pdfparser(file):
    fp = open(file, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()
    return str(data)
def readFile(file):
    f = open(file, 'a+')
    text = f.read()
    f.close()
    return text
