from io import BytesIO

import pdfplumber


class PDFExtractionError(RuntimeError):
	"""Base error for PDF text extraction failures."""


class CorruptedPDFError(PDFExtractionError):
	pass


class EmptyPDFError(PDFExtractionError):
	pass


def extract_text_from_pdf(file_content: bytes) -> str:
	try:
		with pdfplumber.open(BytesIO(file_content)) as pdf:
			page_text = [(page.extract_text() or "").strip() for page in pdf.pages]
	except Exception as exc:
		raise CorruptedPDFError("The uploaded PDF is corrupted or cannot be read") from exc

	text = "\n\n".join(value for value in page_text if value).strip()
	if not text:
		raise EmptyPDFError("The uploaded PDF does not contain extractable text")
	return text
