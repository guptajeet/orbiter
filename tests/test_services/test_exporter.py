import io
from backend.utils.exporter import generate_pdf_from_md, generate_docx_from_md

def test_generate_pdf_from_md():
    md = """# My Resume
## Work Experience
- **Developer** at Company: Developed code.
* Built dynamic matching engines.
"""
    pdf_buf = generate_pdf_from_md(md)
    assert isinstance(pdf_buf, io.BytesIO)
    pdf_data = pdf_buf.getvalue()
    assert len(pdf_data) > 0
    # PDF signature is %PDF
    assert pdf_data.startswith(b'%PDF')

def test_generate_docx_from_md():
    md = """# My Resume
## Work Experience
- **Developer** at Company: Developed code.
* Built dynamic matching engines.
"""
    docx_buf = generate_docx_from_md(md)
    assert isinstance(docx_buf, io.BytesIO)
    docx_data = docx_buf.getvalue()
    assert len(docx_data) > 0
    # ZIP signature is PK\x03\x04 (docx files are zip archives)
    assert docx_data.startswith(b'PK\x03\x04')
