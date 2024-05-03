import json
import os
import ocrmypdf
import PyPDF2
import extract_keyword_reg

def ocr_pdf(input_path, output_path):
    ocrmypdf.ocr(input_path, output_path, force_ocr= True, max_image_mpixels=3000, tesseract_downsample_large_images=True)

def batch_ocr_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"Processing {filename}")

            ocr_pdf(input_path, output_path)

            print(f"Processed {filename}")


def extract_first_page(input_pdf, output_pdf):
    with open(input_pdf, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)

        if len(reader.pages) > 0:
            writer = PyPDF2.PdfWriter()
            first_page = reader.pages[0]
            writer.add_page(first_page)

            with open(output_pdf, 'wb') as outfile:
                writer.write(outfile)
        else:
            print(f"No pages found in {input_pdf}")

def batch_extract_first_pages(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"first_page_of_{filename}")
            extract_first_page(input_path, output_path)
            print(f"First page of {filename} extracted to {output_path}")

def convert_pdf_to_txt(input_dir, output_dir):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_dir, filename)
            output_txt_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.json')
            with open(input_pdf_path, 'rb') as file, open(output_txt_path, 'w') as out_file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        keyword = extract_keyword_reg.extract_keywords_reg(text, path=input_pdf_path)
                        data = {"jsonFile": text, "keyword": keyword}
                        json.dump(data, out_file, indent=4)
                        # out_file.write(text + "\n")


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

def main():
    input_directory = 'pdf_downloads/AllMajorKeywords'
    output_directory = 'pdf_downloads/processed_first_page'
    batch_extract_first_pages(input_directory, output_directory)
    batch_ocr_pdfs(input_dir, output_dir)
    convert_pdf_to_txt(output_directory, text_directory)


if __name__ == "__main__":
    main()


