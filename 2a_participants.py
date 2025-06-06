import json
import pandas as pd

# Load the JSON file
with open('1b_data.json', 'r') as f:
    data = json.load(f) # data is a list (of nested dictionaries, one nested dictionary per participant) corresponding to the MongoDB collection of participant documents

# Build list of dictionaries, as precursor to dataframe
participants_list = []

for participant in data: # each participant is a nested dictionary
    # 4 TOP-LEVEL KEYS (each MongoDB document has 4 top-level keys)
    nth_participant = participant.get('nthParticipant')
    student_id = participant.get('studentID', None) # in Python, None is a special constant that signifying the intentional absence of a value. Pass it as get's 2nd argument, so that missing values get replaced by None. Pandas actually converts it to NaN. Whatever. 
    results_present = 'results' in participant and participant['results'] is not None # returns True if the key 'results' exists in the participant dictionary; also checks that its value is not None
    survey_present = 'survey' in participant and participant['survey'] is not None

    # UNPACK SURVEY DATA:
    if survey_present:
        survey_flat = ( # goal: a flat dictionary of all survey keys, unpackable via **survey_flat inside append({}) later on
            pd.json_normalize(
                participant['survey'], # participant['survey'] returns a nested dictionary: {'page1':, 'page2':, 'page3':, 'page4':}
                sep='_' # json_normalize() flattens the nested dict into a 1-row dataframe, with colnames concatenated from 2 keys (eg 'page1_major')
            ).to_dict(orient='records')[0] # turns it back into a dict, now flat and unpackable. # .to_dict(orient='records') creates a list from the df, with a dict for each row. [0] gets just the first dictionary.
        )
    else:
        survey_flat = {}  # No survey data to unpack

    participants_list.append({
        'nth_participant': nth_participant,
        'student_id': student_id,
        'results_present': results_present,
        'survey_present': survey_present,
        # ^^ manually listing keys is fine for the first 4, but gets tedious for the MANY flattened survey keys:
        **survey_flat, # dict-unpacking is shallow. It's like the spread operator in js.
        # page1_ age, major1, major2, major3, preMed, athlete, occupation1, occupation2
        # page2_ sleep, freshBefore, freshAfter
        # page3_ ADHD, dyslexia, autism, OCD, anxiety, otherDiagnosis, otherDiagnosisText
        # page4_ heardAboutStudy, otherSourceText, name
    })

# Create the DataFrame
participants = pd.DataFrame(participants_list)

# Make composite column for sleep and freshBefore (freshAfter not used)
# recode page2_sleep [good][neutral][poor] as 1, 0, -1.
# participants.groupby("page2_sleep")["page2_sleep"].unique()
participants["sleep"] = participants["page2_sleep"].map({
    "good": 1,
    "neutral": 0,
    "poor": -1
})
# participants.groupby("page2_freshBefore")["page2_freshBefore"].unique()
participants["freshBefore"] = participants["page2_freshBefore"].map({
    "fresh": 1,
    "neutral": 0,
    "fatigued": -1
})

participants["sleep_freshBefore"] = participants["sleep"] + participants["freshBefore"]
# Centroiding sleep:
# Grand‐mean centering (sleep_c = sleep_freshBefore – mean(sleep_freshBefore)) is almost always recommended. It makes the intercept interpretable as the expected log‐odds at average sleep, and it prevents collinearity with the random intercept.
participants["sleep_freshBefore_c"] = participants["sleep_freshBefore"] - participants["sleep_freshBefore"].mean()

participants.to_csv('2b_participants.csv', index=False)

# should I remove this participant? They scored 1 on the Story Task. Do they report being sleep? Yes. So nope, I should
# not remove them.
# print(participants[participants["nth_participant"] == 46].to_dict(index=False))