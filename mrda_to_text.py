from mrda_utilities import *
from process_transcript import *

# Switchboard archive directory
archive_dir = 'mrda_archive'

# Processed data directory
data_dir = 'mrda_data'

# Metadata directory
metadata_dir = os.path.join(data_dir, 'metadata')

# If flag is set will only write utterances and not speaker or DA label
utterance_only_flag = False

# Excluded dialogue act tags i.e. x = Non-verbal and z = Non-labeled
excluded_tags = ['x', 'z']
# Excluded characters for ignoring i.e. '=='
excluded_chars = {'<', '>', '(', ')', '-', '#', '|', '=', '@'}

# Load training, test, validation and development splits
train_split = load_text_data(os.path.join(metadata_dir, 'train_split.txt'))
test_split = load_text_data(os.path.join(metadata_dir, 'test_split.txt'))
val_split = load_text_data(os.path.join(metadata_dir, 'val_split.txt'))

# Load basic da map data
da_map = get_da_maps(os.path.join(metadata_dir, 'basic_da_map.txt'))

# Files for all the utterances in the corpus and data splits
full_set = "full_set"
train_set_file = "train_set"
test_set_file = "test_set"
val_set_file = "val_set"

# Remove old files if they exist, so we do not append to old data
remove_file(data_dir, full_set, utterance_only_flag)
remove_file(data_dir, train_set_file, utterance_only_flag)
remove_file(data_dir, test_set_file, utterance_only_flag)
remove_file(data_dir, val_set_file, utterance_only_flag)

# Get a list of all the transcripts
transcript_list = os.listdir(os.path.join(archive_dir, 'transcripts'))

# Process each transcript
for meeting in transcript_list:

    # Get the id for this meeting
    meeting_name = str(meeting.split('.')[0])

    # Get the transcript and database file
    transcript = load_text_data(os.path.join(archive_dir, 'transcripts', meeting_name + '.trans'), verbose=False)
    database = load_text_data(os.path.join(archive_dir, 'database', meeting_name + '.dadb'), verbose=False)

    # Process the utterances and create a dialogue object
    dialogue = process_transcript(transcript, database, da_map, excluded_chars, excluded_tags)

    # Append all utterances to full_set text file
    dialogue_to_file(os.path.join(data_dir, full_set), dialogue, utterance_only_flag, 'a+')

    # Determine which set this dialogue belongs to (training, test or evaluation)
    set_dir = ''
    set_file = ''
    if meeting_name in train_split:
        set_dir = 'train'
        set_file = train_set_file
    elif meeting_name in test_split:
        set_dir = 'test'
        set_file = test_set_file
    elif meeting_name in val_split:
        set_dir = 'val'
        set_file = val_set_file

    # If only saving utterances use different directory
    if utterance_only_flag:
        set_dir = os.path.join(data_dir, set_dir + '_utt')
    else:
        set_dir = os.path.join(data_dir, set_dir)

    # Create the directory if is doesn't exist yet
    if not os.path.exists(set_dir):
        os.makedirs(set_dir)

    # Write individual dialogue to train, test or validation folders
    dialogue_to_file(os.path.join(set_dir, meeting_name), dialogue, utterance_only_flag, 'w+')

    # Append all dialogue utterances to sets file
    dialogue_to_file(os.path.join(data_dir, set_file), dialogue, utterance_only_flag, 'a+')

