import spacy

nlp = spacy.load("en_core_web_sm")

def match_resume_to_job(resume_text, job_description):
    resume_doc = nlp(resume_text.lower())
    job_doc = nlp(job_description.lower())

    resume_words = set([token.lemma_ for token in resume_doc if not token.is_stop and token.is_alpha])
    job_words = set([token.lemma_ for token in job_doc if not token.is_stop and token.is_alpha])

    overlap = resume_words & job_words
    score = len(overlap) / max(len(job_words), 1)  # процент совпадения

    return round(score * 100, 2), list(overlap)
