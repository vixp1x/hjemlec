from flask import Flask
from datetime import datetime, timedelta
import os
from lectio import Lectio

app = Flask(__name__)

# Configuration (set these as environment variables on Render)
LECTIO_SCHOOL_ID = int(os.getenv("LECTIO_SCHOOL_ID", "123"))  # Replace 123 if testing locally
LECTIO_USER = os.getenv("LECTIO_USER", "your_username")
LECTIO_PASS = os.getenv("LECTIO_PASS", "your_password")

def get_todays_schedule():
    lectio = Lectio(LECTIO_SCHOOL_ID)
    lectio.authenticate(LECTIO_USER, LECTIO_PASS)
    me = lectio.me()

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    schedule = me.get_schedule(start_date=today, end_date=tomorrow)

    if not schedule:
        return "No lessons today."

    lines = []
    for entry in schedule:
        start = entry.start.strftime("%H:%M")
        end = entry.end.strftime("%H:%M")
        subject = entry.subject_name or "Unknown"
        teacher = entry.teacher_name or ""
        room = entry.room_name or ""
        lines.append(f"{start}-{end}  {subject}  {teacher}  {room}")

    return "\n".join(lines)

@app.route("/")
def index():
    try:
        schedule_text = get_todays_schedule()
    except Exception as e:
        schedule_text = f"Error loading schedule: {e}"
    html = f"""
    <html>
      <head>
        <title>Lectio Schedule</title>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
      </head>
      <body>
        <pre>
{schedule_text}
        </pre>
      </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
