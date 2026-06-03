import io
import re
from pypdf import PdfReader
from docx import Document

STOPWORDS = {
    # English Stopwords + Generic
    "that", "this", "these", "those", "the", "a", "an", "and", "or", "but",
    "for", "with", "from", "into", "through", "during", "before", "after",
    "above", "below", "between", "various", "many", "some", "any", "each",
    "every", "both", "few", "more", "most", "other", "another", "such",
    "degree", "years", "work", "team", "experience", "skill", "ability",
    "understanding", "knowledge", "working", "strong", "good", "excellent",
    "basic", "proficient", "familiar", "proven", "demonstrated", "required",
    "preferred", "plus", "bonus", "role", "job", "position", "candidate",
    "looking", "seeking", "join", "help", "build", "create", "make", "using",
    "used", "based", "related", "similar", "equivalent", "including",
    
    # Indonesian Stopwords
    "yang", "dan", "di", "ke", "dari", "pada", "dengan", "untuk", "dalam",
    "adalah", "sebagai", "telah", "akan", "dapat", "tidak", "ini", "itu",
    "juga", "atau", "oleh", "seperti", "sehingga", "serta", "saat", "bagi",
    "kemudian", "namun", "karena", "bisa", "harus", "banyak", "beberapa",
    "tahun", "pengalaman", "kemampuan", "keahlian", "pemahaman", "bekerja",
    "baik", "kuat", "dasar", "terbukti", "dibutuhkan", "diutamakan", "nilai",
    "tambah", "peran", "pekerjaan", "posisi", "kandidat", "mencari", "bergabung",
    "membantu", "membangun", "membuat", "menggunakan", "berbasis", "terkait",
    "serupa", "setara", "termasuk"
}

def clean_text(text: str) -> str:
    """Clean extracted text from noise, excess whitespaces, and common artifacts"""
    # Remove non-alphanumeric characters except basic punctuation
    text = re.sub(r'[^\w\s.,;:()\-+/#]', ' ', text)
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove common CV headers/footers
    noise_patterns = [
        r'(?i)page\s+\d+\s+of\s+\d+',
        r'(?i)curriculum\s+vitae',
        r'(?i)resume'
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, ' ', text)
    return text.strip()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return clean_text(text)

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return clean_text("\n".join(text))

def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        return extract_text_from_docx(file_bytes)
    return clean_text(file_bytes.decode("utf-8", errors="ignore"))

def extract_candidate_name(text: str, filename: str) -> str:
    # Fallback name from filename (remove extension and replace separators)
    fallback_name = re.sub(r"\.[^.]+$", "", filename)
    fallback_name = re.sub(r"[-_]", " ", fallback_name).title().strip()
    
    # Try regex matches
    name_patterns = [
        r"(?i)name\s*:\s*([A-Za-z\s.]{2,50})",
        r"(?i)full\s*name\s*:\s*([A-Za-z\s.]{2,50})",
        r"(?i)nama\s*:\s*([A-Za-z\s.]{2,50})"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip()
            name = re.sub(r"\s+", " ", name)
            if len(name.split()) <= 4:
                return name.title()
                
    # Try first non-empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:3]:
        # Clean from common CV words
        if re.match(r"^[A-Za-z\s.]{2,30}$", line) and not any(w in line.lower() for w in ["curriculum", "vitae", "resume", "cv", "page", "contact", "profile"]):
            return line.title()
            
    return fallback_name
