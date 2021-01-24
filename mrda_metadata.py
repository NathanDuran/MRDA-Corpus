import itertools
from utilities import *
# Initialise Spacy tokeniser
tokeniser = nlp.data.SpacyTokenizer('en_core_web_sm')

# Dictionary for metadata
metadata = dict()

# Processed data directory
data_dir = 'mrda_data'

# Metadata directory
metadata_dir = os.path.join(data_dir, 'metadata')

# Load full_set text file
text = load_text_data(os.path.join(data_dir, 'full_set.txt'))

# Split into speakers and utterances
utterances = []
speakers = []
for line in text:
    utterances.append(line.split("|")[1])
    speakers.append(line.split("|")[0])

# Count total number of utterances
num_utterances = len(utterances)
metadata['num_utterances'] = num_utterances

# Calculate max/mean utterance length in tokens
max_utterance_len = 0
mean_utterance_len = 0
tokenised_utterances = []
for utt in utterances:

    # Tokenise utterance
    tokenised_utterance = tokeniser(utt)
    if len(tokenised_utterance) > max_utterance_len:
        max_utterance_len = len(tokenised_utterance)

    tokenised_utterances.append(tokenised_utterance)

    # Add length to mean
    mean_utterance_len += len(tokenised_utterance)

assert num_utterances == len(tokenised_utterances)
metadata['max_utterance_len'] = max_utterance_len
metadata['mean_utterance_len'] = mean_utterance_len / num_utterances

# Count each sets number of dialogues, max/mean dialogue length and number of utterances
max_dialogue_len = 0
mean_dialogue_len = 0
num_dialogues = 0
sets = ['train', 'test', 'val']
for dataset_name in sets:

    # Load data set list
    set_list = load_text_data(os.path.join(metadata_dir, dataset_name + '_split.txt'))

    # Count the number of dialogues in the set
    set_num_dialogues = len(set_list)
    metadata[dataset_name + '_num_dialogues'] = set_num_dialogues

    # Count max number of utterances in sets dialogues
    set_max_dialogue_len = 0
    set_mean_dialogue_len = 0
    set_num_utterances = 0
    for dialogue in set_list:

        # Load dialogues utterances
        utterances = load_text_data(os.path.join(data_dir, dataset_name, dialogue + '.txt'), verbose=False)

        # Count dialogue length for means/number of utterances
        num_dialogues += 1
        mean_dialogue_len += len(utterances)
        set_mean_dialogue_len += len(utterances)
        set_num_utterances += len(utterances)

        # Check set and global maximum dialogue length
        if len(utterances) > set_max_dialogue_len:
            set_max_dialogue_len = len(utterances)

        if set_max_dialogue_len > max_dialogue_len:
            max_dialogue_len = set_max_dialogue_len

    metadata[dataset_name + '_max_dialogue_len'] = set_max_dialogue_len
    metadata[dataset_name + '_mean_dialogue_len'] = set_mean_dialogue_len / set_num_dialogues
    metadata[dataset_name + '_num_utterances'] = set_num_utterances

metadata['num_dialogues'] = num_dialogues
metadata['max_dialogue_len'] = max_dialogue_len
metadata['mean_dialogue_len'] = mean_dialogue_len / num_dialogues

# Count the word frequencies and generate vocabulary
word_freq = pd.DataFrame.from_dict(nlp.data.count_tokens(list(itertools.chain(*tokenised_utterances))), orient='index')
word_freq.reset_index(inplace=True)
word_freq.columns = ['Words', 'Count']
word_freq.sort_values('Count', ascending=False, ignore_index=True, inplace=True)
vocabulary = word_freq['Words'].to_list()
vocabulary_size = len(word_freq)

metadata['word_freq'] = word_freq
metadata['vocabulary'] = vocabulary
metadata['vocabulary_size'] = vocabulary_size
print("Vocabulary:")
print(word_freq)
print(vocabulary)

# Write vocabulary and word frequencies to file
save_word_frequency_distributions(word_freq, metadata_dir, 'word_freq.txt')
save_text_data(os.path.join(metadata_dir, 'vocabulary.txt'), vocabulary)

# Count the basic label frequencies and generate labels
basic_labels, basic_label_freq = get_label_frequency_distributions(data_dir, metadata_dir, label_map='basic_label_map.txt', label_index=2)
metadata['basic_label_freq'] = basic_label_freq
metadata['basic_labels'] = basic_labels
metadata['num_basic_labels'] = len(basic_labels)
print("Basic Labels:")
print(basic_labels)

