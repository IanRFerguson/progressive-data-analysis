# Imports
library(tidyverse)
library(reshape2)

# Set local file path, update working directory, list files in CWD
path <- "/Users/IanFerguson 1/DATA/00/DNC/Twitter Followers/Follower Data/"
setwd(path)
files <- list.files(path, pattern = "*.csv")

# Read in first CSV file as a template
data <- read.csv(files[1])

# Loop through other files and append to template
for (i in 2:length(files)) {

        a <- read.csv(files[i])
        data <- rbind(data, a)
}

# Drop first column (unneccesary)
data <- data[, 2:length(colnames(data))]

# Melt data ... use "Date" as grouping variable
tall.data <- melt(data)

# Plot distribution of Twitter followers for a given day ... clear nod to Bernard
tall.data %>%
        group_by(variable) %>%
        filter(Date == "02/16/20") %>% 
        ggplot(aes(x = Date, y = value, fill = variable)) +
        geom_bar(stat = "identity", position = "dodge") +
        scale_fill_brewer(palette = "Greens", direction = -1) +
        theme_minimal()

# Create new variable `twitter.increase` ... plot increaes in Twitter followers over the time period listed
tall.data %>% 
        group_by(variable) %>% 
        summarise(twitter.increase = (max(value) - min(value))) %>% 
        ggplot(aes(x = reorder(variable, +twitter.increase), 
                   y = twitter.increase, 
                   fill = variable)) +
        geom_col() +
        scale_fill_brewer(direction = -1) +
        labs(x = "", y = "Increase in Twitter Followers") +
        coord_flip() + 
        theme_minimal() +
        theme(legend.position = "")


        
