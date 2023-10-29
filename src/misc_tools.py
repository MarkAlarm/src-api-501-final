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
