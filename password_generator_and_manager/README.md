
# Password Manager

## Description

The Password Manager is a GUI-based application built using Python and Tkinter. It allows users to generate, store, and manage passwords securely. Users can add passwords associated with specific websites, search for saved passwords, and generate new ones based on user-defined requirements.

### Features:
- Generate strong, random passwords based on user-defined criteria (lowercase, uppercase, digits, symbols).
- Add website login credentials (website, email/username, and password) to a local JSON file.
- Search for and copy a password associated with a specific website to the clipboard.
- Handle custom password requirements such as the number of lowercase, uppercase, digits, and symbols.
- Simple, user-friendly graphical interface using Tkinter.

---

## Requirements

- Python 3.x
- Tkinter
- PIL (Python Imaging Library)
- pyperclip (for clipboard functionality)

### Installing dependencies:

To install the required dependencies, run the following:

```bash
pip install pillow pyperclip
```

---

## Usage

### Starting the Application:

1. Clone or download the script.
2. Navigate to the folder containing the script and run it using the following command:

```bash
python main.py
```

This will open the main window for the password manager.

### Main Functionality:

- **Generate Password**: 
  - Click the "Generate Password" button to create a random password based on your preferences (lowercase, uppercase, digits, symbols).
  
- **Add Password**: 
  - Fill in the "Website", "Email/Username", and "Password" fields, then click the "Add Password" button to save your entry.
  
- **Search Password**: 
  - Enter a website name in the "Website" field and click the "Search" button. If the entry exists in the database, the associated username and password will be copied to the clipboard and shown in a message box.

- **Set Custom Requirements**: 
  - Click the "Requirements" button to adjust how many lowercase letters, uppercase letters, digits, and symbols are included in the generated password.

- **Exit**: 
  - Click the "Exit" button to close the application. If a password has been generated, it will be saved automatically.

---

## File Storage

- Password data is stored in a local JSON file called `password_manager_log.json`. This file is created automatically when the application is run for the first time.
- Each entry consists of the website name, username/email, password, and the date the entry was logged.

---

## Error Handling

- If the JSON file does not exist or is empty, the application will handle errors gracefully by prompting the user to add their first entry.
- The application validates the URL and email/username inputs to ensure they are in the correct format before generating or saving a password.

---

## License

This script is open-source and distributed under the MIT License.

---

## Contributing

Contributions are welcome! Feel free to fork the repository, open issues, and submit pull requests. Please follow standard Python coding conventions and ensure your changes are well-tested.

---

## Contact

For any questions or feedback, please contact a.n.chasovskoy@gmail.com
