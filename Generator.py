from groq import  Groq
from docx import Document
import  os

client = Groq(api_key="PUT_YOUR_KEY")

def generate_cv(field, job_description, num_cvs):

    prompt = f"""
    You are an expert career consultant and resume writer. 
    Generate {num_cvs} different professional CVs tailored for the following job description and field.

    Field: {field}
    Job Description: {job_description}

    Each CV should include:
    - Name (fake realistic name)
    - Contact Information (phone, email, LinkedIn)
    - Professional Summary
    - Skills
    - Work Experience
    - Education
    - Certifications
    - Projects
    
    Rules:
    - Generate EXACTLY {num_cvs} CVs.
    - Each CV must be COMPLETE. Do not stop halfway.
    - If you run out of space, reduce the level of detail but ensure all sections are present.
    - Separate CVs with '---'


    The CVs should be clear, well-structured, ATS-friendly, and realistic.
    Format the CVs in plain text with clear headings and bullet points.
    """

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=65_536,
        top_p=1,
        reasoning_effort="medium",
        stream=False
    )
    return completion.choices[0].message.content

def save_to_word(text, filename="cv.docx"):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)

if __name__ == "__main__":

    field = input("Enter Field Name: ")
    job_description = "Random Job Description , based on the field "
    num_cvs = int(input("Enter Number of CVs: "))

    cv_text = generate_cv(field, job_description, num_cvs)
    cv_list = cv_text.split("---")
    os.makedirs("Generated_CVs", exist_ok=True)
    for idx, cv in enumerate(cv_list, start=1):
        cv = cv.strip()
        if not cv:
            continue
        word_filename = f"Generated_CVs/CV_{idx}.docx"
        save_to_word(cv, word_filename)
