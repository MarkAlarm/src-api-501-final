import misc_tools
import src_tools
import numpy as np


def main():
    misc_tools.clear_log()

    desired_platforms_input = input("Enter the platform(s) you would like to pull from (comma to separate entries).\n")
    desired_platforms_list = desired_platforms_input.split(',')

    misc_tools.log("Getting platforms from SRC...", True)
    src_platforms = src_tools.get_resources_by_type("platforms")

    misc_tools.log("Done getting platforms from SRC", True)

    desired_platforms_corrected = {}
    platform_ids = []

    for desired_platform in desired_platforms_list:
        best_similarity = float("-inf")
        closest_platform_name = ""
        closest_platform_id = ""

        for src_platform in src_platforms:
            src_platform_name = src_platform["name"]
            src_platform_id = src_platform["id"]
            src_platform_similarity = misc_tools.jaccard_similarity(desired_platform, src_platform_name)

            if src_platform_similarity > best_similarity:
                best_similarity = src_platform_similarity
                closest_platform_name = src_platform_name
                closest_platform_id = src_platform_id

        desired_platforms_corrected[desired_platform] = closest_platform_name
        platform_ids.append(closest_platform_id)

    misc_tools.log("Given the input platforms, SRC returned these platforms as the closest matches:", True)
    for key, value in desired_platforms_corrected.items():
        misc_tools.log(f"{value} (from {key})", True)
    platforms_ok = input("Are you ok with your selections? 1 to continue, anything else to exit.\n")

    if platforms_ok != '1':
        return

    require_emulators = input("Does the game need to allow emulators? 1 for yes, anything else for no.\n")
    require_emulators = require_emulators == '1'

    misc_tools.log("Using the median run length as the metric, enter the min and max times you would like to check.", True)
    misc_tools.log("Valid formats - \"HH:MM:SS\", \"MM:SS\".", True)

    min_time_input = ""
    max_time_input = ""
    valid_min = False
    valid_max = False
    while not (valid_min and valid_max):
        min_time_input = input("Min time:\n")
        max_time_input = input("Max time:\n")
        valid_min = misc_tools.is_time_valid_format(min_time_input)
        valid_max = misc_tools.is_time_valid_format(max_time_input)
        if not valid_min:
            misc_tools.log("Invalid min time format", True)
        if not valid_max:
            misc_tools.log("Invalid max time format", True)

    min_time_seconds = misc_tools.get_seconds_from_formatted_time(min_time_input)
    max_time_seconds = misc_tools.get_seconds_from_formatted_time(max_time_input)

    final_list = []

    misc_tools.log("Searching SRC for runs that fit the specified requirements...", True)

    for platform_id in platform_ids:
        uri = f"https://www.speedrun.com/api/v1/games?" \
              f"embed=categories&" \
              f"max=200&" \
              f"platform={platform_id}"

        games = src_tools.get_resources_by_uri(uri)

        filtered_games_list = games

        if require_emulators:
            for game in games:
                if not game["ruleset"]["emulators-allowed"]:
                    filtered_games_list.remove(game)

        games = filtered_games_list

        for game in games:
            misc_tools.log(f"Checking {game['names']['international']}", True)

            game_id = game["id"]
            categories_list = game["categories"]["data"]

            for category in categories_list:
                if category["type"] == "per-game":
                    category_id = category["id"]

                    misc_tools.log(f"Checking {game['names']['international']} - {category['name']}", True)

                    uri = f"https://www.speedrun.com/api/v1/runs?" \
                          f"game={game_id}&" \
                          f"category={category_id}&" \
                          f"platform={platform_id}&" \
                          f"status=verified&" \
                          f"max=200"

                    runs = src_tools.get_resources_by_uri(uri)
                    run_times = []
                    for run in runs:
                        run_times.append(run["times"]["primary_t"])

                    if len(run_times) > 0:
                        min_time = np.min(run_times)
                        max_time = np.max(run_times)
                        median_time = np.median(run_times)
                        average_time = np.mean(run_times)

                        if min_time_seconds <= median_time < max_time_seconds:
                            final_list.append((
                                game["names"]["international"],
                                category["name"],
                                min_time,
                                max_time,
                                median_time,
                                average_time,
                                len(run_times)
                            ))

    final_list = sorted(final_list, key=lambda x: x[4])

    if len(final_list) == 0:
        print("No games/categories given desired parameters")

    for entry in final_list:
        min_formatted = misc_tools.get_formatted_time_from_seconds(entry[2])
        max_formatted = misc_tools.get_formatted_time_from_seconds(entry[3])
        median_formatted = misc_tools.get_formatted_time_from_seconds(entry[4])
        average_formatted = misc_tools.get_formatted_time_from_seconds(entry[5])

        print(f"{entry[0]} - {entry[1]} | "
              f"{min_formatted} to {max_formatted} | {median_formatted} / {average_formatted}")


if __name__ == "__main__":
    main()
