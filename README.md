# Processing the Meeting Recorder Dialogue Act Corpus
Utilities for Processing the Meeting Recorder Dialogue Act Corpus outlined in [this paper by Shriberg, E. et al.(2004)](https://aclweb.org/anthology/W04-2319) for the purpose of dialogue act (DA) classification.
The data can also be downloaded [here](http://www1.icsi.berkeley.edu/~ees/dadb/).
The data is split into the original training and test sets suggested by the authors.
The development set is now used as an evaluation set and a new development set was created from 24 randomly selected from the training set.
There were two unused dialogues and these were added to the evaluation and test sets.

## Scripts
The mrda_to_text.py script processes all dialogues into a plain text format. Individual dialogues are saved into directories corresponding
to the set they belong to (train, test, etc). All utterances in a particular set are also saved to a text file.

The mrda_utilities.py script contains various helper functions for loading/saving and processing the data, including a function for processing each dialogue.

The mrda_metadata.py generates various metadata from the processed dialogues and saves them as a dictionary to a pickle file.
The words, labels and frequencies are also saved as plain text files in the /metadata directory.

## Data Format
Utterance are tagged with the MRDA tagset, which is a variation of the [SWBD-DAMSL](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html) DA.
The original MRDA label construction allowed DA to be concatenated in the form <*general tag*> ^ <*specific tag*> . <*disruptive from*> (see the [MRDA manual](mrda_manual.pdf)).

There are three sets of DA included: 
- Basic, collapses all DA into 5 labels outlined in the original documentation DA maps (see the [basic DA map file](mrda_data/metadata/basic_da_map.txt)).
- General, uses the 12 <*general tag*> described in the [MRDA manual](mrda_manual.pdf).
- Full, uses only the first <*specific tag*> from the original labels, 52 in total.

By default:
- Utterances are written one per line in the format *Speaker* | *Utterance Text* | *Basic DA Tag* | *General DA Tag* | *Full DA Tag*. Setting the utterance_only_flag == True, will change the default output to only one utterance per line i.e. no speaker or DA tags.
- Utterances marked as *Non-verbal* ('x' tags) are removed i.e. 'Laughter' or 'Throat_clearing'.
- Utterances marked as *Non-labeled* ('z' tags) are removed.
- *Interrupted*, *Abandoned* and *Uninterpretable* tags are collapsed into one tag ('%').
- All disfluency annotations are removed i.e. '#', '<', '>', etc.

### Example Utterances
fe016|okay.|F|fg|fg

fe016|so um|F|fh|fh

fe016|i was going to try to get out of here like in half an hour.|S|s|rt

## Dialogue Acts

### Basic Labels
Dialogue Act    | MRDA Label    | Count
--- | :---: | :---:
Statement   | S    | 64233
BackChannel   | B    | 14620
Disruption   | D    | 14548
FloorGrabber | F    | 7818
Question    | Q    | 6983

### General Labels
Dialogue Act    | MRDA Label    | Count
--- | :---: | :---:
Statement   | s    | 69873
Continuer   | b    | 15167
Floor Holder   | fh    | 8362
Yes-No-question | qy    | 4986
Interrupted/Abandoned/Uninterpretable    | %    | 3103
Floor Grabber   | fg    | 3092
Wh-Question   | qw    | 1707
Hold Before Answer/Agreement   | h    | 792
Or-Clause | qrr    | 392
Rhetorical Question    | qh    | 352
Or Question | qr    | 207
Open-ended Question    | qo    | 169

### Full Labels
Dialogue Act    | MRDA Label    | Count
--- | :---: | :---:
Statement   | s    | 33472
Continuer   | b    | 15013
Floor Holder   | fh    | 8362
Acknowledge-answer | bk    | 7177
Accept    | aa    | 5898
Defending/Explanation    | df    | 3724
Expansions of y/n Answers | e    | 3200
Interrupted/Abandoned/Uninterpretable | %    | 3103
Rising Tone | rt    | 3101
Floor Grabber    | fg    | 3092
Offer  | cs | 2662
Assessment/Appreciation    | ba    | 2216
Understanding Check   | bu    | 2091
Declarative-Question | d    | 1805
Affirmative Non-yes Answers    | na | 1112
Wh-Question   | qw    | 951
Reject   | ar    | 908
Collaborative Completion   | 2    | 841
Other Answers | no    | 828
Hold Before Answer/Agreement    | h    | 792
Action-directive    | co    | 674
Yes-No-question   | qy    | 669
Dispreferred Answers   | nd    | 483
Humorous Material   | j    | 463
Downplayer    | bd    | 387
Commit  | cc    | 371
Negative Non-no Answers | ng    | 351
Maybe    | am    | 349
Or-Clause   | qrr    | 345
Exclamation    | fe    | 307
Mimic Other   | m    | 293
Apology    | fa    | 259
About-task  | t    | 253
Signal-non-understanding   | br    | 236
Accept-part  | aap    | 219
Rhetorical-Question	| qh    | 214
Topic Change    | tc    | 212
Repeat | r    | 208
Self-talk | t1    | 198
3rd-party-talk    | t3    | 165
Rhetorical-question Continue    | bh    | 154
Reject-part    | arp    | 150
Misspeak Self-Correction    | bsc    | 150
Reformulate/Summarize    | bs    | 141
"Follow Me"    | f    | 128
Or-Question    | qr    | 127
Thanking    | ft    | 119
Tag-Question    | g    | 87
Open-Question    | qo    | 74
Correct-misspeaking    | bc    | 51
Sympathy    | by    | 11
Welcome    | fw    | 6

## Metadata
- Total number of utterances: 108202
- Max utterance length: 85
- Maximum dialogue length: 3391
- Vocabulary size: 10866
- Number of basic labels: 5
- Number of general labels: 12
- Number of full labels: 52
- Number of dialogue in train set: 51
- Maximum length of dialogue in train set: 3391
- Number of dialogue in test set: 12
- Maximum length of dialogue in test set: 2028
- Number of dialogue in eval set: 12
- Maximum length of dialogue in eval set: 1969
- Number of dialogue in dev set: 24
- Maximum length of dialogue in dev set: 2220

### Keys and values for the metadata dictionary
- num_utterances = Total number of utterance in the full corpus.
- max_utterance_len = Number of words in the longest utterance in the corpus.
- max_dialogues_len = Number of utterances in the longest dialogue in the corpus.
- word_freq = Dictionary with {word : frequency} pairs.
- vocabulary = Full vocabulary - Gluon NLP [Vocabulary.](http://gluon-nlp.mxnet.io/api/modules/vocab.html#gluonnlp.Vocab)
- vocabulary_size = Number of words in the vocabulary.

Each label set (basic, general or full) also has:
- <*setname*>_label_freq = Dictionary with {dialogue act label : frequency} pairs.
- <*setname*>_labels = Full DA labels in a Gluon NLP [Vocabulary.](http://gluon-nlp.mxnet.io/api/modules/vocab.html#gluonnlp.Vocab)
- num_<*setname*>_labels = Number of labels used from each of the label sets.

Each data set also has:
- <*setname*>_num_dialogues = Number of dialogues in the set.
- <*setname*>_max_dialogues_len = Length of the longest dialogue in the set.