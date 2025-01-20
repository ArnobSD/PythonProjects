from PIL import Image
from tkinter import Tk, filedialog

def images_to_pdf():
    # Prompt the user to select image files
    Tk().withdraw()  # Hide the root Tkinter window
    image_files = filedialog.askopenfilenames(
        title="Select Image Files",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All Files", "*.*")]
    )

    if not image_files:
        print("No images selected. Exiting...")
        return

    # Prompt the user to select a location to save the PDF
    output_pdf = filedialog.asksaveasfilename(
        title="Save PDF File",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not output_pdf:
        print("No output file specified. Exiting...")
        return

    try:
        # Open images and convert them to RGB mode
        image_list = []
        for image_file in image_files:
            img = Image.open(image_file)
            if img.mode != "RGB":
                img = img.convert("RGB")  # Convert to RGB mode if not already
            image_list.append(img)

        # Save images as a PDF
        first_image = image_list.pop(0)  # Use the first image as the base
        first_image.save(output_pdf, save_all=True, append_images=image_list)
        print(f"PDF created successfully: {output_pdf}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the conversion
if __name__ == "__main__":
    images_to_pdf()
