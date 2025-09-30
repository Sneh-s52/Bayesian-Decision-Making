import csv
import os

def convert_to_tab_separated(input_file, output_file):
    # Dictionary to map subject names to new subject IDs
    subject_map = {}
    current_id = 1
    
    # Read the input CSV file
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        
        # Open the output file for writing
        with open(output_file, 'w') as out_f:
            # Write the header
            out_f.write("subjID\tchoice\tgain\tloss\n")
            
            # Process each row
            for row in reader:
                if len(row) < 14:  # Check if row has enough columns
                    continue
                
                subj_name = row[12]  # Name column
                
                # Map subject name to numeric ID if not already mapped
                if subj_name not in subject_map:
                    subject_map[subj_name] = current_id
                    current_id += 1  # Sequential IDs: 1, 2, 3, ...
                
                subj_id = str(subject_map[subj_name])
                # Add 1 to choice to make it start from 1 instead of 0
                choice = str(int(row[1]) + 1)
                reward = row[2]    # Reward column
                
                # Determine gain and loss
                gain = reward if int(reward) > 0 else "0"
                loss = "0" if int(reward) > 0 else "0"  # Always 0 as per requirement
                
                # Write to the output file
                out_f.write(f"{subj_id}\t{choice}\t{gain}\t{loss}\n")
                
    print(f"Conversion complete. Output saved to {output_file}")
    print(f"Subject mapping: {subject_map}")

# Example usage
input_file = "Foraging_data.csv"
output_file = "foraging_data_hBayesDM.txt"

# If the input file doesn't exist, create it first with the provided data
if not os.path.exists(input_file):
    with open(input_file, 'w', newline='') as f:
        f.write(",Patch,Reward,Time,p0,p1,p2,p3,p4,p5,p6,p7,Name,Block,subno\n")
        # Extract data from the document
        with open("document_content.txt", 'r') as doc_file:
            data = doc_file.readlines()
        for line in data:
            f.write(line)

convert_to_tab_separated(input_file, output_file)