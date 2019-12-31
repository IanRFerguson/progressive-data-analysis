library(tidyverse)

# Load in "WTHH" data set from Data For Progress + YouGov Blue
# Data available @ https://wthh.dataforprogress.org/

setwd("~/DATA/DFP/")
data <- read.csv("DFP_WTHH_release.csv")
attach(data)

# Recode factor levels for state
data$state <- recode(.x = data$state, '1' = "Alabama", '2' = "Alaska", '4' = "Arizona", '5' = "Arkansas", 
                     '6' = "California", '8' = "Colorado", '9' = "Connecticut", '10' = "Deleware", 
                     '11' = "D.C.", '12' = "Florida", '13' = "Georgia", '15' = "Hawaii", '16' = "Idaho", 
                     '17' = "Illinois", '18' = "Indiana", '19' = "Iowa", '20' = "Kansas", '21' = "Kentucky", 
                     '22' = "Louisiana", '23' = "Maine", '24' = "Maryland", '25' = "Massachusetts", '26' = "Michigan", 
                     '27' = "Minnesota", '28' = "Mississippi", '29' = "Missouri", '30' = "Montana", '31' = "Nebraska", 
                     '32' = "Nevada", '33' = "New Hampshire", '34' = "New Jersey", '35' = "New Mexico", '36' = "New York", 
                     '37' = "North Carolina", '38' = "North Dakota", '39' = "Ohio", '40' = "Oklahoma", '41' = "Oregon", 
                     '42' = "Pennsylvania", '44' = "Rhode Island", '45' = "South Carolina", '46' = "South Dakota", 
                     '47' = "Tennessee", '48' = "Texas", '49' = "Utah", '50' = "Vermont", '53' = "Virginia", 
                     '51' = "Washington", '54' = "West Virginia", '55' = "Wisconsin", '56' = "Wyoming", 'District of Columbia' = "D.C.")

data$ideo5 <- as.factor(data$ideo5)
data$ideo5 <- recode(.x = data$ideo5, '1' = "Very Liberal", '2' = "Liberal",
                         '3' = "Moderate", '4' = "Conservative", '5' = "Very Conservative")

# We're interested primarily in ideological factors that accompany (or inform) ideological cognition and political party affiliation
# We'll select several variables of interest from the large WTHH data set ... most of these pretain to demographic change and social initiatives

ideology <- data %>%
        select(state, ideo5, CUSTOMS, SPEAK, ENRICH, SERVICES, JOBS, 
               fear_of_demographic_change_scaled, fear_of_demographic_change_raw,
               PATH, BORDER, DEPORT,
               SOCIALDOMINANCE_PRIORITIES, SOCIALDOMINANCE_SUPERIOR, SOCIALDOMINANCE_NOTPUSH, SOCIALDOMINANCE_EQUALIDEAL,
               POP_2, ICE, GREENJOB, PUBLICGEN, FREECOLL, M4A, pid3,
               educ2, educ4, age5) %>% 
        filter(ideo5 != 6)

# fear_of_demographic_change_raw consists of summed responses from ENRICH, SERVICES, JOBS (ENRICH reverse coded)

ideology %>% 
        ggplot(aes(x = fear_of_demographic_change_raw)) +
        geom_histogram(binwidth = 1, color = 'white') +
        labs(x = "Fear of Social Change", y = "")

# Lots of score '0' ... let's take a closer look
ideology %>% 
        filter(fear_of_demographic_change_raw == 0) %>% 
        select(state, ideo5, ENRICH, SERVICES, JOBS)

# Majority of responses driven by ideology (low fear of social change)
# We'll omit responses of "Not Sure" across all three variables

ideology <- ideology %>% 
        filter(ENRICH != 6 & SERVICES != 6 & JOBS != 6)

ideo.clean <- na.omit(ideology)
dim(ideo.clean)

# Left with 2781 responses - still robust
ideo.clean %>% 
        group_by(ideo5) %>% 
        summarise(sample = n())

# We observe a balanced ratio of Liberals / Conservatives
# Calculating sample-wide fear of social change
grand.mean <- mean(ideo.clean$fear_of_demographic_change_raw, na.rm = T)

# We'll explore state-wise differences in fear of social change
statewise <- ideo.clean %>% 
                group_by(state) %>% 
                summarise(state.mean.fear = mean(fear_of_demographic_change_raw, na.rm = T),
                  state.fear.diff = state.mean.fear - grand.mean,
                  dems = sum(ideo5 == "Liberal") + sum(ideo5 == "Very Liberal"),
                  cons = sum(ideo5 == "Conservative") + sum(ideo5 == "Very Conservative")) %>% 
                mutate(state.ideo = ifelse(dems >= cons, "D", "R"))

statewise %>% 
        ggplot(aes(x = reorder(state, +state.fear.diff), y = state.fear.diff, fill = state.ideo)) +
        geom_col() +
        coord_flip() +
        labs(x = "State", y = "Average Fear of Social Change") +
        scale_fill_brewer(palette = "Set1", direction = -1)

# This provides further evidence for ideological trends observed at individual level
cor(statewise$state.fear.diff, statewise$dems)
