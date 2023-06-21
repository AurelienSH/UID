# Load the necessary libraries
library(lme4)
library(boot)
library(MuMIn)

# Set the seed for reproducibility
set.seed(123)

args <- commandArgs(trailingOnly = TRUE)



# Read in the dataset
data <- read.csv("GUMdata_all.csv")

# # Fit a generalized linear mixed-effects model with a logistic link function using lme4
# model <- glmer(that_omission ~ length_matrix_verb_to_CC + length_CC_onset + length_CC_remainder +
#                     position_matrix_verb + subject_form_CC_subject1v2 + subject_form_CC_subject1v3 + subject_form_CC_subject1v4 + frequency_CC_subject_head + word_form_similarity +
#                     frequency_matrix_verb + matrix_subject1v2 + matrix_subject1v3 + matrix_subject1v4 + uid_amp + (1|genre), data = data, family = binomial())

# # Summarize the model
# summary(model)

# # Calculate the marginal R-squared value for the model
# r2 <- r.squaredGLMM(model)

# position_matrix_verb
# length_matrix_verb_to_CC
# length_CC_onset
# length_CC_remainder
# subject_form_CC_subject1v3
# frequency_matrix_verb
# matrix_subject1v2
# frequency_CC_subject_head
# that_omission
# matrix_subject1v3
# subject_form_CC_subject1v4
# matrix_subject1v4
# word_form_similarity
# subject_form_CC_subject1v2
# uid_var
# uid_igauche2_2
# uid_var
# uid_jaeger
# uid_iphrase
# uid_biggestStep
# uid_idoc
# uid_amp
# uid_avgStep

# Fit a generalized linear model with a logistic link function using glm
model2 <- glm(that_omission ~ 
                    # length_matrix_verb_to_CC + 
                    length_CC_onset + 
                    # length_CC_remainder +
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
                    # uid_var
                    # uid_igauche2_2
                    # uid_jaeger
                    # uid_iphrase
                    # uid_biggestStep
                    # uid_idoc
                    # uid_amp
                    uid_avgStep
                    , data = data, family = binomial())

# Summarize the model
summary(model2)

#  Calculate the marginal R-squared value for the model
r2 <- r.squaredGLMM(model2)