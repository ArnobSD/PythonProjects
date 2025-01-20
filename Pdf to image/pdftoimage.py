import fitz  # PyMuPDF
import os
from tkinter import Tk, filedialog

def pdf_to_images():
    # Prompt the user to select a PDF file
    Tk().withdraw()  # Hide the root Tkinter window
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF File",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )

    if not pdf_path:
        print("No file selected. Exiting...")
        return

    # Create an output directory for images
    output_dir = os.path.splitext(pdf_path)[0] + "_images"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Iterate over each page
        for page_number in range(len(pdf_document)):
            print(f"Processing page {page_number + 1}...")
            page = pdf_document[page_number]

            # Render the page as an image
            pix = page.get_pixmap(dpi=300)  # High resolution for clarity
            output_file = os.path.join(output_dir, f"page_{page_number + 1}.png")

            # Save the image
            pix.save(output_file)
            print(f"Saved: {output_file}")

        print(f"All pages have been saved as images in: {output_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the conversion
if __name__ == "__main__":
    pdf_to_images()
