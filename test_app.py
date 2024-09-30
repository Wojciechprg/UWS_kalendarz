import unittest
from app import app


class CalendarAppTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        # Test the home page loads correctly
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Use the correct byte sequence for 'Kalendarz wydarzeń'
        self.assertIn(b'Kalendarz wydarze\xc5\x84', response.data)

    def test_event_details(self):
        # Test fetching details for an event
        response = self.client.get('/event-details/5')
        self.assertEqual(response.status_code, 200)
        # Check if the response contains 'name' in the JSON output
        self.assertIn(b'name', response.data)

    def test_filter_events(self):
        # Test filtering events by tags
        response = self.client.get('/?tags=Music')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Music', response.data)


if __name__ == '__main__':
    unittest.main()
