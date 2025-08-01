import fitz

# Function to read PDF and return text
def read_pdf(file_path):
    doc = fitz.open(file_path)
    
    text = ""
    for page in doc:
        text += page.get_text()
        
    return text
