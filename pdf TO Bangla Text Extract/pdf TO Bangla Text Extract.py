import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os

def extract_images_from_pdf(pdf_path, image_folder="pdf_images"):
    """Extract all images from a PDF and save them in a folder."""
    os.makedirs(image_folder, exist_ok=True)
    pdf_document = fitz.open(pdf_path)
    image_paths = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(image_folder, f"page_{page_number+1}_img_{img_index+1}.{image_ext}")

            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            image_paths.append(image_filename)

    pdf_document.close()
    print(f"Extracted {len(image_paths)} images to {image_folder}")
    return image_paths

def extract_bangla_text_from_images(image_paths, output_text_file="bangla_text.txt"):
    """Extract Bangla text from images using Tesseract OCR."""
    # Configure Tesseract to use the Bangla language
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this for your system
    tesseract_config = "--psm 6 -l ben"  # 'ben' is the language code for Bangla

    with open(output_text_file, "w", encoding="utf-8") as text_file:
        for image_path in image_paths:
            try:
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, config=tesseract_config)
                text_file.write(f"--- Text from {image_path} ---\n")
                text_file.write(text + "\n\n")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    print(f"Bangla text extracted to {output_text_file}")

if __name__ == "__main__":
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    # Ask the user for the PDF file
    print("Select a PDF file:")
    Tk().withdraw()  # Hide the root tkinter window
    pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if pdf_path:
        # Extract images from the PDF
        image_folder = "pdf_images"
        image_paths = extract_images_from_pdf(pdf_path, image_folder=image_folder)

        # Extract Bangla text from images
        output_text_file = "bangla_text.txt"
        extract_bangla_text_from_images(image_paths, output_text_file=output_text_file)

        print(f"Process completed! Text saved in: {output_text_file}")
    else:
        print("No file selected.")
