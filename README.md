# WhatsApp Message Sender

A professional desktop application to automate sending WhatsApp messages to multiple participants and an instructor using a clean, user-friendly interface. Built with Python, Tkinter, and `pywhatkit`, this app provides robust logging, validation, and real-time progress tracking.

## Features

- **Bulk WhatsApp Messaging:** Send personalized messages to multiple participants and an instructor with ease.
- **User-Friendly GUI:** Simple and intuitive interface using Tkinter.
- **Phone Number Validation:** Ensures numbers are in the correct format before sending.
- **Progress Tracking:** Real-time progress bar and status updates for message sending.
- **Operation Control:** Ability to stop the sending process at any time.
- **Result Logging:** Saves detailed logs of send results in a `logs/` directory for auditing and troubleshooting.

## Prerequisites

- Python 3.7+
- Google Chrome browser (used by `pywhatkit` for WhatsApp Web)
- WhatsApp account logged in to WhatsApp Web

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/phlzas/message-sender.git
    cd message-sender
    ```

2. **Install dependencies:**
    ```bash
    pip install pywhatkit
    ```

## Usage

1. **Run the application:**
    ```bash
    python main.py
    ```

2. **Fill in the fields:**
    - **Participants:** Comma-separated list of phone numbers (must start with `+`, e.g., `+1234567890`).
    - **Instructor:** (Optional) A phone number for the instructor.
    - **Message for Participants:** The message text to send to all participants.
    - **Message for Instructor:** The message text to send to the instructor.

3. **Click "Send Messages":**
    - Watch the progress bar as messages are sent.
    - You can stop the process at any time using the "Stop" button.

4. **Logs:**
    - After completion, a log file with send results is saved to the `logs/` directory.

## Troubleshooting

- **Invalid phone numbers:** Make sure all numbers start with a `+` followed by the country code and number.
- **pywhatkit errors:** Ensure Google Chrome is installed and you are logged into WhatsApp Web before sending messages.
- **Permissions:** The app writes logs to `logs/` in the current directory; ensure you have write permissions.

## Disclaimer

This application automates sending messages via WhatsApp Web. Use responsibly and do not spam users.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

- [phlzas](https://github.com/phlzas)

