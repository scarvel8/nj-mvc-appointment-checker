Get a REAL ID appointment for personal use. Do not use for abuse.

# njmvcappointmentchecker

This project is designed to check for available appointments at specified locations and send email notifications if appointments are found before a specified cutoff date. It utilizes Playwright for web automation and SMTP for sending emails.

## Project Structure

```
njmvcappointmentchecker
├── src
│   ├── mvcappointmentchecker.py  # Main logic for checking appointments and sending notifications
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd njmvcappointmentchecker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your email configuration in `src/mvcappointmentchecker.py`:
   - Update `EMAIL_ADDRESS` and `EMAIL_PASSWORD` with your email credentials.
   - Modify `RECIPIENTS` to include the email addresses you want to notify.

## Usage

To run the application, execute the following command:
```
python src/mvcappointmentchecker.py
```

The script will check for available appointments at the specified locations and send email notifications if any appointments are found before the cutoff date.

## Dependencies

- `playwright`: For web automation.
- `smtplib`: For sending emails.
- `email.mime`: For constructing email messages.

## Notes

- You may need to install Playwright browsers by running:
  ```
  playwright install
  ```
