import requests
import time
import misc_tools


def get_resources_by_type(resource_type):
    return get_resources_by_uri(f"https://www.speedrun.com/api/v1/{resource_type}?max=200")


def get_resources_by_uri(uri):
    get_more = True
    all_entries = []
    consecutive_errors = 0

    misc_tools.log(f"get resources by uri - {uri}", True)

    while get_more:
        response = requests.get(uri)

        if response.status_code == 200:
            consecutive_errors = 0
            json = response.json()
            data = json["data"]
            pagination = json["pagination"]

            all_entries += data

            log_str = f"{response.status_code} - ok ({len(data)} processed, {len(all_entries)} total)"
            sleep_time = 1

            links = pagination["links"]

            get_more = False

            for link in links:
                if link["rel"] == "next":
                    uri = link["uri"]
                    get_more = True

        elif response.status_code == 420:
            log_str = f"{response.status_code} - rate limited, waiting 1 minute..."
            sleep_time = 60

        else:
            consecutive_errors += 1
            log_str = f"{response.status_code} - unknown error (streak of {consecutive_errors}, waiting 10 seconds"
            sleep_time = 10

            if consecutive_errors == 3:
                get_more = False

        time.sleep(sleep_time)
        misc_tools.log(f"{log_str}", True)

    return all_entries
