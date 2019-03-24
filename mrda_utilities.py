import os
import pickle
import spacy
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en')
tokenizer = Tokenizer(nlp.vocab)


class Dialogue:
    def __init__(self, folder_name, conversation_num, num_utterances, utterances):
        self.folder_name = folder_name
        self.conversation_num = conversation_num
        self.num_utterances = num_utterances
        self.utterances = utterances

    def to_string(self):
        return str("Folder Name: " + self.folder_name + "\n"
                   + "Conversation: " + self.conversation_num + "\n"
                   + "Number of Utterances: " + str(self.num_utterances))


class Utterance:
    def __init__(self, speaker, text, da_label):
        self.speaker = speaker
        self.text = text
        self.da_label = da_label

    def to_string(self):
        return str(self.speaker + " " + self.text + " " + self.da_label)


def process_transcript(transcript, database, excluded_chars=None):

    # Process each utterance in the transcript and create list of Utterance objects
    utterances = []
    for utt_index in range(len(transcript)):

        # Split on comma to get text from CSV
        utterance_tokens = tokenizer(transcript[utt_index].split(',')[1])
        print(len(utterance_tokens))


        # Remove the word annotations and filter_disfluency
        utterance_text = []
        for word in utterance_tokens:
            word = word.text
            # If no excluded characters are present just add it
            if all(char not in excluded_chars for char in word):
                utterance_text.append(word)
                
            # # Else, if it contains'#' that is sometimes appended to words remove
            # elif any(char in excluded_chars for char in word):
            #     for char in word:
            #         if char in excluded_chars:
            #             word = word.replace(char, "")
            #             utterance_text.append(word)

            # Else, to keep hyphenated words, check 1st, last and 2nd-to-last char for interruptions (i.e. 'spi-,')
            elif len(word) > 1:
                if word[0] not in excluded_chars and word[-1] not in excluded_chars and word[-2] not in excluded_chars:
                    utterance_text.append(word)

        # If the last token is punctuation, concatenate with last word
        if len(utterance_text) > 1:
            if any(char in ['.', '?'] for char in utterance_text[-1]):
                utterance_text[-2] = ''.join((utterance_text[-2], utterance_text[-1]))
                utterance_text.pop()

        # Join words for complete sentence
        utterance_text = " ".join(utterance_text)
        # Strip leading and trailing whitespace
        utterance_text.strip()

        print(utterance_tokens)
        print(utterance_text)



def load_data(path, verbose=True):
    with open(path, "r") as file:
        # Read a line and strip newline char
        lines = [line.rstrip('\r\n') for line in file.readlines()]
    if verbose:
        print("Loaded data from file %s." % path)
    return lines


def save_data_pickle(path, data, verbose=True):
    file = open(path, "wb")
    pickle.dump(data, file, protocol=2)
    file.close()
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
                file.write(utterance.speaker + "|" + utterance.text.strip() + "|" + utterance.da_label + "\n")


def remove_file(data_dir, file, utterance_only):
    # Remove either text or full versions
    if utterance_only:
        if os.path.exists(data_dir + file + "_utt" + ".txt"):
            os.remove(data_dir + file + "_utt" + ".txt")
    else:
        if os.path.exists(data_dir + file + ".txt"):
            os.remove(data_dir + file + ".txt")