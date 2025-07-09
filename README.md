# ambiData 
ambiData is the data-processing repository for Luke Hafermann's Dartmouth College QSS Honors Thesis: Memory Test for Interconnected vs. Tightly-Scoped Thinking, Long Term Working Memory, and Schema Formation. There are 2 other repositories: a frontend repository called ambidextrous, and a backend repository called ambiServer. All 3 repositories are publically available at https://github.com/lukehaf. The data itself has not been pushed yet, actually, since I need to anonymize the data first. 35 participants completed the memory test, and Ambidata currently contains just the python scripts & jupyter notebooks I used to process the data.

## Step 1: Export Data from MongoDB
ambiData/1a_mongo_export.sh was used to read in participants' data from a MongoDB backend (hosted by MongoDB Atlas), and is now stored in ambiData/1b_data.json. All the data has been fetched & the Atlas backend has now been shut down.

The Cluster...tgz file is an archive (.gz) containing a binary dump of my data. It's BSON format, sufficient to spin up a local MongoDB Community instance, or I can use MongoDB's CLI tools to restore from it without even having to spin up a 
local instance.

## Step 2: Make table by participant, containing participants' survey responses
ambiData/2a_participants.py converts Step 1's 1b_data.json into a csv table, organized by participant. The nested json structure (with multiple survey pages) is flattened to facilitate later steps' usage of the outputted ambiData/2b_participants.csv as a dataframe.

## Step 3: Make accuracy table, with 24 memory-test questions per participant
ambiData/3a_accuracy.py outputs ambiData/3b_accuracy.csv, which has 24x as many rows; 24 questions x 35 participants. It also contains the 2b_participants.csv table, merged on, so that the survey responses are also available (useful as controls when predicting question accuracy).

3a_accuracy.py also contains the initial data check, which verifies that the number of rows are correct, and which counts that the Echo Task (in aggregate) had 75% accuracy while the Story Task had 70% accuracy.

## Step 4+: Jupyter Notebooks
These notebooks are what I used to generate the plots and tables included within my actual thesis document, because they enable markdown based explanation rather than commenting, and allow running of one cell at a time more easily. Each notebook is labeled according to its output (where "output" means something included in the thesis document, or a section of the thesis document).