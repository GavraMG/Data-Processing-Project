'''

Q4_graph_creation.py

Author: Markus Gavra (1277056)
Project: Milestone IV Project
Date of Last Update: Aril 4, 2024

Code Summary: 
    Question #4: What are the differences in job vacancies and wages between permanent and temporary positions across various quarters?
    
    Purpose: 
        - Takes the filtered data and uses it to make a bar graph 

    Command Line: 
        - python Q4_graph_creation.py (year argument) path/to/dataset1.csv
    
    Process:
        - Takes the filtered data and makes a bar graph
    
    Output:
        - Takes the filtered data and makes a bar graph
        - When completed, the graph will be sent to the folder "Q4_Graphs" to help keep it organized and clean

Data Citation:
    - https://www150.statcan.gc.ca/n1/en/type/data?HPA=1

Libraries Used:
    import sys
    import os
    import pandas
    import matplotlib.pyplot
    
'''

# libraries
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Main Function
def main(year):
    
    # Double checks to make sure argv was inputted
    if len(sys.argv) != 2:
        print("Usage: python Q4_graph_creation.py <year>")
        sys.exit(1) 
    
    # Folders
    input_folder = "Q4_Processed_Data"
    output_folder = "Q4_Graphs"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # This sets the path to the filtered datasets
    permanent_file_path = os.path.join(input_folder, f"Filtered_Permanent_Data_{year}.csv")
    temporary_file_path = os.path.join(input_folder, f"Filtered_Temporary_Data_{year}.csv")
    
    # Read the data into pandas DataFrames
    permanent_data = pd.read_csv(permanent_file_path)
    temporary_data = pd.read_csv(temporary_file_path)

    # Convert 'REF_DATE' to datetime and sort the data
    permanent_data['REF_DATE'] = pd.to_datetime(permanent_data['REF_DATE'])
    temporary_data['REF_DATE'] = pd.to_datetime(temporary_data['REF_DATE'])
    permanent_data.sort_values('REF_DATE', inplace=True)
    temporary_data.sort_values('REF_DATE', inplace=True)

    # Aggregate the sums of vacancies on each date
    permanent_sums = permanent_data.groupby('REF_DATE')['VALUE'].sum().reset_index()
    temporary_sums = temporary_data.groupby('REF_DATE')['VALUE'].sum().reset_index()

    # Set the positions for the bars on the x-axis
    positions = range(len(permanent_sums))
    
    # Plot setup
    plt.figure(figsize=(10, 5))
    plt.bar(positions, permanent_sums['VALUE'], width=0.35, label='Permanent Positions', color='red')
    plt.bar([p + 0.35 for p in positions], temporary_sums['VALUE'], width=0.35, label='Temporary Positions', color='blue')

    # Axis labeling for the graph
    plt.xlabel('Date')
    plt.ylabel('Number of Vacancies')
    plt.title(f'Job Vacancies in {year}')
    plt.xticks([p + 0.35 / 2 for p in positions], permanent_sums['REF_DATE'].dt.strftime('%Y-%m'), rotation=45)

    # Legend
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Save the figure
    graph_image_output_path = os.path.join(output_folder, f"{year}_graph.png")
    plt.tight_layout()
    plt.savefig(graph_image_output_path)
    plt.close()

    # Print success message
    print(f"The bar graph has been saved to: Q4_Graphs")

# This is the starting point of the script.
if __name__ == "__main__":
    main(sys.argv[1])