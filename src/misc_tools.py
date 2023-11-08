import pickle

log_filename = "../data/log.txt"


def clear_log():
    with open(log_filename, 'w') as file:
        pass


def log(string, do_print):
    if do_print:
        print(string)

    with open(log_filename, 'a', encoding="utf-8") as file:
        file.write(string + '\n')


def pickle_save(filename, data):
    with open("../data/" + filename, "wb") as file:
        pickle.dump(data, file)


def pickle_load(filename):
    with open("../data/" + filename, "rb") as file:
        return pickle.load(file)


def jaccard_similarity(str1, str2):
    set1 = set(str1.lower())
    set2 = set(str2.lower())

    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection

    similarity = intersection / union
    return similarity


def is_time_valid_format(formatted_time):
    split_time = formatted_time.split(':')

    if len(formatted_time) == 5 and len(split_time) == 2:
        try:
            minutes = int(split_time[0])
            seconds = int(split_time[1])

            if 0 <= minutes < 60 and 0 <= seconds < 60:
                return True
        except ValueError:
            return False

    elif len(formatted_time) == 8 and len(split_time) == 3:
        try:
            hours = int(split_time[0])
            minutes = int(split_time[1])
            seconds = int(split_time[2])

            if 0 < hours and 0 <= minutes < 60 and 0 <= seconds < 60:
                return True
        except ValueError:
            return False

    elif formatted_time == "none":
        return True

    return False


def get_seconds_from_formatted_time(formatted_time):
    split_time = formatted_time.split(':')

    if len(formatted_time) == 5 and len(split_time) == 2:
        minutes = int(split_time[0])
        seconds = int(split_time[1])

        return minutes * 60 + seconds

    elif len(formatted_time) == 8 and len(split_time) == 3:
        hours = int(split_time[0])
        minutes = int(split_time[1])
        seconds = int(split_time[2])

        return hours * 3600 + minutes * 60 + seconds


def get_formatted_time_from_seconds(duration):
    h = int(duration // 3600)
    duration -= h * 3600
    m = int(duration // 60)
    duration -= m * 60
    s = int(duration // 1)
    duration -= s
    ms = int(round(duration, 3) * 1000)

    if h == 0 and ms == 0:
        return f"{m}:{'{:02d}'.format(s)}"
    elif h == 0 and ms != 0:
        return f"{m}:{'{:02d}'.format(s)}.{'{:03d}'.format(ms)}"
    elif h != 0 and ms == 0:
        return f"{h}:{'{:02d}'.format(m)}:{'{:02d}'.format(s)}"
    else:
        return f"{h}:{'{:02d}'.format(m)}:{'{:02d}'.format(s)}.{'{:03d}'.format(ms)}"
