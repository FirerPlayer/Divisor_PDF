from PyPDF2 import PdfFileReader, PdfFileWriter
from os import mkdir, remove
from zipfile import ZipFile


def split_pdf(file_path, out_path, is_zip=False, start=1, end: int = None):
    try:
        mkdir(out_path)
    except OSError:
        pass

    pdf = PdfFileReader(file_path)
    sep = "/" if file_path.count("/") != 0 else "\\"
    file_name = file_path.split(sep)[-1].removesuffix(".pdf")
    if not end or end >= pdf.getNumPages() or end <= 0:
        end = pdf.getNumPages()

    if start < 1 or start > end:
        raise IndexError

    if not is_zip:
        i = start
        while i <= end:
            out = PdfFileWriter()
            out.addPage(pdf.pages[i - 1])
            out_s = f"{out_path}/{file_name} - {i}.pdf"
            out.write(open(out_s, "wb"))
            i += 1
    else:
        z = ZipFile(f"{out_path}/{file_name} parts.zip", "w")
        i = start
        while i <= end:
            out = PdfFileWriter()
            out.addPage(pdf.pages[i - 1])
            out_s = f"{file_name} - {i}.pdf"
            out.write(open(out_s, "wb"))
            z.write(out_s)
            remove(out_s)
            i += 1
        z.close()


def get_pdf_number_pages(file_path):
    try:
        return PdfFileReader(file_path).getNumPages()
    except:
        return 1
