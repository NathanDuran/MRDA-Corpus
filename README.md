# Processing the Meeting Recorder Dialogue Act Corpus
Utilities for Processing the Meeting Recorder Dialogue Act Corpus outlined in [this paper by Shriberg, E. et al.(2004)](https://aclweb.org/anthology/W04-2319) for the purpose of dialogue act (DA) classification.
The data can also be downloaded [here](http://www1.icsi.berkeley.edu/~ees/dadb/).
The data is split into the original training and test sets suggested by the authors.
The development set is now used as an evaluation set and a new development set was created from 24 randomly selected from the training set.
There were two unused dialogues and these were added to the evaluation and test sets.

## Scripts
The mrda_to_text.py script processes all dialogues into a plain text format. Individual dialogues are saved into directories corresponding
to the set they belong to (train, test, etc). All utterances in a particular set are also saved to a text file.

The mrda_utilities.py script contains various helper functions for loading/saving the data.

The process_transcript.py includes functions for processing each dialogue.

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
- Utterances are written one per line in the format *Speaker* | *Utterance Text* | *Basic DA Tag* | *General DA Tag* | *Full DA Tag*.
- Setting the utterance_only_flag == True, will change the default output to only one utterance per line i.e. no speaker or DA tags.
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
Dialogue Act                   |        Labels        |  Count   |    %     |   Train Count   | Train %  |   Test Count    |  Test %  |    Val Count    |  Val %  
--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:
Statement                      |          S           |  64233   |  59.36   |      45099      |  60.08   |      9571       |  57.30   |      9563       |  58.19  
BackChannel                    |          B           |  14620   |  13.51   |      10265      |  13.67   |      2152       |  12.88   |      2203       |  13.41  
Disruption                     |          D           |  14548   |  13.45   |      9739       |  12.97   |      2339       |  14.00   |      2470       |  15.03  
FloorGrabber                   |          F           |   7818   |   7.23   |      5324       |   7.09   |      1409       |   8.44   |      1085       |   6.60  
Question                       |          Q           |   6983   |   6.45   |      4640       |   6.18   |      1231       |   7.37   |      1112       |   6.77 

![Basic Label Frequencies](mrda_data/metadata/MRDA%20Basic%20Label%20Frequency%20Distributions.png)

### General Labels
Dialogue Act                   |        Labels        |  Count   |    %     |   Train Count   | Train %  |   Test Count    |  Test %  |    Val Count    |  Val %  
--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:
Statement                      |          s           |  69873   |  64.58   |      48952      |  65.21   |      10472      |  62.70   |      10449      |  63.59  
Continuer                      |          b           |  15167   |  14.02   |      10606      |  14.13   |      2219       |  13.29   |      2342       |  14.25  
Floor Holder                   |          fh          |   8362   |   7.73   |      5617       |   7.48   |      1520       |   9.10   |      1225       |   7.45  
Yes-No-question                |          qy          |   4986   |   4.61   |      3310       |   4.41   |       870       |   5.21   |       806       |   4.90  
Interrupted/Abandoned/Uninterpretable |          %           |   3103   |   2.87   |      2171       |   2.89   |       492       |   2.95   |       440       |   2.68  
Floor Grabber                  |          fg          |   3092   |   2.86   |      2076       |   2.77   |       489       |   2.93   |       527       |   3.21  
Wh-Question                    |          qw          |   1707   |   1.58   |      1110       |   1.48   |       310       |   1.86   |       287       |   1.75  
Hold Before Answer/Agreement   |          h           |   792    |   0.73   |       474       |   0.63   |       134       |   0.80   |       184       |   1.12  
Or-Clause                      |         qrr          |   392    |   0.36   |       244       |   0.33   |       75        |   0.45   |       73        |   0.44  
Rhetorical Question            |          qh          |   352    |   0.33   |       260       |   0.35   |       56        |   0.34   |       36        |   0.22  
Or Question                    |          qr          |   207    |   0.19   |       131       |   0.17   |       37        |   0.22   |       39        |   0.24  
Open-ended Question            |          qo          |   169    |   0.16   |       116       |   0.15   |       28        |   0.17   |       25        |   0.15  

![General Label Frequencies](mrda_data/metadata/MRDA%20General%20Frequency%20Distributions.png)

### Full Labels
Dialogue Act                   |        Labels        |  Count   |    %     |   Train Count   | Train %  |   Test Count    |  Test %  |    Val Count    |  Val %  
--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:
Statement                      |          s           |  33472   |  30.93   |      23238      |  30.96   |      4971       |  29.76   |      5263       |  32.03  
Continuer                      |          b           |  15013   |  13.87   |      10517      |  14.01   |      2175       |  13.02   |      2321       |  14.12  
Floor Holder                   |          fh          |   8362   |   7.73   |      5617       |   7.48   |      1520       |   9.10   |      1225       |   7.45  
Acknowledge-answer             |          bk          |   7177   |   6.63   |      5117       |   6.82   |      1031       |   6.17   |      1029       |   6.26  
Accept                         |          aa          |   5898   |   5.45   |      4097       |   5.46   |       903       |   5.41   |       898       |   5.46  
Defending/Explanation          |          df          |   3724   |   3.44   |      2790       |   3.72   |       531       |   3.18   |       403       |   2.45  
Expansions of y/n Answers      |          e           |   3200   |   2.96   |      2360       |   3.14   |       540       |   3.23   |       300       |   1.83  
Interrupted/Abandoned/Uninterpretable |          %           |   3103   |   2.87   |      2171       |   2.89   |       492       |   2.95   |       440       |   2.68  
Rising Tone                    |          rt          |   3101   |   2.87   |      2015       |   2.68   |       516       |   3.09   |       570       |   3.47  
Floor Grabber                  |          fg          |   3092   |   2.86   |      2076       |   2.77   |       489       |   2.93   |       527       |   3.21  
Offer                          |          cs          |   2662   |   2.46   |      1878       |   2.50   |       402       |   2.41   |       382       |   2.32  
Assessment/Appreciation        |          ba          |   2216   |   2.05   |      1605       |   2.14   |       354       |   2.12   |       257       |   1.56  
Understanding Check            |          bu          |   2091   |   1.93   |      1405       |   1.87   |       371       |   2.22   |       315       |   1.92  
Declarative-Question           |          d           |   1805   |   1.67   |      1153       |   1.54   |       350       |   2.10   |       302       |   1.84  
Affirmative Non-yes Answers    |          na          |   1112   |   1.03   |       870       |   1.16   |       133       |   0.80   |       109       |   0.66  
Wh-Question                    |          qw          |   951    |   0.88   |       630       |   0.84   |       160       |   0.96   |       161       |   0.98  
Reject                         |          ar          |   908    |   0.84   |       594       |   0.79   |       152       |   0.91   |       162       |   0.99  
Collaborative Completion       |          2           |   841    |   0.78   |       571       |   0.76   |       136       |   0.81   |       134       |   0.82  
Other Answers                  |          no          |   828    |   0.77   |       563       |   0.75   |       98        |   0.59   |       167       |   1.02  
Hold Before Answer/Agreement   |          h           |   792    |   0.73   |       474       |   0.63   |       134       |   0.80   |       184       |   1.12  
Action-directive               |          co          |   674    |   0.62   |       460       |   0.61   |       97        |   0.58   |       117       |   0.71  
Yes-No-question                |          qy          |   669    |   0.62   |       476       |   0.63   |       90        |   0.54   |       103       |   0.63  
Dispreferred Answers           |          nd          |   483    |   0.45   |       341       |   0.45   |       82        |   0.49   |       60        |   0.37  
Humorous Material              |          j           |   463    |   0.43   |       326       |   0.43   |       67        |   0.40   |       70        |   0.43  
Downplayer                     |          bd          |   387    |   0.36   |       290       |   0.39   |       68        |   0.41   |       29        |   0.18  
Commit                         |          cc          |   371    |   0.34   |       258       |   0.34   |       51        |   0.31   |       62        |   0.38  
Negative Non-no Answers        |          ng          |   351    |   0.32   |       236       |   0.31   |       56        |   0.34   |       59        |   0.36  
Maybe                          |          am          |   349    |   0.32   |       224       |   0.30   |       66        |   0.40   |       59        |   0.36  
Or-Clause                      |         qrr          |   345    |   0.32   |       216       |   0.29   |       66        |   0.40   |       63        |   0.38  
Exclamation                    |          fe          |   307    |   0.28   |       195       |   0.26   |       56        |   0.34   |       56        |   0.34  
Mimic Other                    |          m           |   293    |   0.27   |       200       |   0.27   |       48        |   0.29   |       45        |   0.27  
Apology                        |          fa          |   259    |   0.24   |       181       |   0.24   |       46        |   0.28   |       32        |   0.19  
About-task                     |          t           |   253    |   0.23   |       154       |   0.21   |       42        |   0.25   |       57        |   0.35  
Signal-non-understanding       |          br          |   236    |   0.22   |       161       |   0.21   |       39        |   0.23   |       36        |   0.22  
Accept-part                    |         aap          |   219    |   0.20   |       158       |   0.21   |       27        |   0.16   |       34        |   0.21  
Rhetorical-Question            |          qh          |   214    |   0.20   |       166       |   0.22   |       30        |   0.18   |       18        |   0.11  
Topic Change                   |          tc          |   212    |   0.20   |       127       |   0.17   |       35        |   0.21   |       50        |   0.30  
Repeat                         |          r           |   208    |   0.19   |       131       |   0.17   |       45        |   0.27   |       32        |   0.19  
Self-talk                      |          t1          |   198    |   0.18   |       120       |   0.16   |       38        |   0.23   |       40        |   0.24  
3rd-party-talk                 |          t3          |   165    |   0.15   |       105       |   0.14   |       36        |   0.22   |       24        |   0.15  
Rhetorical-question Continue   |          bh          |   154    |   0.14   |       109       |   0.15   |       26        |   0.16   |       19        |   0.12  
Reject-part                    |         bsc          |   150    |   0.14   |       94        |   0.13   |       22        |   0.13   |       34        |   0.21  
Misspeak Self-Correction       |         arp          |   150    |   0.14   |       89        |   0.12   |       18        |   0.11   |       43        |   0.26  
Reformulate/Summarize          |          bs          |   141    |   0.13   |       89        |   0.12   |       17        |   0.10   |       35        |   0.21  
"Follow Me"                    |          f           |   128    |   0.12   |       98        |   0.13   |       12        |   0.07   |       18        |   0.11  
Or-Question                    |          qr          |   127    |   0.12   |       88        |   0.12   |       17        |   0.10   |       22        |   0.13  
Thanking                       |          ft          |   119    |   0.11   |       88        |   0.12   |        9        |   0.05   |       22        |   0.13  
Tag-Question                   |          g           |    87    |   0.08   |       58        |   0.08   |        9        |   0.05   |       20        |   0.12  
Open-Question                  |          qo          |    74    |   0.07   |       49        |   0.07   |       14        |   0.08   |       11        |   0.07  
Correct-misspeaking            |          bc          |    51    |   0.05   |       29        |   0.04   |       13        |   0.08   |        9        |   0.05  
Sympathy                       |          by          |    11    |   0.01   |        5        |   0.01   |        2        |   0.01   |        4        |   0.02  
Welcome                        |          fw          |    6     |   0.01   |        5        |   0.01   |        0        |   0.00   |        1        |   0.01  

![Full Label Frequencies](mrda_data/metadata/MRDA%20Full%20Frequency%20Distributions.png)

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

Each DA label set (basic, general or full) also has:
- <*setname*>_label_freq = [Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing all data in the sets Dialogue Acts table above.
- <*setname*>_labels = List of all DA labels.
- num_<*setname*>_labels = Number of labels used from each of the label sets.

Each data set also has:
- <*setname*>_num_dialogues = Number of dialogues in the set.
- <*setname*>_max_dialogues_len = Length of the longest dialogue in the set.