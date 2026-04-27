from PyPDF2 import PdfReader


class PDFHandler:

    @staticmethod
    def read_pdf(path):
        try:
            reader = PdfReader(path)
            text = ""

            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

            return text[:3000]

        except Exception as e:
            print("❌ PDF Error:", e)
            return ""