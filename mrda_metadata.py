import itertools
import gluonnlp as nlp
from mrda_utilities import *
# Initialise Spacy tokeniser
tokeniser = nlp.data.SpacyTokenizer('en')

# Dictionary for metadata
metadata = dict()

# Processed data directory
data_dir = 'mrda_data'

# Metadata directory
metadata_dir = os.path.join(data_dir, 'metadata')

# Load full_set text file
mrda_text = load_text_data(os.path.join(data_dir, 'full_set.txt'))

# Split into labels and utterances
utterances = []
basic_da_labels = []
general_da_labels = []
full_da_labels = []
for line in mrda_text:
    utterances.append(line.split("|")[1])
    basic_da_labels.append(line.split("|")[2])
    general_da_labels.append(line.split("|")[3])
    full_da_labels.append(line.split("|")[4])

# Count total number of utterances
num_utterances = len(utterances)

metadata['num_utterances'] = num_utterances
print("Total number of utterances: ", num_utterances)

# Calculate max utterance length in tokens
max_utterance_len = 0
tokenised_utterances = []
for utt in utterances:

    # Tokenise utterance
    tokenised_utterance = tokeniser(utt)
    if len(tokenised_utterance) > max_utterance_len:
        max_utterance_len = len(tokenised_utterance)

    tokenised_utterances.append(tokenised_utterance)

metadata['max_utterance_len'] = max_utterance_len
print("Max utterance length: ", max_utterance_len)
assert num_utterances == len(tokenised_utterances)

# Count the word frequencies and generate vocabulary
word_freq = nlp.data.count_tokens(list(itertools.chain(*tokenised_utterances)))
vocabulary = nlp.Vocab(word_freq)
vocabulary_size = len(word_freq)

metadata['word_freq'] = word_freq
metadata['vocabulary'] = vocabulary
metadata['vocabulary_size'] = vocabulary_size
print("Words:")
print(word_freq)
print(vocabulary)
print(vocabulary_size)

# Write vocabulary and word frequencies to file
with open(os.path.join(metadata_dir, 'vocabulary.txt'), 'w+') as file:
    for i in range(4, len(vocabulary)):
        file.write(vocabulary.to_tokens(i) + " " + str(word_freq[vocabulary.to_tokens(i)]) + "\n")

# Count the basic label frequencies and generate labels
basic_label_freq = nlp.data.count_tokens(basic_da_labels)
basic_labels = nlp.Vocab(basic_label_freq)
num_basic_labels = len(basic_label_freq)

metadata['basic_label_freq'] = basic_label_freq
metadata['basic_labels'] = basic_labels
metadata['num_basic_labels'] = num_basic_labels
print("Basic Labels:")
print(basic_label_freq)
print(basic_labels)
print(num_basic_labels)

# Write labels and frequencies to file
with open(os.path.join(metadata_dir, 'labels.txt'), 'w+') as file:
    file.write("Basic Labels:\n")
    for i in range(4, len(basic_labels)):
        file.write(basic_labels.to_tokens(i) + " " + str(basic_label_freq[basic_labels.to_tokens(i)]) + "\n")
    file.write("\n")

# Count the general label frequencies and generate labels
general_label_freq = nlp.data.count_tokens(general_da_labels)
general_labels = nlp.Vocab(general_label_freq)
num_general_labels = len(general_label_freq)

metadata['general_label_freq'] = general_label_freq
metadata['general_labels'] = general_labels
metadata['num_general_labels'] = num_general_labels
print("General Labels:")
print(general_label_freq)
print(general_labels)
print(num_general_labels)

# Write labels and frequencies to file
with open(os.path.join(metadata_dir, 'labels.txt'), 'a+') as file:
    file.write("General Labels:\n")
    for i in range(4, len(general_labels)):
        file.write(general_labels.to_tokens(i) + " " + str(general_label_freq[general_labels.to_tokens(i)]) + "\n")
    file.write("\n")

# Count the full label frequencies and generate labels
full_label_freq = nlp.data.count_tokens(full_da_labels)
full_labels = nlp.Vocab(full_label_freq)
num_full_labels = len(full_label_freq)

metadata['full_label_freq'] = full_label_freq
metadata['full_labels'] = full_labels
metadata['num_full_labels'] = num_full_labels
print("Full Labels:")
print(full_label_freq)
print(full_labels)
print(num_full_labels)

# Write labels and frequencies to file
with open(os.path.join(metadata_dir, 'labels.txt'), 'a+') as file:
    file.write("Full Labels:\n")
    for i in range(4, len(full_labels)):
        file.write(full_labels.to_tokens(i) + " " + str(full_label_freq[full_labels.to_tokens(i)]) + "\n")
    file.write("\n")

# Count sets number of dialogues and maximum dialogue length
max_dialogues_len = 0
sets = ['train', 'test', 'val', 'dev']
for i in range(len(sets)):

    # Load data set list
    set_list = load_text_data(os.path.join(metadata_dir, sets[i] + '_split.txt'))

    # Count the number of dialogues in the set
    set_num_dialogues = len(set_list)
    metadata[sets[i] + '_num_dialogues'] = set_num_dialogues
    print("Number of dialogue in " + sets[i] + " set: " + str(set_num_dialogues))

    # Count max number of utterances in sets dialogues
    set_max_dialogues_len = 0
    for dialogue in set_list:

        # Load dialogues utterances
        utterances = load_text_data(os.path.join(data_dir, sets[i], dialogue + '.txt'), verbose=False)

        # Check set and global maximum dialogue length
        if len(utterances) > set_max_dialogues_len:
            set_max_dialogues_len = len(utterances)

        if set_max_dialogues_len > max_dialogues_len:
            max_dialogues_len = set_max_dialogues_len

    metadata[sets[i] + '_max_dialogues_len'] = set_max_dialogues_len
    print("Maximum length of dialogue in " + sets[i] + " set: " + str(set_max_dialogues_len))

metadata['max_dialogues_len'] = max_dialogues_len
print("Maximum dialogue length: " + str(max_dialogues_len))

# Save data to pickle file
save_data_pickle(os.path.join(metadata_dir, 'metadata.pkl'), metadata)
