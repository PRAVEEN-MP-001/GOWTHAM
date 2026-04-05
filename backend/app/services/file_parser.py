"""File parsing service: handles PDF, DOCX, and TXT extraction."""
import io
from fastapi import UploadFile, HTTPException, status  # type: ignore[import]
import pdfplumber  # type: ignore[import]
from docx import Document  # type: ignore[import]


ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


async def extract_text_from_file(file: UploadFile) -> str:
    """Read an uploaded file and return its text content."""
    content_type = file.content_type or ""

    # Normalise; browsers sometimes send charset suffix for text/plain
    if content_type.startswith("text/plain"):
        content_type = "text/plain"

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. Only PDF, DOCX, and TXT are allowed.",
        )

    raw: bytes = await file.read()  # type: ignore[assignment]

    if len(raw) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the 5 MB size limit.",
        )

    if len(raw) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        if content_type == "application/pdf":
            return _parse_pdf(raw)
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return _parse_docx(raw)
        else:
            return raw.decode("utf-8", errors="replace")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse file: {str(exc)}",
        ) from exc


def _parse_pdf(raw: bytes) -> str:
    """Try pdfplumber first, fall back to pypdf if no text extracted."""
    # Attempt 1: pdfplumber
    try:
        import io as _io
        text_parts = []
        with pdfplumber.open(_io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        result = "\n".join(text_parts).strip()
        if result:
            return result
    except Exception:
        pass

    # Attempt 2: pypdf fallback
    try:
        from pypdf import PdfReader  # type: ignore[import]
        reader = PdfReader(io.BytesIO(raw))
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        result = "\n".join(text_parts).strip()
        if result:
            return result
    except Exception:
        pass

    # Attempt 3: OCR fallback for scanned/image-based PDFs
    try:
        import pytesseract  # type: ignore[import]
        from pdf2image import convert_from_bytes  # type: ignore[import]
        images = convert_from_bytes(raw, dpi=200)
        text_parts = []
        for image in images:
            page_text = pytesseract.image_to_string(image)
            if page_text.strip():
                text_parts.append(page_text)
        result = "\n".join(text_parts).strip()
        if result:
            return result
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=(
            "Could not extract text from this PDF. "
            "The file may be corrupted or heavily formatted. "
            "Try exporting your resume from Word or Google Docs as a PDF."
        ),
    )


def _parse_docx(raw: bytes) -> str:
    doc = Document(io.BytesIO(raw))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    result = "\n".join(paragraphs).strip()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not extract any text from the DOCX file.",
        )
    return result
