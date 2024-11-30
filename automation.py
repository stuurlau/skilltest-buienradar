'''
Automation approach:

Run a cron job on a server, (some cloud vm?).
As script we could reuse fetch data code form database.py.

cron job to fetch data every 20 minutes:
0,20,40 * * * * /path/to/python3 /path/to/automation.py

Drawbacks:
- No checks for duplicated data
    - if something goes wrong, and we restart the instance for example, we could end up with duplicated data

'''

from database import fetch_measurement_data, fetch_stations,engine

if __name__ == "__main__":
    fetch_stations()
    fetch_measurement_data()