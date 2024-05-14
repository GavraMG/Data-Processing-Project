'''

Q2_data_processing.py

Author: Markus Gavra (1277056)
Project: Milestone IV Project
Date of Last Update: April 4, 2024

Code Summary: 
    Question #4: What are the differences in job vacancies and wages between permanent and temporary positions across various quarters?
    
    Purpose: 
        - Analyzes the correlation between job vacancy numbers and employment levels in Canada.

    Command Line: 
        - python Q2_data_processing.py (year argument) path/to/dataset1.csv
    
    Process:
        - Processes data from dataset#1 
        
        Dataset #1:
        - Filters and keeps only the 'REF_DATE', 'GEO', 'Job vacancy characteristics', 'VALUE'

        Dataset #2:
        - Filters and keeps only the 'REF_DATE', 'GEO', 'Hours and wages', 'UOM', 'SCALAR_FACTOR', 'VALUE'
    
    Output:
        - Outputs filtered data to a folder named "Q2_Processed_Data".
        - The "Processed_Data" folder is used to help keep data organzied and clean


Data Citation:
    - https://www150.statcan.gc.ca/n1/en/type/data?HPA=1

Libraries Used:
    import csv
    import sys
    import os
    
'''

# Libraries
import csv
import sys
import os

# Main Function
def main(argv):
    # Checks to make sure the correct number of arguments were provided
    if len(argv) < 3:
        print("Usage: Q1_data_processing.py <year> <dataset_1_path>")
        sys.exit(1)

    # Assigns the command line arguments to variables
    year = argv[1]
    dataset_1_path = argv[2]
    output_folder = "Q2_Processed_Data"

    # Will create new folder if one is not already made
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filtered_data_1 = []
    filtered_data_2 = []

    # Headers for Dataset #1 and Dataset #2
    headers_1 = ['REF_DATE', 'GEO', 'Job vacancy characteristics', 'Statistics', 'VALUE']

    # Check if Dataset #1 file is empty
    if os.stat(dataset_1_path).st_size == 0:
        print(f"File '{dataset_1_path}' is empty. Exiting.")
        sys.exit(1)

    # Process Dataset #1
    try:
        with open(dataset_1_path, encoding="utf-8-sig") as file_data1:
            dataset1 = csv.reader(file_data1)
            for rowDataFields in dataset1:
                # Checks if the row's date starts with the year given in the argument and checks to make sure the "VALUE" column has a number
                if len(rowDataFields) >= 13:
                    date = rowDataFields[0] 
                    place = rowDataFields[1] if rowDataFields[1] else "N/A"
                    job_vacancy = rowDataFields[4] if rowDataFields[4] else "N/A"
                    stats = rowDataFields[5] if rowDataFields[5] else "N/A"
                    value = rowDataFields[12] if rowDataFields[12] else "N/A" 

                    # Filter for Permanent vacancies position
                    if year in date and "Canada" in place and "Permanent" in job_vacancy and "Job vacancies" in stats:
                        filtered_data_1.append([date, place, job_vacancy, stats, value])

                    # Filter for Temporary vacancies positions
                    elif year in date and "Canada" in place and "Temporary (seasonal and non-seasonal)" in job_vacancy and "Job vacancies" in stats:
                        filtered_data_2.append([date, place, job_vacancy, stats, value])

    # File checker
    except IOError as err:
        print(f"Unable to open file '{dataset_1_path}' : {err}", file=sys.stderr)
        sys.exit(1)


    # Writes filtered_data_1 to new CSV file that is then put in "Q2_Processed Data" folder
    output_file_1_path = os.path.join(output_folder, f"Filtered_Permanent_Data_{year}.csv")
    with open(output_file_1_path, mode = 'w', newline = '', encoding = "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers_1)         
        writer.writerows(filtered_data_1) 

    # Writes filtered_data_1 to new CSV file that is then put in "Q2_Processed Data" folder
    output_file_2_path = os.path.join(output_folder, f"Filtered_Temporary_Data_{year}.csv")
    with open(output_file_2_path, mode = 'w', newline = '', encoding = "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers_1)
        writer.writerows(filtered_data_2) 

    # Lets the user know when their data was finished processing 
    print(f"Filtered data for the year {year} has been saved to the {output_folder} folder.")

if __name__ == "__main__":
    main(sys.argv) 
