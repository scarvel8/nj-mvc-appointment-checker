import asyncio
from playwright.async_api import async_playwright
from datetime import datetime  # Ensure datetime is imported
import smtplib
from email.mime.text import MIMEText
import json

# Email config
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_ADDRESS = 'email@email.com'
EMAIL_PASSWORD = ''
RECIPIENTS = ['someemail@someemail.com']

# Locations and cutoff
TARGET_LOCATIONS = ['Edison']
CUTOFF_DATE = datetime(2025, 10, 10)

# Add the toggle flag
SEND_EMAIL_ALWAYS = False  # Set to True to send email even if no appointments are found before the cutoff date

async def send_email(subject, body):
    # Add the current time to the email body
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    body += f"\n\nEmail sent at: {current_time}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENTS)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENTS, msg.as_string())

async def check_appointments():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://telegov.njportal.com/njmvc/AppointmentWizard/11")

        # Extract locationData and timeData from the page's JavaScript context
        location_data = await page.evaluate("locationData")
        time_data = await page.evaluate("timeData")

        # Filter locations based on TARGET_LOCATIONS
        filtered_locations = [loc for loc in location_data if loc['Name'].split(' - ')[0] in TARGET_LOCATIONS]

        found_appointments = False

        for location in filtered_locations:
            location_name = location['Name']
            location_id = location['LocAppointments'][0]['LocationId']

            # Find the corresponding time data for the location
            time_info = next((time for time in time_data if time['LocationId'] == location_id), None)
            if not time_info:
                print(f"  ❌ No time data available for {location_name}")
                continue

            # Extract the first available appointment date
            first_open_slot = time_info['FirstOpenSlot']
            print(f"  📅 Found time slot for {location_name}: {first_open_slot}")

            # Parse the date and check against the cutoff
            try:
                appointment_date_str = first_open_slot.split("Next Available: ")[1].strip()
                appointment_date = datetime.strptime(appointment_date_str, "%m/%d/%Y %I:%M %p")
                if appointment_date < CUTOFF_DATE:
                    found_appointments = True
                    print(f"  ✅ Appointment found before {CUTOFF_DATE.strftime('%m/%d/%Y')} at {location_name} on {appointment_date.strftime('%m/%d/%Y %I:%M %p')}")
                    subject = f"Appointment Available at {location_name}"
                    body = f"An appointment is available at {location_name} on {appointment_date.strftime('%m/%d/%Y %I:%M %p')}."
                    await send_email(subject, body)
                else:
                    print(f"  ❌ No appointments before {CUTOFF_DATE.strftime('%m/%d/%Y')} at {location_name}")
            except (IndexError, ValueError):
                print(f"  ⚠️ Invalid time slot format for {location_name}: {first_open_slot}")
                continue

        if SEND_EMAIL_ALWAYS and not found_appointments:
            subject = "No Appointments Found"
            body = f"No NJ MVC appointments were found before {CUTOFF_DATE.strftime('%m/%d/%Y')} for the selected locations."
            await send_email(subject, body)

        await browser.close()

# Run it
asyncio.run(check_appointments())
