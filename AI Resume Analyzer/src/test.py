import os
import json
import PyPDF2
from docx import Document

class test: 
    def __init__(self, filename): self.filename = filename 

    def parse_resume(self, output_file = "resume.json"):
            # get file extension of resume file and convert to lowercase
            ext = os.path.splitext(self.filename)[1].lower()

            # create empty string
            text = ""

            # check if file is a docx 
            if ext == ".docx": 
                doc = Document(self.filename)

                # get all text from paragraphs and put them together
                text = " ".join(p.text for p in doc.paragraphs)
            
            # check if file is a pdf 
            elif ext == ".pdf": 
                if not PyPDF2: raise ImportError("PyPDF2 is required for PDFs!")

                # read pdf file 
                reader = PyPDF2.PdfReader(self.filename)

                # get all text from all pages and put them together
                text = " ".join(page.extract_text() for page in reader.pages) 

                # if file is not of supported file type
            else: raise ValueError("Unsupported file type!")

            # create dictionary to hold words 
            words = {}

            # loop for each word in text
            for word in text.split():

                # make the word lowercase and get rid of extra spaces
                word = word.lower().strip()

                # count each word
                if word: words[word] = words.get(word, 0) + 1
            
            # save the word counts to json file 
            with open(output_file, "w", encoding = "utf-8") as f: json.dump(words, f, indent = 4)

            # return dictionary of the count
            return words
    
parse = test("Alden Hilton Resume.docx")
word_counts = parse.parse_resume()
print(word_counts)