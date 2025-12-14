from pathlib import Path
import pdfplumber
from docx import Document


SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx", ".pdf"}


def read_txt_or_md(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")


def read_docx(file_path: Path) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def read_pdf(file_path: Path) -> str:
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Неподдерживаемый формат: {ext}")

    if ext in [".txt", ".md"]:
        return read_txt_or_md(path)

    if ext == ".docx":
        return read_docx(path)

    if ext == ".pdf":
        return read_pdf(path)
    raise RuntimeError("Не удалось обработать файл")


def convert_to_txt(input_file: str, output_dir: str = "output_txt") -> str:
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    text = extract_text(input_file)

    output_file = output_path / f"{input_path.stem}.txt"
    output_file.write_text(text, encoding="utf-8")

    return str(output_file)

def get_result_file(file: str) -> str:
    input_file = file
    result = convert_to_txt(input_file)
    return result