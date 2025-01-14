# vCard QR Code Generator

This Python script generates QR codes containing vCard (Virtual Contact File) data from an Excel spreadsheet. The generated QR codes can be used to quickly share contact information by scanning them with a smartphone or other QR code reader.

## Features

- **Reads contact data from Excel:** The script takes an Excel file as input, reading contact information from its columns.
- **Generates vCard data:** It creates vCard formatted contact data using the provided fields, ensuring cross-platform compatibility.
- **QR Code Creation:** The script creates QR code images from the vCard data, using specific parameters to optimize for a smaller size.
- **Professional Use:** It handles names with middle names and provides the full name in the correct format, especially for Android compatibility.
- **Logging:** The script provides detailed output of the process, displaying errors and successes.
- **Multiple Email/Phone Numbers:** The script supports multiple entries for emails and phone numbers.

## Setup

### Prerequisites

Before running the script, ensure you have the following installed:

- **Python 3.6 or higher**
- **Required Python Libraries:**
  - `qrcode`: For generating QR codes
  - `pandas`: For working with Excel files
  - `openpyxl`: For reading Excel files

Install the required libraries using `pip`:

```bash
pip install qrcode pandas openpyxl
```

### Excel File Preparation

Ensure your Excel file meets these requirements:

- **Column Headers:** The Excel file should contain the following headers (or similar):
  - `Last Name`
  - `First Name`
  - `Middle Name`
  - `EMAIL` (comma-separated multiple entries are supported)
  - `TEL` (comma-separated multiple entries are supported)
  - `ORG` (Organization name)
  - `TITLE` (Job title)
  - `ADR` (Address)
  - `URL` (Website URL)

- **File Name:** Save your Excel file as `data_for_qr_codes.xlsx` (or update the `excel_file` variable in the script).

## Usage

1. **Clone or Download:** Clone or download this repository to your local machine.
2. **Place Excel File:** Ensure your `data_for_qr_codes.xlsx` file is in the same directory as the script.
3. **Run the Script:** Execute the script using the command:

```bash
python your_script_name.py
```

4. **Output:** The script will create a directory named `qr_codes` in the same directory as the script. Inside this folder, it will save PNG images of the QR codes. Each file name corresponds to the first and last name of the contact data, with a suffix `_QR`.

## Script Configuration

- **Output Directory:** The QR codes are saved to a folder called `qr_codes`.
- **Excel File Path:** The script reads data from `data_for_qr_codes.xlsx` by default. You can change the `excel_file` variable in the `if __name__ == "__main__":` section to use another Excel file.

## Testing

After generating QR codes, test them thoroughly:

- **Mobile Devices:** Scan the QR codes using the camera or a QR code reader application on Android and iOS devices.
- **Contact Saving:** Verify that all contact information (name, phone numbers, emails, organization, website, etc.) is accurately populated and saved into your device's contact list.

## Troubleshooting

- **Excel File Errors:** If the script fails to load the Excel file, verify the path and ensure the file exists. Ensure column headers in Excel match those expected by the script.
- **QR Code Not Scanning:** If a QR code fails to scan:
  - Try a different QR code reader.
  - Re-generate the QR code with adjustments to the `box_size` or error correction level in the `create_contact_qr_code` function.
- **Incorrect Data:** Check that the input data in Excel is formatted correctly. Special characters or improper formatting may cause issues.

## Contributing

Contributions are welcome! Feel free to create issues for bugs or submit pull requests for enhancements.

## License

This project is licensed under the [MIT License](LICENSE).
