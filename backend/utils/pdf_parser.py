class PDFParser:
    def extract_text(self, file_content: bytes) -> str:
        """Extract text from PDF bytes. Uses PyPDF2 if available, falls back to raw decode."""
        try:
            import PyPDF2
            import io
            reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except ImportError:
            # Fallback: try to decode as text
            return file_content.decode('utf-8', errors='ignore')

pdf_parser = PDFParser()
