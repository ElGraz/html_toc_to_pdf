import os
import subprocess
import tempfile
from weasyprint import HTML, CSS


class HTMLToPDF:
    """Transforms html to pdf, page by page"""
    __out_path = None
    __created_files = None
    __cache = None

    def __init__(self):
        self.__out_path = tempfile.mkdtemp()
        print(f"= saving pages in {self.__out_path}")
        self.__created_files = list()
        self.__cache = dict()

    def add_page(self, page):
        css = CSS(string='''
            p {font-size: 14px;}''')

        fname = tempfile.mkstemp(dir=self.__out_path, suffix=".pdf")[1]
        print(f"= writing pdf to {fname}")
        html = HTML(url=page.url)
        html.write_pdf(fname,
                       optimize_size=('fonts', 'images'),
                       image_cache=self.__cache,
                       stylesheets=[css])

        self.__created_files.append(fname)

    def get_files(self):
        return self.__created_files

    def join_files(self, outpath: str = "./output.pdf"):
        params = ["/usr/bin/pdfjam"]
        for tbj in self.get_files():
            params.append(tbj)
        print(params)
        return subprocess.run(params)


    def cleanup(self):
        for fname in self.__created_files:
            print(f"= removing temp file {fname}")
            try:
                os.unlink(fname)
            except Exception as ex:
                print(ex)
        print(f"= removing temp dir {self.__out_path}")
        try:
            os.removedirs(self.__out_path)
        except Exception as ex:
            print(ex)

