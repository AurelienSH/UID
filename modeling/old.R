# Load the necessary libraries
library(lme4)
library(boot)
library(MuMIn)

# Set the seed for reproducibility
set.seed(123)

# Read in the dataset
data <- read.csv("data.csv")

# Fit a generalized linear mixed-effects model with a logistic link function using lme4
model <- glmer(that ~ length_matrix_verb_to_CC + length_CC_onset + length_CC_remainder +
                    position_matrix_verb + subject_form_CC_subject + frequency_CC_subject_head + word_form_similarity +
                    frequency_matrix_verb + matrix_subject + uid + (1|genre:that), data = data, family = binomial())

# Summarize the model
summary(model)

# Calculate the marginal R-squared value for the model
r2 <- r.squaredGLMM(model)

# Fit a generalized linear model with a logistic link function using glm
#model2 <- glm(that ~ length_matrix_verb_to_CC + length_CC_onset + length_CC_remainder +
#                    position_matrix_verb +
#                    subject_form_CC_subject + frequency_CC_subject_head + word_form_similarity +
#                    frequency_matrix_verb + matrix_subject , data = data, family = binomial())

# Summarize the model
#summary(model2)

# Calculate the marginal R-squared value for the model
#r2 <- r.squaredGLMM(model2)