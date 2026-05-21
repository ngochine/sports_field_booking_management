from datetime import datetime, timedelta

DAY = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")
PAST= (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
NOW = datetime.now()

BOOKING_CASES = {
    "default_day": DAY,
    "past_date": PAST,
    "end_smaller_than_start": ("10:00", "08:00"),
    "empty_start_time": ("", NOW.strftime("%H:%M")),
    "empty_end_time": (NOW.strftime("%H:%M"), ""),
    "outside_business_hours": ("00:00", "06:00"),
    "duplicate_slot_index": 1,
    "valid_slot_index": 2,
    "booking_slot_index": 0,
    "start_smaller_than_current":(NOW.strftime("%Y-%m-%d"),(NOW - timedelta(hours=1)).strftime("%H:%M"),(NOW + timedelta(hours=1)).strftime("%H:%M")),
    "under_one_hour":(DAY,NOW.strftime("%H:%M"),(NOW + timedelta(hours=0.5)).strftime("%H:%M")),
    "invalid_time":("aa:00","-1:00")
}

CANCEL_CASE={
    "valid_user": ("user03", "Aa@123456"),
}