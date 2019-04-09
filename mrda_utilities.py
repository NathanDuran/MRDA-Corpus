import os
import pickle
import re
import spacy
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en')
tokenizer = Tokenizer(nlp.vocab)


class Dialogue:
    def __init__(self, conversation_id, num_utterances, utterances):
        self.conversation_id = conversation_id
        self.num_utterances = num_utterances
        self.utterances = utterances

    def to_string(self):
        return str("Conversation: " + self.conversation_id + "\n"
                   + "Number of Utterances: " + str(self.num_utterances))


class Utterance:
    def __init__(self, speaker, text, basic_da_label, general_da_label, full_da_label):
        self.speaker = speaker
        self.text = text
        self.basic_da_label = basic_da_label
        self.general_da_label = general_da_label
        self.full_da_label = full_da_label

    def to_string(self):
        return str(self.speaker + " " +
                   self.text + " " +
                   self.basic_da_label + " " +
                   self.general_da_label + " " +
                   self.full_da_label)


def process_transcript(transcript, database, da_map, excluded_chars=None, excluded_tags=None):

    # Process each utterance in the transcript and create list of Utterance objects
    utterances = []
    for utt_index in range(len(transcript)):

        # Process the utterance text
        # Split on comma to get text from Original CSV Transcription
        text = transcript[utt_index].split(',')[1]

        # If text is allcaps i.e. 'DIGIT_TASK' then ignore
        if text.isupper():
            continue

        # Tokenise
        utterance_tokens = tokenizer(text)

        # Remove the word annotations and filter_disfluency
        utterance_text = []
        for word in utterance_tokens:
            word = word.text
            # If no excluded characters are present just add it
            if all(char not in excluded_chars for char in word):
                utterance_text.append(word)
            # Else, to keep hyphenated words, check 1st, last and 2nd-to-last char for interruptions (i.e. 'spi-,')
            elif len(word) > 1:
                if word[0] not in excluded_chars and word[-1] not in excluded_chars and word[-2] not in excluded_chars:
                    utterance_text.append(word)

        # Check utterance is not only punctuation (because the rest was invalid/removed)
        if len(utterance_text) > 0 and all(char in ['.', '?', '!', ' '] for char in utterance_text[0]):
            # If so, ignore
            continue
        # Else if the last token is punctuation, concatenate with last word
        elif len(utterance_text) > 1 and any(char in ['.', '?', '!'] for char in utterance_text[-1]):
            if len(utterance_text[-2]) > 0:
                utterance_text[-2] = ''.join((utterance_text[-2], utterance_text[-1]))
                utterance_text.pop()

        # Concatenate acronyms i.e. 't.v.'
        tmp_utt_txt = []
        i = 0
        while i < len(utterance_text):

            # Check if this token is part of an acronym i.e. 't.'
            if re.match("([a-zA-Z]\.)", utterance_text[i]):

                # Add the first part of the acronym
                accronym_list = [utterance_text[i]]

                # Find and add the following acronym tokens
                next_ind = i + 1
                while next_ind < len(utterance_text) and (re.match("([a-zA-Z]\.)", utterance_text[next_ind])
                                                          or (re.match("([a-zA-Z])", utterance_text[next_ind])
                                                              and len(utterance_text[next_ind]) == 1)):
                    # If the last token is missing full stop then append one
                    if re.match("([a-zA-Z])", utterance_text[next_ind]) and len(utterance_text[next_ind]) == 1:
                        utterance_text[next_ind] += '.'
                    accronym_list.append(utterance_text[next_ind])
                    next_ind += 1

                # Skip the acronym tokens we just appended
                i += len(accronym_list)

                # Join the acronym tokens and append to the sentence
                accronym = ''.join(accronym_list)
                tmp_utt_txt.append(accronym)

            # Else just add the word
            else:
                tmp_utt_txt.append(utterance_text[i])
                i += 1
        utterance_text = tmp_utt_txt

        # Join words for complete sentence
        utterance_text = " ".join(utterance_text)
        # Strip leading and trailing whitespace
        utterance_text.strip()
        # Strip duplicate whitespace
        utterance_text = re.sub(' +', ' ', utterance_text)

        # Process the utterance dialogue act, adjacency pair and speaker
        # Get the dialogue act from the database file
        raw_da_tag = database[utt_index].split(',')[5]

        # Get the basic da tag
        basic_da_tag = da_map[raw_da_tag]

        # Get the general and full da tags
        if any(char in ['|'] for char in raw_da_tag):  # Take first da if multiple
            raw_da_tag = raw_da_tag.split('|')[0]
        if any(char in [':'] for char in raw_da_tag):  # Remove quote da split
            raw_da_tag = raw_da_tag.split(':')[0]
        if any(char in ['.'] for char in raw_da_tag):  # Remove disruptive form tag
            raw_da_tag = raw_da_tag.split('.')[0]
        if any(char in ['^'] for char in raw_da_tag):  # Get general and full da tags
            general_da_tag = raw_da_tag.split('^')[0]
            full_da_tag = raw_da_tag.split('^')[1]
        # If no '^' separator general and full tags are the same
        else:
            general_da_tag = raw_da_tag
            full_da_tag = raw_da_tag

        # Collapse disruptions i.e. interrupted, abandoned and uninterpretable
        if any(char in ['-'] for char in general_da_tag):
            general_da_tag = '%'
        if any(char in ['-'] for char in full_da_tag):
            full_da_tag = '%'

        # Get the speaker label
        speaker = database[utt_index].split(',')[7]

        # Print original and processed utterances
        # print(str(utt_index) + " " + text)
        # print(str(utt_index) + " " + speaker + " " + utterance_text + " " +
        #       basic_da_tag + " " + general_da_tag + " " + full_da_tag)

        # Check we are not adding an empty utterance (i.e. because it was just 'DIGIT_TASK'),
        # or adding an utterance with an excluded tag.
        if len(utterance_text) > 0 \
                and basic_da_tag.lower() not in excluded_tags\
                and general_da_tag.lower() not in excluded_tags\
                and full_da_tag.lower() not in excluded_tags:

            # Create Utterance and add to list
            current_utt = Utterance(speaker, utterance_text, basic_da_tag, general_da_tag, full_da_tag)
            utterances.append(current_utt)

    # Create Dialogue
    transcript_id = transcript[0].split('-')[0]
    dialogue = Dialogue(transcript_id, len(utterances), utterances)

    return dialogue


def get_da_maps(path):
    # Load the da maps from file
    da_map_data = load_data(path)

    # Split on tabs and save to dictionary (key=full_da : val=basic_da)
    da_map = dict()
    for line in da_map_data:
        da_map[line.split('\t')[0]] = line.split('\t')[1]

    return da_map


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