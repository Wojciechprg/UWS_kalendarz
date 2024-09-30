import requests
import calendar
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "https://rekrutacja.teamwsuws.pl"

API_KEY = "7548b171b023fd49512c016f3a10429f"


def get_events_for_month(year, month, selected_tags=[]):
    """
    Fetches events for a given month and filters them by selected tags (if provided).

    Args:
        year (int): The year of the events to fetch.
        month (int): The month of the events to fetch.
        selected_tags (list): A list of tags to filter events (optional).

    Returns:
        list: A list of events for the specified month, filtered by tags if provided.
    """
    headers = {'api-key': API_KEY}

    if selected_tags:
        tags_query = '&'.join([f'tag={tag}' for tag in selected_tags])
        url = f"{BASE_URL}/events/filter/?{tags_query}"
    else:
        url = f"{BASE_URL}/events/"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events = response.json()
        filtered_events = [
            event for event in events
            if datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S').year == year
               and datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S').month == month
        ]
        return filtered_events
    else:
        return []


@app.route('/event-details/<int:event_id>')
def get_event_details(event_id):
    """
    Fetches detailed information about a specific event by its ID.

    Args:
        event_id (int): The ID of the event to fetch.

    Returns:
        dict: A dictionary with event details if found, or an error message.
    """
    url = f"{BASE_URL}/events/{event_id}"
    headers = {'api-key': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Event not found"}, 404


def get_tags():
    """
    Fetches all available tags from the events API.

    Returns:
        list: A list of unique tag names used in events.
    """
    url = f"{BASE_URL}/events/"
    headers = {'api-key': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events = response.json()
        tags = {tag['name'] for event in events for tag in event['tags']}
        return list(tags)
    else:
        return []


def generate_calendar(events, year, month):
    """
    Generates the calendar structure with events for a given month.

    Args:
        events (list): A list of events for the month.
        year (int): The year of the events.
        month (int): The month of the events.

    Returns:
        list: A nested list representing the calendar weeks and their events.
    """
    cal = calendar.Calendar(firstweekday=6)
    weeks = []
    for week in cal.monthdayscalendar(year, month):
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({"day": "", "events": []})
            else:
                day_events = [
                    event for event in events
                    if datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S').day == day
                       and datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S').month == month
                       and datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S').year == year
                ]
                week_data.append({"day": day, "events": day_events})
        weeks.append(week_data)

    return weeks


@app.route('/')
def calendar_view():
    """
    Renders the calendar view with events for the current or selected month.

    Retrieves events, filters them by selected tags if any, and prepares the calendar.

    Returns:
        Rendered HTML template for the calendar view.
    """
    year = request.args.get('year', default=datetime.today().year, type=int)
    month = request.args.get('month', default=datetime.today().month, type=int)

    selected_tags = request.args.getlist('tags')

    if selected_tags:
        events = get_events_for_month(year,month,selected_tags)
    else:
        events = get_events_for_month(year, month)

    all_tags = get_tags()

    calendar_weeks = generate_calendar(events, year, month)

    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1

    return render_template(
        'calendar.html',
        calendar_weeks=calendar_weeks,
        year=year, month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        base_url=BASE_URL,
        all_tags=all_tags,
        selected_tags=selected_tags
    )


if __name__ == '__main__':
    app.run(debug=True)
