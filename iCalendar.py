import csv
from datetime import datetime
from pathlib import Path


# -----------------------------
# FILES
# -----------------------------
input_file = "output/CSV/september_menu_calendar.csv"
output_file = "output/iCalendar/VIT-AP_September_2026_Mess_Menu_IST.ics"

def escape_ical(text):
    """
    Escape characters that have special meaning in iCalendar.
    """
    if text is None:
        return ""

    text = str(text)

    return (
        text
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r", "")
        .replace("\n", "\\n")
    )


events = []

with open(input_file, "r", encoding="utf-8-sig", newline="") as f:

    reader = csv.DictReader(f)

    for row in reader:

        start_datetime = datetime.strptime(
            f"{row['Start Date']} {row['Start Time']}",
            "%Y-%m-%d %H:%M"
        )

        end_datetime = datetime.strptime(
            f"{row['End Date']} {row['End Time']}",
            "%Y-%m-%d %H:%M"
        )

        # Unique ID for Google Calendar
        uid = (
            f"{row['Subject'].replace(' ', '-')}"
            f"-{row['Start Date']}"
            f"@vit-ap-mess"
        )

        event = [
            "BEGIN:VEVENT",

            f"UID:{escape_ical(uid)}",

            # Timezone is explicitly India
            f"DTSTART;TZID=Asia/Kolkata:"
            f"{start_datetime.strftime('%Y%m%dT%H%M%S')}",

            f"DTEND;TZID=Asia/Kolkata:"
            f"{end_datetime.strftime('%Y%m%dT%H%M%S')}",

            f"SUMMARY:{escape_ical(row['Subject'])}",

            f"DESCRIPTION:{escape_ical(row['Description'])}",

            "STATUS:CONFIRMED",

            "END:VEVENT"
        ]

        events.extend(event)

calendar = [
    "BEGIN:VCALENDAR",

    "VERSION:2.0",

    "PRODID:-//VIT-AP//September 2026 Mess Menu//EN",

    "CALSCALE:GREGORIAN",

    "METHOD:PUBLISH",

    "X-WR-CALNAME:VIT-AP Mess Menu - September 2026",

    "X-WR-TIMEZONE:Asia/Kolkata",

    "BEGIN:VTIMEZONE",

    "TZID:Asia/Kolkata",

    "X-LIC-LOCATION:Asia/Kolkata",

    "BEGIN:STANDARD",

    "TZOFFSETFROM:+0530",

    "TZOFFSETTO:+0530",

    "TZNAME:IST",

    "DTSTART:19700101T000000",

    "END:STANDARD",

    "END:VTIMEZONE",
]

calendar.extend(events)


calendar.append("END:VCALENDAR")


Path(output_file).parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(output_file, "w", encoding="utf-8", newline="") as f:

    f.write("\r\n".join(calendar))
    f.write("\r\n")


print("ICS file created successfully!")
print(f"Output: {output_file}")
print(f"Total events: {len(events) // 7}")