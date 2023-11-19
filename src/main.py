import misc_tools
import src_tools
import numpy as np


def main():
    misc_tools.clear_log()

    # get the platforms to check
    desired_platforms_input = input("Enter the platform(s) you would like to pull from (comma to separate entries).\n")
    desired_platforms_list = desired_platforms_input.split(',')

    misc_tools.log("Getting platforms from SRC...", True)
    src_platforms = src_tools.get_resources_by_type("platforms")

    misc_tools.log("Done getting platforms from SRC", True)

    desired_platforms_corrected = {}
    platform_ids = []

    # get a list of the expected platforms by comparing those requested and those on speedrun.com
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

    # ask if it's ok to continue, end if not
    misc_tools.log("Given the input platforms, SRC returned these platforms as the closest matches:", True)
    for key, value in desired_platforms_corrected.items():
        misc_tools.log(f"{value} (from {key})", True)
    platforms_ok = input("Are you ok with your selections? 1 to continue, anything else to exit.\n")

    if platforms_ok != '1':
        return

    # check if emulators are necessary or not
    require_emulators = input("Does the game need to allow emulators? 1 for yes, anything else for no.\n")
    require_emulators = require_emulators == '1'

    # get a range of times
    misc_tools.log("Using the median run length as the metric, enter the min and max times you would like to check.", True)
    misc_tools.log("Valid formats - \"HH:MM:SS\", \"MM:SS\".", True)

    min_time_input = ""
    max_time_input = ""
    valid_min = False
    valid_max = False

    # ensure times submitted are valid (format and sensible)
    while not (valid_min and valid_max):
        min_time_input = input("Min time:\n")
        max_time_input = input("Max time:\n")
        valid_min = misc_tools.is_time_valid_format(min_time_input)
        valid_max = misc_tools.is_time_valid_format(max_time_input)

        if not valid_min:
            misc_tools.log("Invalid min time format", True)
        if not valid_max:
            misc_tools.log("Invalid max time format", True)

        if valid_min and valid_max:
            temp_min = misc_tools.get_seconds_from_formatted_time(min_time_input)
            temp_max = misc_tools.get_seconds_from_formatted_time(max_time_input)

            if temp_min >= temp_max:
                valid_min = False
                valid_max = False
                misc_tools.log("Min longer than max", True)

    min_time_seconds = misc_tools.get_seconds_from_formatted_time(min_time_input)
    max_time_seconds = misc_tools.get_seconds_from_formatted_time(max_time_input)

    final_list = []

    # see if there's a limit to the number of games/categories that should be returned
    valid_limit = False
    limit = float("inf")

    while not valid_limit:
        limit = input("How many categories do you want to limit your search to? Put a negative number to search all.\n")

        try:
            limit = int(limit)

            if limit < 0:
                limit = float("inf")

            valid_limit = True
        except ValueError:
            pass

        if not valid_limit:
            misc_tools.log("Invalid limit entered", True)

    misc_tools.log("Searching SRC for runs that fit the specified requirements...", True)

    # for every platform...
    for platform_id in platform_ids:
        uri = f"https://www.speedrun.com/api/v1/games?" \
              f"embed=categories&" \
              f"max=200&" \
              f"platform={platform_id}"

        # get its games
        games = src_tools.get_resources_by_uri(uri)

        filtered_games_list = games

        # if emulators required, filter out games that ban them
        if require_emulators:
            for game in games:
                if not game["ruleset"]["emulators-allowed"]:
                    filtered_games_list.remove(game)

        games = filtered_games_list

        # for every game...
        for game in games:
            misc_tools.log(f"Checking {game['names']['international']}", True)

            # get a list of its categories
            game_id = game["id"]
            categories_list = game["categories"]["data"]

            # for every category...
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

                    # get a list of its runs
                    runs = src_tools.get_resources_by_uri(uri)
                    run_times = []

                    # for every run...
                    for run in runs:
                        # add it to the list of all run times
                        run_times.append(run["times"]["primary_t"])

                    # if there are runs for the game
                    if len(run_times) > 0:
                        min_time = np.min(run_times)
                        max_time = np.max(run_times)
                        median_time = np.median(run_times)
                        average_time = np.mean(run_times)

                        # check if the median is within the range the user wants. if so, append it to the final list
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

                # break if the limit is reached
                if len(final_list) >= limit:
                    break

            if len(final_list) >= limit:
                break

        if len(final_list) >= limit:
            break

    # sort the final list by median run time
    final_list = sorted(final_list, key=lambda x: x[4])

    # print out the final list of games/categories and their run times! (assuming a non zero amount are found)
    if len(final_list) == 0:
        misc_tools.log("No games/categories given desired parameters", True)
    else:
        misc_tools.log(f"Found {len(final_list)} categories! Formatted as:", True)
        misc_tools.log("Game - Category | Fastest to Slowest | Median / Average", True)

    for entry in final_list:
        min_formatted = misc_tools.get_formatted_time_from_seconds(entry[2])
        max_formatted = misc_tools.get_formatted_time_from_seconds(entry[3])
        median_formatted = misc_tools.get_formatted_time_from_seconds(entry[4])
        average_formatted = misc_tools.get_formatted_time_from_seconds(entry[5])

        misc_tools.log(f"{entry[0]} - {entry[1]} | "
                       f"{min_formatted} to {max_formatted} | {median_formatted} / {average_formatted}",
                       True)


if __name__ == "__main__":
    main()
