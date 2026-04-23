import os
from dataclasses import dataclass
from pathlib import Path

from werkzeug.utils import secure_filename

from ai.prompts import DEFAULT_AUDIENCE_ID, DEFAULT_PROMPT_ID
from ai.summarizer import DraftGenerator
from core.extractor import (
    extract_text,
    extract_text_from_docx_bytes,
    extract_text_from_pdf_bytes,
)
from core.formatter import format_structure
from core.structure_parser import extract_structure
from storage.file_manager import save_text


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_DOCUMENT_UPLOADS = 5


@dataclass
class MaterialBundle:
    compiled_text: str
    source_names: list[str]
    char_count: int
    word_count: int


def _prepare_text_for_ai(raw_text):
    structured = extract_structure(raw_text)
    return format_structure(structured).strip()


def get_allowed_extensions():
    return sorted(ALLOWED_EXTENSIONS)


def get_max_document_uploads():
    return MAX_DOCUMENT_UPLOADS


def build_material_bundle(uploaded_files, pasted_text, max_input_chars):
    sections = []
    source_names = []
    source_char_count = 0
    valid_uploads = [
        uploaded_file
        for uploaded_file in uploaded_files
        if uploaded_file and uploaded_file.filename
    ]

    if len(valid_uploads) > MAX_DOCUMENT_UPLOADS:
        raise ValueError(
            f"Upload no more than {MAX_DOCUMENT_UPLOADS} documents at a time."
        )

    for uploaded_file in valid_uploads:
        safe_name = secure_filename(uploaded_file.filename) or "uploaded-material"
        suffix = Path(safe_name).suffix.lower()

        if suffix == ".doc":
            raise ValueError(
                f"{safe_name} is a legacy Word document. Save it as a DOCX file and upload it again."
            )

        if suffix not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"{safe_name} is not supported. Upload PDF, DOCX, or TXT files only."
            )

        file_bytes = uploaded_file.read()
        if not file_bytes:
            continue

        if suffix == ".pdf":
            raw_text = extract_text_from_pdf_bytes(file_bytes)
        elif suffix == ".docx":
            raw_text = extract_text_from_docx_bytes(file_bytes)
        else:
            raw_text = file_bytes.decode("utf-8", errors="ignore")

        prepared_text = _prepare_text_for_ai(raw_text)
        if not prepared_text:
            raise ValueError(f"{safe_name} did not contain readable text.")

        source_names.append(safe_name)
        sections.append(f"Source: {safe_name}\n\n{prepared_text}")
        source_char_count += len(prepared_text)

    pasted_text = (pasted_text or "").strip()
    if pasted_text:
        prepared_pasted_text = _prepare_text_for_ai(pasted_text)
        if not prepared_pasted_text:
            raise ValueError("The pasted text did not contain readable content.")

        source_names.append("Pasted text")
        sections.append(f"Source: Pasted text\n\n{prepared_pasted_text}")
        source_char_count += len(prepared_pasted_text)

    if not sections:
        raise ValueError(
            "Upload at least one PDF, DOCX, or TXT file, or paste source material before generating notes."
        )

    compiled_text = "\n\n" + ("\n\n---\n\n".join(sections))
    char_count = len(compiled_text)

    if source_char_count > max_input_chars:
        raise ValueError(
            "The combined source text is too large for one note. "
            f"Limit: {max_input_chars:,} characters. Current source text: {source_char_count:,} characters."
        )

    return MaterialBundle(
        compiled_text=compiled_text,
        source_names=source_names,
        char_count=char_count,
        word_count=len(compiled_text.split()),
    )


def generate_draft(
    config,
    material_bundle,
    prompt_id,
    audience_id,
    custom_instructions="",
    draft_title="",
):
    generator = DraftGenerator(config)
    return generator.generate(
        text=material_bundle.compiled_text,
        prompt_id=prompt_id,
        audience_id=audience_id,
        custom_instructions=custom_instructions,
        draft_title=draft_title,
    )


def generate_legal_draft(
    config,
    material_bundle,
    prompt_id,
    audience_id,
    custom_instructions="",
    draft_title="",
):
    return generate_draft(
        config=config,
        material_bundle=material_bundle,
        prompt_id=prompt_id,
        audience_id=audience_id,
        custom_instructions=custom_instructions,
        draft_title=draft_title,
    )


def process_pdf(pdf_path, config):
    raw_text = extract_text(pdf_path)
    prepared_text = _prepare_text_for_ai(raw_text)
    material_bundle = MaterialBundle(
        compiled_text=f"Source: {os.path.basename(pdf_path)}\n\n{prepared_text}",
        source_names=[os.path.basename(pdf_path)],
        char_count=len(prepared_text),
        word_count=len(prepared_text.split()),
    )

    draft = generate_draft(
        config=config,
        material_bundle=material_bundle,
        prompt_id=DEFAULT_PROMPT_ID,
        audience_id=DEFAULT_AUDIENCE_ID,
    )

    filename = os.path.basename(pdf_path).replace(".pdf", "_notes.txt")
    output_path = os.path.join(config["output_folder"], filename)
    save_text(output_path, draft)

    return output_path
