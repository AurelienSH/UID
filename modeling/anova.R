# Load the necessary libraries
library(lme4)
library(boot)
library(MuMIn)

# Set the seed for reproducibility
set.seed(123)

args <- commandArgs(trailingOnly = TRUE)

# Read in the dataset
data <- read.csv("GUMdata_all_nofrac.csv")

uid_types <- c("amp", "avgStep", "biggestStep", "var")

models <- list()

for (uid_typeA in uid_types){
  # Fit a generalized linear model with a logistic link function using glm
  modelA <- glm(that_omission ~ 
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
                  data[[paste0("uid_", uid_typeA)]],
                data = data, family = binomial())
  
  for (uid_typeB in uid_types[!uid_types == uid_typeA]){
    modelB <- glm(that_omission ~ 
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
                    data[[paste0("uid_", uid_typeB)]],
                  data = data, family = binomial())
    
    print(uid_typeA)
    print(uid_typeB)
    
    # Compare the models using the likelihood ratio test (LRT)
    anova_results <- anova(modelA, modelB, test = "LRT")
    print(anova_results)
  }
}

