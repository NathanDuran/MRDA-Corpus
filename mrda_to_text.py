from mrda_utilities import *

# Switchboard archive directory
archive_dir = 'mrda_archive'

# Processed data directory
data_dir = 'mrda_data/'

# If flag is set will only write utterances and not speaker or DA label
utterance_only_flag = False

# Excluded characters for ignoring i.e. '=='
excluded_chars = {'<', '>', '(', ')', '-', '#', '|', '='}

# Load training, test, validation and development splits
train_split = load_data(data_dir + 'train_split.txt')
test_split = load_data(data_dir + 'test_split.txt')
val_split = load_data(data_dir + 'eval_split.txt')
dev_split = load_data(data_dir + 'dev_split.txt')

# Files for all the utterances in the corpus and data splits
all_mrda_file = "all_mrda"
train_set_file = "train_set"
test_set_file = "test_set"
val_set_file = "eval_set"
dev_set_file = "dev_set"

# Remove old files if they exist, so we do not append to old data
remove_file(data_dir, all_mrda_file, utterance_only_flag)
remove_file(data_dir, train_set_file, utterance_only_flag)
remove_file(data_dir, test_set_file, utterance_only_flag)
remove_file(data_dir, val_set_file, utterance_only_flag)
remove_file(data_dir, dev_set_file, utterance_only_flag)

# TEST TRANSCRIPT
trans_name = "Bed004"

transcript = load_data(archive_dir + "/" + trans_name + ".trans")
database = load_data(archive_dir + "/" + trans_name + ".dadb")


process_transcript(transcript, database, excluded_chars)