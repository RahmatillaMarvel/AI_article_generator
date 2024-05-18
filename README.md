# AI Article Generator

## Overview

The AI Article Generator is a Python application built with PyQt5, allowing users to register, log in, and generate scientific articles based on their provided code snippets. It employs an AI model to produce articles structured with abstracts, introductions, main paragraphs, and conclusions.

## Requirements

Ensure you have Python 3.x installed on your system. You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

The dependencies include:

- PyQt5
- requests
- deep-translator
- markdown
- langdetect
- fpdf

## Usage

To launch the application, run the following command:

```bash
python main.py
```

Upon startup, the application presents a registration/login interface. New users can register, while existing users can log in. Once logged in, users can input their code snippets to generate scientific articles.

## Project Structure

- `main.py`: Contains the main application logic, GUI setup, and page navigation.
- `src/`: Directory containing source code files.
  - `registration.py`: Handles the registration page functionality.
  - `mainpage.py`: Implements the main page for article generation.
- `data/`: Directory storing application data.
  - `in_login.txt`: Indicates user login status (1 for logged in, 0 for not logged in).
- `gemini_pro.py`: Module for interacting with the AI model to generate article content.

## Contribution

Contributions to the project are welcomed. If you encounter any issues or have suggestions for enhancements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.
