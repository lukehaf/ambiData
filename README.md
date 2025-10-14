# ambiData 
ambiData is the data-processing repository for Luke Hafermann's Dartmouth College QSS Honors Thesis: Memory Test for Interconnected vs. Tightly-Scoped Thinking, Long Term Working Memory, and Schema Formation. There are 2 other repositories: a frontend repository called ambidextrous, and a backend repository called ambiServer. All 3 repositories are publically available at https://github.com/lukehaf. The frontend (website) is publically hosted at https://ambidextrous.app. For my thesis-submission, I am submitting just the ambiData repository as a zip file, since I am supposed to submit my data & data-analysis code. Note that this zip-file should not yet be made publically available, since it has not yet been anonymized. Here is the data contained which might be sensitive: 35 participants completed the memory test, and it contains their student ID (their f00 email) as an identifier, along with a potentially-sensitive questionnaire including a question on any cognition-related diagnoses. The public Ambidata repository currently contains just the python scripts & jupyter notebooks I used to process the data; I plan to push the anonymized data to the public repository once I have anonymized it, in order to have all 3 repositories publically available for other researchers, and as a portfolio-piece of my work.

## Step 1: Export Data from MongoDB
ambiData/1a_mongo_export.sh was used to read in participants' data from a MongoDB backend (hosted by MongoDB Atlas), and is now stored in ambiData/1b_data.json. All the data has been fetched & the Atlas backend has now been shut down.

The 1c_Cluster...tgz file is an archive (.gz) containing a binary dump of my data. It's BSON format, sufficient to spin up a local MongoDB Community instance, or I can use MongoDB's CLI tools to restore from it without even having to spin up a 
local instance.

The 1d_rPipeline.r script was used to monitor the data as it rolled in, as more participants took the memory test & submitted results. It was useful for tracking the number of participants who submitted valid results, until the funding-cap of 25 (paid) participants was reached. (35 participants were reached in total, thanks to responses from friends and family.) It was also useful for extracting the list of emails to send to Drew Coombs so participants could receive compensation for participating. It was written in r only because at the time I was still more fluent in r than python.

## Step 2: Make table by participant, containing participants' survey responses
ambiData/2a_participants.py converts Step 1's 1b_data.json into a csv table, organized by participant. The nested json structure (with multiple survey pages) is flattened to facilitate later steps' usage of the outputted ambiData/2b_participants.csv as a dataframe.

## Step 3: Make accuracy table, with 24 memory-test questions per participant
ambiData/3a_accuracy.py outputs ambiData/3b_accuracy.csv, which has 24x as many rows; 24 questions x 35 participants. It also contains the 2b_participants.csv table, merged on, so that the survey responses are also available (useful as controls when predicting question accuracy).

3a_accuracy.py also contains the initial data check, which verifies that the number of rows are correct, and which counts that the Echo Task (in aggregate) had 75% accuracy while the Story Task had 70% accuracy.

## Step 4: Generate SLR scatterplot of participants' accuracy on the Echo Task vs. Story Task
ambiData/4a_SLR_accuracy_scatterplot.py generates one of the 3 Results Section scatterplots. It outputs this scatterplot as a file called 4c_SLR.pdf. The first step of the script is to generate a scatterplot of participant accuracy. The second step is to run an SLR regression on these points. The third step is to add the regression's regression line to the the scatterplot, and output the pdf.

ambiData/4b_SLR_accuracy_scatterplot.ipynb does the exact same thing, but the script is a Jupyter Notebook to make plotting & commenting more convenient.

## Step 5: Build LMR model (Model 2). Consider 4 predictor variables ("accuracy", "names_flag", "nth_participant", and "question_k") via LRTs for full vs. reduced model.
ambiData/5a_LMR_accuracy_names_participant.py builds the first LMR model using pymer. It evaluates whether an initial 3 predictors significantly improve fit (for accuracy, the predicted variable), and thus if they are worth including in the model. It does this via a series of Likelihood Ratio Tests on the full vs. reduced model, each of which outputs a Chi2 statistic. No plots are generated; just this series of Chi2 statistics. The script needs to be run for each separate test of a full vs. reduced model. The model_full = Lmer(...); model_reduced = Lmer(...) syntax makes it easy to run the script multiple times, including various combinations of the 4 predictor variables as desired.

## Step 6: Expand LMR model (Model 3). Consider 3 additional predictor variables ("page1_age", "sleep_freshBefore", and "interf") via LRTs for full vs. reduced model.
ambiData/6a_LMR_accuracy_sleep_interf.py expands the above LMR model. Just "accuracy", "names_flag", and "nth_participant" are kept from the above LMR model. The 3 additional predictor variables ("page1_age", "sleep_freshBefore", and "interf") are similarly examined using Likelihood Ratio Tests, to see if they are worth adding to the model. (sleep_freshBefore is kept as control for sleep. Separately, interf allows analyzing the pattern of proactive interference between the 4 test sections.)

## Step 7: Generate 2 LMR scatterplots (before & after controlling for sleep)
ambiData/7a_LMR_scatter.py produces an LMR scatterplot before controlling for sleep, ambiData/7b_LMR_scatter_sleep.py produces the LMR scatterplot which controlls for sleep. (The plots do not get written to a file; I simply copied them into my thesis document from my VSCode IDE. They could easily be written to a file, like in script 4a.)

## Step 8: Jupyter Notebook, for retrieving (and initial filtering) all the Incorrect Responses entered by Participants. (All of the Data-processing relevant for H2 is contained here.)
The Incorrect Responses were subsequently manually coded by their source and type, and entered (in tabular form) into a confusion-matrix inspired table design, formatted manually within the Thesis main Overleaf document. 
ambiData/8a_story_mistake_types_by_question_and_participant.ipynb is the only script out of all these which still feels messy and unrefined. There is one unused portion where I generated a bar plot of the percent accuracy by question, rather than participant (as was the focus of H1). I ended up addressing H2 by showing the errors themselves within a table, since this allowed better visualization of the sources of intrusion errors, rather than by using the 1-dimensional accuracy metric conveyed by a bar plot. There is also an initial attempt at a python Confusion Matrix before I developed the final table-design which accomplishes that while also showing the errors themselves and conveying additional, more-qualitative information about error type.

