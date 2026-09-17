"""Keep the Monday writer and Tuesday reviewer on the same fortnight."""

import os
from datetime import date, datetime, timezone

FIRST_WRITE_DATE = date(2026, 9, 21)  # Monday; review follows on Tuesday.


def should_run(today, event_name):
    if event_name == "workflow_dispatch":
        return True
    weeks = (today - FIRST_WRITE_DATE).days // 7
    return event_name == "schedule" and weeks >= 0 and weeks % 2 == 0


if __name__ == "__main__":
    run = should_run(datetime.now(timezone.utc).date(), os.environ["GITHUB_EVENT_NAME"])
    print(f"run={str(run).lower()}")
