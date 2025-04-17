import docx
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(file, filename):
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    else:
        return {"error": "Unsupported file format."}

    doc = nlp(text)

    skills = [ent.text for ent in doc.ents if ent.label_ in ['SKILL', 'ORG']]
    experience = [ent.text for ent in doc.ents if ent.label_ in ['DATE', 'ORG']]
    education = [ent.text for ent in doc.ents if ent.label_ in ['EDUCATION', 'ORG']]

    return {
        "text": text[:1000],  # обрезаем для примера
        "skills": list(set(skills)),
        "experience": list(set(experience)),
        "education": list(set(education)),
    }
