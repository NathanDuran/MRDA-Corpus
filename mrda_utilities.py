import os
import pickle


def get_da_maps(path):
    # Load the da maps from file
    da_map_data = load_text_data(path)

    # Split on tabs and save to dictionary (key=full_da : val=basic_da)
    da_map = dict()
    for line in da_map_data:
        da_map[line.split('\t')[0]] = line.split('\t')[1]

    return da_map


def load_text_data(path, verbose=True):
    with open(path, "r") as file:
        # Read a line and strip newline char
        lines = [line.rstrip('\r\n') for line in file.readlines()]
    if verbose:
        print("Loaded data from file %s." % path)
    return lines


def save_data_pickle(path, data, verbose=True):
    with open(path, "wb") as file:
        pickle.dump(data, file, protocol=2)
    if verbose:
        print("Saved data to file %s." % path)


def dialogue_to_file(path, dialogue, utterance_only, write_type):
    if utterance_only:
        path = path + "_utt"
    with open(path + ".txt", write_type) as file:
        for utterance in dialogue.utterances:
            if utterance_only:
                file.write(utterance.text.strip() + "\n")
            else:
                file.write(utterance.speaker + "|" + utterance.text.strip() + "|" +
                           utterance.basic_da_label + "|" +
                           utterance.general_da_label + "|" +
                           utterance.full_da_label + "\n")


def remove_file(data_dir, file, utterance_only):
    # Remove either text or full versions
    if utterance_only:
        if os.path.exists(data_dir + file + "_utt" + ".txt"):
            os.remove(data_dir + file + "_utt" + ".txt")
    else:
        if os.path.exists(data_dir + file + ".txt"):
            os.remove(data_dir + file + ".txt")