# Create label frequency chart
label_freq_chart = plot_label_distributions(basic_label_freq, title='MRDA Basic Label Frequency Distributions', num_labels=15)
label_freq_chart.savefig(os.path.join(metadata_dir, 'MRDA Basic Label Frequency Distributions.png'))

# Write labels and frequencies to file
save_label_frequency_distributions(basic_label_freq, metadata_dir, 'basic_label_freq.txt', to_markdown=False)
save_text_data(os.path.join(metadata_dir, 'basic_labels.txt'), basic_labels)

# Count the general label frequencies and generate labels
general_labels, general_label_freq = get_label_frequency_distributions(data_dir, metadata_dir, label_map='general_label_map.txt', label_index=3)
metadata['general_label_freq'] = general_label_freq
metadata['general_labels'] = general_labels
metadata['num_general_labels'] = len(general_labels)
print("General Labels:")
print(general_labels)

# Create label frequency chart
label_freq_chart = plot_label_distributions(general_label_freq, title='MRDA General Frequency Distributions', num_labels=15)
label_freq_chart.savefig(os.path.join(metadata_dir, 'MRDA General Frequency Distributions.png'))

# Write labels and frequencies to file
save_label_frequency_distributions(general_label_freq, metadata_dir, 'general_label_freq.txt', to_markdown=False)
save_text_data(os.path.join(metadata_dir, 'general_labels.txt'), general_labels)

# Count the full label frequencies and generate labels
full_labels, full_label_freq = get_label_frequency_distributions(data_dir, metadata_dir, label_map='full_label_map.txt', label_index=4)
metadata['full_label_freq'] = full_label_freq
metadata['full_labels'] = full_labels
metadata['num_full_labels'] = len(full_labels)
print("Full Labels:")
print(full_labels)

# Create label frequency chart
label_freq_chart = plot_label_distributions(full_label_freq, title='MRDA Full Frequency Distributions', num_labels=15)
label_freq_chart.savefig(os.path.join(metadata_dir, 'MRDA Full Frequency Distributions.png'))

# Write labels and frequencies to file
save_label_frequency_distributions(full_label_freq, metadata_dir, 'full_label_freq.txt', to_markdown=False)
save_text_data(os.path.join(metadata_dir, 'full_labels.txt'), full_labels)

# Count speakers and save to list
metadata['num_speakers'] = len(set(speakers))
metadata['speakers'] = list(set(speakers))
save_text_data(os.path.join(metadata_dir, 'speakers.txt'), list(set(speakers)))
print("Speakers:")
print(speakers)

# Create and print the metadata string
metadata_str = ["- Total number of utterances: " + str(metadata['num_utterances']),
                "- Max utterance length: " + str(metadata['max_utterance_len']),
                "- Mean utterance length: " + str(round(metadata['mean_utterance_len'], 2)),
                "- Total Number of dialogues: " + str(metadata['num_dialogues']),
                "- Max dialogue length: " + str(metadata['max_dialogue_len']),
                "- Mean dialogue length: " + str(round(metadata['mean_dialogue_len'], 2)),
                "- Vocabulary size: " + str(metadata['vocabulary_size']),
                "- Number of basic labels: " + str(metadata['num_basic_labels']),
                "- Number of general labels: " + str(metadata['num_general_labels']),
                "- Number of full labels: " + str(metadata['num_full_labels']),
                "- Number of speakers: " + str(metadata['num_speakers'])]

for dataset_name in sets:
    metadata_str.append(dataset_name.capitalize() + " set")
    metadata_str.append("- Number of dialogues: " + str(metadata[dataset_name + '_num_dialogues']))
    metadata_str.append("- Max dialogue length: " + str(metadata[dataset_name + '_max_dialogue_len']))
    metadata_str.append("- Mean dialogue length: " + str(round(metadata[dataset_name + '_mean_dialogue_len'], 2)))
    metadata_str.append("- Number of utterances: " + str(metadata[dataset_name + '_num_utterances']))

for string in metadata_str:
    print(string)

# Save metadata to pickle and text file
save_data_pickle(os.path.join(metadata_dir, 'metadata.pkl'), metadata)
save_text_data(os.path.join(metadata_dir, 'metadata.txt'), metadata_str)
