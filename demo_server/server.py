import datetime
import csv
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from io import StringIO
from urllib.parse import urlparse, parse_qs



STATS = [
    ('Campaign A', 10, 12.2),
    ('Campaign B', 7, 9.9),
    ('Campaign C', 14, 16.3),
]


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        query_components = parse_qs(urlparse(self.path).query, keep_blank_values=True)

        user_id = query_components['user_id'][0]
        date_from = datetime.date.fromisoformat(query_components['date_from'][0])
        date_to = datetime.date.fromisoformat(query_components['date_to'][0])

        # Create CSV content
        buff = StringIO()
        writer = csv.DictWriter(buff, fieldnames=['Date', 'User ID', 'Campaign', 'Clicks', 'Spend'])
        writer.writeheader()

        date = date_from
        while date <= date_to:
            campaign, clicks, spend = STATS[date.day % len(STATS)]

            writer.writerow({
                'Date': date.isoformat(),
                'User ID': user_id,
                'Campaign': campaign,
                'Clicks': clicks,
                'Spend': spend,
            })
            date += datetime.timedelta(days=1)

        buff.seek(0)

        # Send response headers
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.send_header('Content-Disposition', 'attachment; filename="stats.csv"')
        self.end_headers()

        # Send CSV content as response
        self.wfile.write(buff.read().encode('utf-8'))


def run():
    port = 8008

    httpd = HTTPServer(('', port), ServerHandler)
    print(f"Starting server on port {port}")

    httpd.serve_forever()


if __name__ == "__main__":
    run()
