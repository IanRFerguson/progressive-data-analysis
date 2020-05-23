# READ IN WTHH DATA FROM DATA FOR PROGRESS (LOCAL DIRECTORY IN THIS CASE)
data.path <- "/Users/IanFerguson 1/Documents/ACADEMIA/03_Industry/02_Political_Future/04_Data/DFP_WTHH_release.csv"
data <- read.csv(data.path)

# PACKAGE IMPORTS
library(tidyverse)
library(likert)

# CHERRY PICK VARIABLES OF INTEREST
DFP <- data %>% 
        dplyr::select(ideo5, contains("SOCIALDOMINANCE")) %>% 
        na.omit() %>% 
        dplyr::filter(ideo5 != 6)

# RECODE FACTOR LEVELS
DFP$ideo5 <- dplyr::recode_factor(DFP$ideo5, "1" = "Very Liberal",
                                  "2" = "Liberal", "3" = "Moderate",
                                  "4" = "Conservative", "5" = "Very Conservative",
                                  "6" = "Not Sure")

# THIS NEEDS TO BE AUTOMATED ... CHANGES COLUMN VECTORS TO CHARACTER TYPES
DFP$SOCIALDOMINANCE_PRIORITIES <- as.character(DFP$SOCIALDOMINANCE_PRIORITIES)
DFP$SOCIALDOMINANCE_NOTPUSH <- as.character(DFP$SOCIALDOMINANCE_NOTPUSH)
DFP$SOCIALDOMINANCE_EQUALIDEAL <- as.character(DFP$SOCIALDOMINANCE_EQUALIDEAL)
DFP$SOCIALDOMINANCE_SUPERIOR <- as.character(DFP$SOCIALDOMINANCE_SUPERIOR)

# SKIP OVER POLITICAL ORIENTATION COLUMN
for (var in colnames(DFP)[2:5]) {
        
        # RECODE FROM NUMERIC TO QUALITATIVE RESPONSES
        DFP[, var] <- dplyr::recode_factor(DFP[, var], "1" = "Strongly Agree",
                                         "2" = "Somewhat Agree", "3" = "Neither Agree nor Disagree",
                                         "4" = "Somewhat Disagree", "5" = "Strongly Disagree")
        
        # REVERSE FACTOR LEVELS (SUCH THAT 'STRONGLY DISAGREE' == 1)
        DFP[, var] <- forcats::fct_rev(DFP[, var])
}



# REPLACE COLUMN NAMES WITH SURVEY PROMPTS
colnames(DFP) <- c("Political Orientation",
                   "In setting priorities, we must consider all groups",
                   "We should not push for group equality",
                   "Group equality should be our ideal",
                   "Superior groups should dominate inferior groups")

# APPLY 'LIKERT' FUNCTION TO SURVEY ITEMS
lik.test <- likert(items = DFP[, 2:5],
                   grouping = DFP[, 1])

# VISUALIZE RESULTS
plot(lik.test)
