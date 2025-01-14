import qrcode
import pandas as pd
import os
from re import sub
from urllib.parse import quote
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_filename(name):
    """Replace invalid characters in file names with underscores."""
    return sub(r'[^\w\-_. ]', '_', name).strip()

def create_contact_qr_code(vcard_data, output_file):
    """Generate a QR code from vCard data and save it."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=3,
            border=2,
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img.save(output_file, format="PNG")
        logging.info(f"QR code saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error creating QR code: {e}")


def generate_vcard(row):
    """Create vCard data from a row of contact information, now using vCard 4.0 and including middle name."""
    try:
        last_name = row.get("Last Name", "").strip()
        first_name = row.get("First Name", "").strip()
        middle_name = row.get("Middle Name", "").strip()
        email_list = [e.strip() for e in row.get("EMAIL", "").split(',') if e.strip()]
        phone_list = [p.strip() for p in row.get("TEL", "").split(',') if p.strip()]
        org = row.get("ORG", "").strip()
        title = row.get("TITLE", "").strip()
        address = row.get("ADR", "").strip()
        website = row.get("URL", "").strip()

        # Construct full name, handling missing parts.
        name_parts = [part for part in [first_name, middle_name, last_name] if part]
        full_name = " ".join(name_parts).strip() if name_parts else "Unknown"

        # Construct given_name
        given_name_parts = [part for part in [first_name, middle_name] if part]
        given_name = " ".join(given_name_parts).strip() if given_name_parts else "Unknown"

        vcard = f"""BEGIN:VCARD
VERSION:4.0
N:{last_name};{given_name};;;
FN:{full_name}
"""
        if org:
            vcard += f"ORG:{org}\n"
        if title:
            vcard += f"TITLE:{title}\n"
        for phone in phone_list:
            vcard += f"TEL;TYPE=WORK,VOICE:{phone}\n"
        for email in email_list:
            vcard += f"EMAIL;TYPE=WORK:{email}\n"
        if website:
            vcard += f"URL:{quote(website)}\n"
        if address:
            vcard += f"ADR;TYPE=WORK:;;{address}\n"

        vcard += "END:VCARD"
        return vcard
    except Exception as e:
        logging.error(f"Error generating vCard data: {e}")
        return None
def process_excel(file_path, output_dir):
    """Process an Excel sheet to generate QR codes for all contacts."""
    try:
        data = pd.read_excel(file_path)
        logging.info("Excel file loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load Excel file: {e}")
        return

    os.makedirs(output_dir, exist_ok=True)

    for index, row in data.iterrows():
      try:
        logging.info(f"Processing row {index}: {row.to_dict()}")
        vcard_data = generate_vcard(row)
        if vcard_data:
            # Get names
            last_name = row.get("Last Name", "").strip()
            first_name = row.get("First Name", "").strip()

            if not last_name and not first_name:
              file_name = "unknown"
            elif not last_name:
              file_name = first_name
            elif not first_name:
              file_name = last_name
            else:
              file_name = f"{first_name}_{last_name}"

            output_file = os.path.join(output_dir, f"{sanitize_filename(file_name)}_QR.png")
            create_contact_qr_code(vcard_data, output_file)
      except Exception as e:
        logging.error(f"Error processing row {index}: {e}")


if __name__ == "__main__":
    excel_file = "./data_for_qr_codes.xlsx"
    output_directory = "qr_codes"
    process_excel(excel_file, output_directory)