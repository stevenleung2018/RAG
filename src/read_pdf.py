import fitz

# Function to read PDF and return text
def read_pdf(file_path):
    doc = fitz.open(file_path)
    # print(f"doc: {doc}")
    text = ""
    for page in doc:
        text += page.get_text()
        # print(f"text: {text}")
    return text
