import qrcode
from PIL import Image
import sys


def create_qr_code(data, output_file, logo_file=None):
    """
    Generate a high-quality QR code with an optional logo.
    :param data: Data for the QR code
    :param output_file: Output file name
    :param logo_file: Optional logo file path
    """
    # Create QR code instance with high resolution
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=30,  # Increase the size of each box for high resolution
        border=4,  # Thickness of the border (minimum is 4)
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create a QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # If a logo file is provided, add it to the QR code
    if logo_file:
        try:
            logo = Image.open(logo_file).convert("RGBA")
            qr_width, qr_height = qr_img.size

            # Resize the logo proportionally for higher resolution
            max_logo_width = qr_width // 4
            max_logo_height = qr_height // 4
            logo_ratio = logo.width / logo.height
            if logo.width > logo.height:
                logo_width = max_logo_width
                logo_height = int(max_logo_width / logo_ratio)
            else:
                logo_height = max_logo_height
                logo_width = int(max_logo_height * logo_ratio)

            logo = logo.resize((logo_width, logo_height), Image.ANTIALIAS)

            # Get dimensions for centering the logo
            logo_x = (qr_width - logo_width) // 2
            logo_y = (qr_height - logo_height) // 2

            # Paste the logo onto the QR code
            qr_img.paste(logo, (logo_x, logo_y), mask=logo)
        except Exception as e:
            print(f"Error adding logo to QR code: {e}. Proceeding without logo.")

    # Save the high-quality QR code image
    qr_img.save(output_file, format="PNG", dpi=(600, 600))  # Set DPI for print quality
    print(f"High-quality QR code generated and saved as '{output_file}'.")


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <data-for-qr-code> <output-file-name> [logo-file-name]")
        sys.exit(1)
        
    data = sys.argv[1]
    output_file = sys.argv[2]
    logo_file = sys.argv[3] if len(sys.argv) > 3 else None

    # Generate the QR code
    create_qr_code(data, output_file, logo_file)
