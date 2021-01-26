# ------------ Imports + Environment
library(tidyverse)
library(maps)
library(tidytext)
library(lubridate)

path <- "~/DATA/01_POLITICS/04_DNC/00_Twitter/00_Assorted/Debate_0929_2020"                                     # Set local file path
setwd(path)

data <- read.csv("Debate-output.csv")                                                                           # Read in Twitter CSV

# ------------ Text Cleaning
data$Tweet <- gsub("https\\S*", "", data$Tweet)                                                                 # Filter out hyperlinks
data$Tweet <- gsub("@\\w+", "", data$Tweet)                                                                     # Filter out extra characters

reduced <- data %>% dplyr::select(Created, User.Name, Tweet, TARGET)                                            # Chop down DF to relevant columns

reduced <- reduced %>% 
        mutate(date = ymd_hms(Created)) %>%                                                                     # Convert to datetime
        mutate(minute = with_tz(floor_date(date, unit = "minute")), tzone="America/Los Angeles") %>%            # Isolate minute
        mutate(idx = row_number())                                                                              # Unique identifier / user

td.data <- reduced %>% 
        unnest_tokens(word, Tweet, token = "tweets") %>%                                                        # Tokenize words in tweet
        filter(!str_detect(word, "^[0-9]*$")) %>%                                                               # Remove extra characters
        anti_join(stop_words) %>%
        mutate(word = SnowballC::wordStem(word))                                                                

td.data <- td.data %>% 
        left_join(get_sentiments("afinn")) %>%                                                                  # Get semantic valence / word
        group_by(idx)                                                                                           # Compile sentiments / user

td.data_non <- td.data %>% 
        summarise(target=first(TARGET),
                  value=mean(value, na.rm=T),
                  minute=first(minute)) %>% na.omit()

td.data_non %>% 
        ggplot(aes(x = minute, y = value, color = target)) +
        stat_summary() +
        geom_hline(yintercept = 0, linetype = "dashed", alpha=0.75, color="grey") +
        scale_color_brewer(palette = "Set1", direction = -1) +
        theme_minimal() +
        labs(x = "",
             y = "AFINN Polarity Value",
             color = "Candidate",
             title = "Presidential Debate: Twitter Reactions",
             subtitle = "September 29, 2020",
             caption = "All times in PST | Scraped by Ian Ferguson") +
        theme(plot.title = element_text(face = "bold", hjust = 0.5),
              plot.subtitle = element_text(hjust = 0.5),
              axis.title.x = element_text(vjust=2),
              plot.caption = element_text(hjust = 0.5, face="bold"))