import mammoth

class WordProcessor():
    @staticmethod
    def WordToHtml(wordPath):
        # Convert Word document to HTML
        with open(wordPath, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            return result
    @staticmethod
    def FileSystemStorage(rootPath, filePath):
        pass