
# QR Code Generator with Optional Logo

This Python script generates high-quality QR codes with an optional logo in the center. It can be run from the terminal with customizable input parameters.

## Features

- **High-resolution QR codes**: Suitable for printing and professional use.
- **Optional logo**: Place a logo in the center of the QR code.
- **Command-line usage**: Easily specify the QR code data, output file name, and optional logo file.

## Prerequisites

Ensure you have Python 3.x installed on your system and the following Python libraries:

- `qrcode`
- `Pillow` (PIL)

Install the dependencies using pip:

```bash
pip install qrcode[pil] Pillow
```

## Usage

Run the script from the terminal with the following arguments:

```bash
python .py <data-for-qr-code> <output-file-name> [logo-file-name]
```

### Arguments:
- `<data-for-qr-code>` (required): The text, URL, or data to encode in the QR code.
- `<output-file-name>` (required): The name of the output PNG file.
- `[logo-file-name]` (optional): The path to the logo file to embed in the QR code.

### Examples:

**Generate a QR code without a logo:**

```bash
python qrCodeGenerator.py "https://www.example.com" qr_code.png
```

**Generate a QR code with a logo:**

```bash
python qrCodeGenerator.py "https://www.example.com" qr_code_with_logo.png logo.png
```

## Output

The script saves the generated QR code as a PNG file at the specified location. The output image is high resolution (600 DPI), making it suitable for professional use.

## Error Handling

If the specified logo file cannot be loaded, the script will print an error message and proceed to generate the QR code without the logo.

## File Structure

```
.
├── qrCodeGenerator.py   # The QR code generator script
└── README.md        # This README file
```

## Contribution

Feel free to submit issues or pull requests to improve this script. Contributions are always welcome!

## License

This project is licensed under the MIT License.

## Acknowledgments

- `qrcode` library for QR code generation.
- `Pillow` (PIL) library for image processing.
