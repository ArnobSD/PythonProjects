import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from tkinter import Tk, filedialog

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf():
    # Prompt the user to select a PDF file
    Tk().withdraw()  # Hide the root Tkinter window
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF File",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )

    if not pdf_path:
        print("No file selected. Exiting...")
        return

    # Output text file path
    output_text_file = pdf_path.replace(".pdf", "_output.txt")

    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Prepare the output text file
        with open(output_text_file, "w", encoding="utf-8") as output_file:
            # Iterate over each page in the PDF
            for page_number in range(len(pdf_document)):
                print(f"Processing page {page_number + 1}...")
                page = pdf_document[page_number]

                # Render the page as an image
                pix = page.get_pixmap(dpi=300)  # High resolution
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Perform OCR on the image
                text = pytesseract.image_to_string(image, config='--oem 1 --psm 4')  # Preserve layout

                # Write text to the output file
                output_file.write(f"--- Page {page_number + 1} ---\n")
                output_file.write(text)
                output_file.write("\n\n")

        print(f"Text extracted and saved to {output_text_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the extraction
if __name__ == "__main__":
    extract_text_from_pdf()
