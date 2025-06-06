# install.packages('jsonlite')
# Load the package
library(jsonlite)
library(tidyverse)
library(purrr)

# Import the JSON file, preserving nested structure
data <- fromJSON("~/CodeProjects/ambiData/data.json", simplifyVector = FALSE)

# Quickly inspect the structure up to 2 levels deep
# str(data, max.level = 2)

# Create a summary data frame for the top-level keys
df_summary <- data.frame(
  # 4 top-level keys
  nthParticipant  = map_chr(data, ~ as.character(pluck(.x, "nthParticipant", .default = NA))),
  studentID       = map_chr(data, ~ as.character(pluck(.x, "studentID", .default = NA))),
  results_present = map_lgl(data, ~ !is.null(.x$results)),
  survey_present  = map_lgl(data, ~ !is.null(.x$survey)),
  # keys from survey
  name            = map_chr(data, ~ as.character(pluck(.x, "survey", "page4", "name", .default = NA))),
  heardAboutStudy = map_chr(data, ~ {
    value <- as.character(pluck(.x, "survey", "page4", "heardAboutStudy", .default = NA))
    if (!is.na(value) && value == "other") {
      other_text <- as.character(pluck(.x, "survey", "page4", "otherSourceText", .default = NA))
      paste("other:", other_text)
    } else {
      value
    }
  }),
  stringsAsFactors = FALSE
)





# See how many rows submitted results: (4/20: 35!)
# (make sure that everyone after nth=13 is also submitting survey, too.) (4/20: Yep Looks good!)
# See how many students need to get paid: (4/20: 25 - Omar f0056hz + Addy Domain f0078wv)
emails <- df_summary %>%
  filter(results_present == "TRUE" | studentID == "f0078wv") %>% #  In my dataframe, "null" is actually stored as a string ("null") rather than an R NULL value.
  filter(studentID != "NA") %>%
  # get the 25 student IDs
  select(studentID) %>%
  # filter out Omar:
  filter(studentID != "f0056hz")

# Append "@Dartmouth.edu"
emails <- emails %>%
  mutate(email = paste0(studentID, "@dartmouth.edu"))
# turn into a comma-separated string
email_string <- paste(emails$email, collapse = ", ")
# cat prints the string without quotes or linebreaks
cat(email_string)
# f0079d6@dartmouth.edu, f006h7g@dartmouth.edu, f007b1k@dartmouth.edu, f006v5k@dartmouth.edu, f00790h@dartmouth.edu, f007jvc@dartmouth.edu, f007b5k@dartmouth.edu, f0079dm@dartmouth.edu, f0055vp@dartmouth.edu, f004n2c@dartmouth.edu, f0078wv@dartmouth.edu, f005697@dartmouth.edu, f004py1@dartmouth.edu, f007grq@dartmouth.edu, f0079zk@dartmouth.edu, f006g40@dartmouth.edu, f006gc7@dartmouth.edu, f00799z@dartmouth.edu, f006bv5@dartmouth.edu, f007mv1@dartmouth.edu, f007hn2@dartmouth.edu, f0070x8@dartmouth.edu, f007gnz@dartmouth.edu, f006b6p@dartmouth.edu, f0071bb@dartmouth.edu





