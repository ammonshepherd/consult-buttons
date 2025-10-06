from gpiozero import Button
from signal import pause
import time
import gspread
from google.oauth2.service_account import Credentials

# --- Google Sheets Setup ---
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"

# Authorize Google Sheets client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# --- Button Setup ---
# Use the GPIO pin your button is connected to (BCM numbering)
button = Button(18, pull_up=True, bounce_time=0.2)

def send_to_sheets():
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data = [timestamp, "Button pressed!"]
        sheet.append_row(data)
        print(f"✅ Sent data: {data}")
    except Exception as e:
        print(f"⚠️ Failed to send data: {e}")

# Attach the function to the button press event
button.when_pressed = send_to_sheets

print("Waiting for button press... (Press Ctrl+C to exit)")
pause()  # Keeps the script running and listens for button events