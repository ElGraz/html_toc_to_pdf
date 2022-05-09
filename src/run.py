import sys

from spider import Spider
from html_to_pdf import HTMLToPDF


class TocToPdf:
    __url = None

    def __init__(self, url: str):
        self.__url = url

    def run(self):
        spider = Spider(self.__url)
        pages = spider.get_pages()
        print(f"\n> Done fetching TOC")
        print(f"= Found a total of {len(pages)} pages ({len(pages)-1} + TOC)")
        print(f"> Starting HTML to PDF\n")

        pdf = HTMLToPDF()
        try:
            for page in pages:
                pdf.add_page(page)
        except Exception as ex:
            print(ex)

        print(pdf.get_files())
        output = "./output.pdf"

        print(f"> Exporting result on {output}")
        pdf.join_files(outpath=output)

        pdf.cleanup()



if __name__ == "__main__":
    print("Running")

    if len(sys.argv) != 2:
        print("Usage: toc_to_pdf [TOC_URL]")
        exit(1)

    inst = TocToPdf(sys.argv[1])
    inst.run()
    print("Terminating")
