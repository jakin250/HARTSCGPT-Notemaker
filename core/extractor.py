import io
import zipfile
from xml.etree import ElementTree as ET

import fitz


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD_TAGS = {
    "paragraph": f"{{{WORD_NAMESPACE}}}p",
    "text": f"{{{WORD_NAMESPACE}}}t",
    "tab": f"{{{WORD_NAMESPACE}}}tab",
    "line_break": f"{{{WORD_NAMESPACE}}}br",
    "carriage_return": f"{{{WORD_NAMESPACE}}}cr",
}


def _extract_from_document(document):
    return "\n".join(page.get_text("text") for page in document)


def extract_text(pdf_path):
    with fitz.open(pdf_path) as document:
        return _extract_from_document(document)


def extract_text_from_pdf_bytes(file_bytes):
    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        return _extract_from_document(document)


def extract_text_from_docx_bytes(file_bytes):
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as archive:
            document_xml = archive.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile) as error:
        raise ValueError("The DOCX file could not be read.") from error

    root = ET.fromstring(document_xml)
    paragraphs = []

    for paragraph in root.iter(WORD_TAGS["paragraph"]):
        fragments = []

        for node in paragraph.iter():
            if node.tag == WORD_TAGS["text"] and node.text:
                fragments.append(node.text)
            elif node.tag == WORD_TAGS["tab"]:
                fragments.append("\t")
            elif node.tag in {WORD_TAGS["line_break"], WORD_TAGS["carriage_return"]}:
                fragments.append("\n")

        paragraph_text = "".join(fragments).strip()
        if paragraph_text:
            paragraphs.append(paragraph_text)

    return "\n".join(paragraphs)
