# Load the necessary libraries
library(lme4)
library(boot)
library(MuMIn)

# Set the seed for reproducibility
set.seed(123)

args <- commandArgs(trailingOnly = TRUE)

uid_type <- args[1]

# Read in the dataset
data <- read.csv("gpt_gum_nofrac.csv")


# Fit a generalized linear model with a logistic link function using glm
model <- glm(that_omission ~ 
                    length_CC_onset + 
                    length_CC_remainder +
                    position_matrix_verb + 
                    subject_form_CC_subject1v2 +
                    subject_form_CC_subject1v3 + 
                    subject_form_CC_subject1v4 + 
                    frequency_CC_subject_head + 
                    word_form_similarity +
                    frequency_matrix_verb + 
                    matrix_subject1v2 +
                    matrix_subject1v3 +
                    matrix_subject1v4 +
                    data[[paste0("uid_", uid_type)]]
                    , data = data, family = binomial())


# Summarize the model
summary(model)

#  Calculate the marginal R-squared value for the model
r2 <- r.squaredGLMM(model)