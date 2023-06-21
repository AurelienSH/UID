#!/bin/bash

# Retrieve the output folder argument
output_folder=$1

# Define the types of uids to run
uids=("var" "igauche2_2" "jaeger" "iphrase" "biggestStep" "idoc" "amp" "avgStep")

# Loop through the uids and run the R script for each type
for uid_type in "${uids[@]}"
do
  echo "Running R script for uid type: $uid_type"
  Rscript uid_model_mixed.R "$uid_type" > "$output_folder/$uid_type.txt"
done
