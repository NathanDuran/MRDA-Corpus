from mrda_utilities import *

# Switchboard archive directory
archive_dir = 'mrda_archive'

# Processed data directory
data_dir = 'mrda_data/'

# If flag is set will only write utterances and not speaker or DA label
utterance_only_flag = False

# Excluded dialogue act tags i.e. x = Non-verbal
excluded_tags = ['x'] # TODO exclude z tag?
# Excluded characters for ignoring i.e. '=='
excluded_chars = {'<', '>', '(', ')', '-', '#', '|', '=', '@'}

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

# Get a list of all the transcripts
transcript_list = os.listdir(archive_dir + "/transcripts")

# Process each transcript
for meeting in transcript_list:

    # Get the id for this meeting
    meeting_name = meeting.split('.')[0]

    # Get the transcript and database file
    transcript = load_data(archive_dir + "/transcripts/" + meeting_name + ".trans", verbose=False)
    database = load_data(archive_dir + "/database/" + meeting_name + ".dadb", verbose=False)

    # Process the utterances and create a dialogue object
    dialogue = process_transcript(transcript, database, excluded_chars, excluded_tags)

    # Append all utterances to all_mrda text file
    dialogue_to_file(data_dir + all_mrda_file, dialogue, utterance_only_flag, 'a+')

    # Determine which set this dialogue belongs to (training, test or evaluation)
    set_dir = ''
    set_file = ''
    if meeting_name in train_split:
        set_dir = data_dir + 'train'
        set_file = train_set_file
    elif meeting_name in test_split:
        set_dir = data_dir + 'test'
        set_file = test_set_file
    elif meeting_name in val_split:
        set_dir = data_dir + 'eval'
        set_file = val_set_file

    # If only saving utterances use different directory
    if utterance_only_flag:
        set_dir = set_dir + "_utt/"
    else:
        set_dir = set_dir + "/"

    # Create the directory if is doesn't exist yet
    if not os.path.exists(set_dir):
        os.makedirs(set_dir)

    # Write individual dialogue to train, test or validation folders
    dialogue_to_file(set_dir + meeting_name, dialogue, utterance_only_flag, 'w+')

    # Append all dialogue utterances to sets file
    dialogue_to_file(data_dir + set_file, dialogue, utterance_only_flag, 'a+')

    # If it is also in the development set write it there too
    if meeting_name in dev_split:

        set_dir = data_dir + 'dev'
        set_file = dev_set_file

        # If only saving utterances use different directory
        if utterance_only_flag:
            set_dir = set_dir + "_utt/"
        else:
            set_dir = set_dir + "/"

        # Create the directory if is doesn't exist yet
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        # Write individual dialogue to dev folder
        dialogue_to_file(set_dir + meeting_name, dialogue, utterance_only_flag, 'w+')

        # Append all dialogue utterances to dev set file
        dialogue_to_file(data_dir + set_file, dialogue, utterance_only_flag, 'a+')
