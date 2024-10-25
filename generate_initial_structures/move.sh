#!/bin/bash

# Define the destination directory
DEST_DIR="../bstates"

# Check if the bstates directory exists, if not create it
if [ ! -d "$DEST_DIR" ]; then
  mkdir "$DEST_DIR"
  echo "Directory $DEST_DIR created."
fi

# Loop through files prod1.rst to prod10.rst
for x in {1..10}; do
  # Pad the number to two digits, e.g., "01", "02", ..., "10"
  SUB_DIR=$(printf "%02d" "$x")
  
  # Create subdirectory in the bstates directory if it doesn't exist
  if [ ! -d "$DEST_DIR/$SUB_DIR" ]; then
    mkdir "$DEST_DIR/$SUB_DIR"
    echo "Subdirectory $DEST_DIR/$SUB_DIR created."
  fi
  
  # Define the filename to move
  FILE="prod${x}.rst"
  
  # Check if the file exists and move it to the subdirectory
  if [ -f "$FILE" ]; then
    #cp "$FILE" "$DEST_DIR/$SUB_DIR/bstate.ncrst"
    cp "$FILE" "$DEST_DIR/$SUB_DIR"
    echo "$FILE copied to $DEST_DIR/$SUB_DIR."
  else
    echo "$FILE does not exist."
  fi
done
