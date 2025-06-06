def accuracy_domino_stack(results, nth_participant, names_or_objects, list_half):
    """
    assess participant's accuracy on 1 of 4 domino_stacks.
    returns a list of (5 or 7) rows, each with the accuracy boolean for one domino_pair.
    """
    # results is just the results key in the MongoDB participant doc
    domino_stack = results[names_or_objects][list_half]['recall'][0] # I'm examining just their 0th lap on the recall test. Save 1th & 2th laps for auxilliary analysis.

    # relabel "one"/"two" → "A"/"B"
    relabeled_list_half = 'A' if list_half == 'one' else 'B'
    orders = [
       'namesA namesB objectsA objectsB',
       'namesB namesA objectsB objectsA',
       'objectsA objectsB namesA namesB',
       'objectsB objectsA namesB namesA',
    ]
    replacement_map = {
        'emma': 'liam', # {'leftHalf': None, 'rightHalf': 'emma'} replace None with "liam"
        'owen': 'chloe',# {'leftHalf': None, 'rightHalf': 'owen'} replace None with "chloe"
        'leaves': 'rake', #{'leftHalf': None, 'rightHalf': 'leaves'} replace None with "rake"
        'pond': 'dryland' # {'leftHalf': None, 'rightHalf': 'pond'} replace None with "dryland"
    }

    
    rows = []
    for pair_index, pair in enumerate(domino_stack): # enumerate gives you both the index and the item. Unpack the tuple directly in the for loop header.
        accuracy = (pair['reinforcement'] is None) # Accurate responses (no IDK button) have a pair.reinforcement that remained null (and was never initialized with a reinforcement-rep object). 
        names_flag = (names_or_objects == 'names') # bool. True for names; False for objects
        wrong_submissions = len(pair['rightHalf']['wrongSubmissions']) # returns 0 if it's an empty array []. Crashes w keyError if the key doesn't exist.
        list_of_strings = [ # extract only the characters from each userEntry, join them into strings, and collect those into an array of word-strings.
            ''.join(char_obj['char'] for char_obj in submission['userEntry'])
            for submission in pair['rightHalf']['wrongSubmissions']
        ]
        # Handle special cases where left is None; (first domino_pair in every stack, unfortunately)
        right = pair['targetPair']['rightHalf']
        left = pair['targetPair']['leftHalf'] or replacement_map[right]

        rows.append({
            'accuracy': accuracy, # bool

            'names_flag': names_flag, # bool. True for names; False for objects
            'names_or_objects': names_or_objects, # 'names' or 'objects' test

            'nth_participant': nth_participant, # int (not squished down to 1-35, though).
            # 'participant_k': ,

            # inside one list-quarter, question_k needs to know pair_index, names_flag, and relabeled_list_half.
            # assign each question a unique index, using Order 0: ['namesA', 'namesB', 'objectsA', 'objectsB']. note: question_k is NOT the question index as it appeared to PARTICIPANTS. (that's only true for participants assigned order 0.)
            'question_k': (pair_index                                                 # Names 1/A begins liam emma noah.
                           + (5 if names_flag and relabeled_list_half == 'B' else 0)  # Names 2/B begins chloe owen caleb.
                           + (10 if not names_flag and relabeled_list_half == 'A' else 0)# Objects 1/A begins rake leaves stream.
                           + (17 if not names_flag and relabeled_list_half == 'B' else 0)# Objects 2/B begins dryland pond bamboo.
                           ),

            # I need to ID if the test was the 2nd one in a pair, FROM THE PERSPECTIVE OF THE PARTICIPANT.
            # So, the participant's order is very relevant. Get the participant's order via (nth_participant % 4 ). If it's order 0 or 2, A came first in the pair. (see orders list above.)
            # order is nth_participant % 4
            # case order is 0 or 2: 
                # if relabeled_list_half = 'A', interf = False
                # if relabeled_list_half = 'B', interf = True
            # case order is 1 or 3: 
                # if relabeled_list_half = 'A', interf = True
                # if relabeled_list_half = 'B', interf = False
            'interf': (relabeled_list_half == 'B') if (nth_participant % 4) in [0, 2] else (relabeled_list_half == 'A'),

            # For Thesis2025's SIMPLE qualitative analysis of missed words:
            'target_pair': f"{left}_{right}", # the pair of words they were supposed to type
            'list_of_strings': list_of_strings, # If you write a list (e.g. ['hv', 'iv', '']) into a CSV column, pandas stores it as a string.
            'pair_index': pair_index, # see if this has an effect on question difficulty
            
            # not relevant to Thesis2025
            'order': orders[nth_participant % 4], # list of strings-- what order did they take the 4 tests?
            'list_half': relabeled_list_half, # 'A' or 'B' test version (each version tests half the names or half the objects)
            'wrong_submissions': wrong_submissions # int. 0 means IDK immediately. 1+ means they typed something, then clicked IDK. (not a relevant distinction for Thesis2025; it's a flag for future analyses, to investigate the qualitative nature of the wrong_submissions, and make finding these rows easier)
        })
    return rows
##########################################################
import json
# Load the JSON file
with open('1b_data.json', 'r') as f:
    data = json.load(f) # data is a list (of nested dictionaries, one nested dictionary per participant) corresponding to the MongoDB collection of participant documents
filtered_data = [participant for participant in data if participant.get('results')] # returns just the participants with results. # .get() returns None (falsy) if participant has no results key.

all_rows = []
for participant in filtered_data: # about 35 participants
    nth_participant = participant.get('nthParticipant') # != index, since some participants were filtered out.
    results = participant.get('results')
    for names_or_objects in ('names', 'objects'):
        for list_half in ('one', 'two'):
            all_rows.extend(
                accuracy_domino_stack(results, nth_participant, names_or_objects, list_half)
            )
########################################################
# make accuracy dataframe, merge in the participant csv, save accuracy.csv
import pandas as pd
accuracy = pd.DataFrame(all_rows)

# one-to-many merge on 'nth_participant'
participants = pd.read_csv('2b_participants.csv')
accuracy = pd.merge(
    accuracy,
    participants,
    on='nth_participant',
    how='inner' # I want to bring in the participants columns, but only for participants who had results. So an inner join. All participants who had results are also a participant. Note that not all participants have the survey.
)
# save accuracy.csv
accuracy.to_csv('3b_accuracy.csv', index=False)


#########################################################
# INITIAL DATA CHECK

# wrong_submissions
# accuracy.head()
# accuracy[(accuracy['wrong_submissions'] > 0) & (accuracy['accuracy'])].shape[0]
# 270 rows typed something incorrectly
# 119 rows with a mistake and then they remember it, no idk needed.

#################### TESTING & RESULTS FROM JUST ACCURACY, NAMES_OR_OBJECTS, NTH_PARTICIPANT

# CHECK PERCENT ACCURATE ON NAMES VS OBJECTS (AGGREGATE PARTICIPANTS)
# accuracy_byType = accuracy.groupby('names_or_objects')['accuracy'].agg(['count', 'sum'])
# ^^ looks good. 350 entries on names test (10 qs, 35 participants.) 490 entries on objects test (14 qs, 35 participants.)
# accuracy_byType['pct'] = accuracy_byType['sum']/accuracy_byType['count']
# ^^ names: 75% accurate
# ^^ objects: 70% accurate. That's great! 
# Takeaways: there's a correct number of rows. Difficulty is calibrated reasonably well.
# Takeaways: the two tests have different difficulty, aggregated across participants.

#########################################################


# check how many participants got each of the 4 orders
# accuracy.groupby("order")["nth_participant"].nunique()
