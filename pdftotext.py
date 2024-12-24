import PyPDF2

def pdf_to_text(pdf_path, output_txt):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_path = 'resume.pdf'

    output_txt = 'output.txt'

    pdf_to_text(pdf_path, output_txt)

    print("PDF converted to text successfully!")