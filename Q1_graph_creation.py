'''

Q1_graph_creation.py

Author: Markus Gavra (1277056)
Project: Milestone IV Project
Date of Last Update: April 4, 2024

Code Summary: 
    
    Question 1: How do changes in job vacancy numbers relate to employment levels in Canada, and can we observe 
                any trends that suggest a direct correlation between the number of job vacancies and the total 
                number of employees? 
    
    Purpose: 
        - Takes the filtered data and uses it to make a graph 

    Command Line: 
        - python Q1_graph_creation.py (year argument) path/to/dataset1.csv 
    
    Process:
        - Takes the filtered data and makes a dual line graph with it
    
    Output:
        - Takes the filtered data and makes a dual-axis graph
        - When completed, the graph will be sent to the folder "Q1_Graphs" to help keep it organized and clean

Data Citation:
    - https://www150.statcan.gc.ca/n1/en/type/data?HPA=1

Libraries Used:
    import sys
    import os
    import pandas
    import matplotlib.pyplot
    
'''

# Libraries 
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Main Function
def main(year):

    # Double checks to make sure argv was inputted
    if len(sys.argv) != 2:
        print("Usage: Q1_graph_creation.py <year>")
        sys.exit(1)

    # Folders
    input_folder = "Q1_Processed_Data"
    graphs_folder = "Q1_Graphs"
    
    # This will make a folder for the graphs to be stored in
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    # This sets the path to the filtered datasets
    filtered_file_1_path = os.path.join(input_folder, f"Filtered_Data_Dataset1_{year}.csv")
    filtered_file_2_path = os.path.join(input_folder, f"Filtered_Data_Dataset2_{year}.csv")
    
    # Pandas is used to read the filtered Data
    df1 = pd.read_csv(filtered_file_1_path)
    df2 = pd.read_csv(filtered_file_2_path)

    # This Aggregates dataset#1 & datset#2 
    df1_total = df1.groupby(['REF_DATE', 'GEO'])['VALUE'].sum().reset_index()
    df2_total = df2.groupby(['REF_DATE', 'GEO'])['VALUE'].sum().reset_index()

    # Merge the total values on 'REF_DATE' and 'GEO'
    merged_df = pd.merge(df1_total, df2_total, on=['REF_DATE', 'GEO'], suffixes=('_vacancies', '_employment'))
    
    # Sort the merged DataFrame by 'REF_DATE'
    merged_df.sort_values('REF_DATE', inplace=True)
    
    # 'VALUE_vacancies' will be expressed in thousands on the graph
    merged_df['VALUE_vacancies'] = merged_df['VALUE_vacancies'] / 1000
    
    # Begins the dual-axis line graph
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # First plots the job vacancies data on the primary y-axis
    color = 'tab:red'
    ax1.set_xlabel('Year Timeline')
    ax1.set_ylabel('Job Vacancies', color=color)
    ax1.plot(merged_df['REF_DATE'], merged_df['VALUE_vacancies'], color=color, marker='o', label='Job Vacancies')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=45)

    # Plotting total employment numbers on secondary y-axis
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Total Employment Numbers', color=color)
    ax2.plot(merged_df['REF_DATE'], merged_df['VALUE_employment'], color=color, marker='s', label='Employment Numbers')
    ax2.tick_params(axis='y', labelcolor=color)

    # Graph title
    plt.title('Job Vacancies and Total Employees Over Time')

    # Legend for the graph
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='best')

    # Save the plot as an image file in the "Q1_Graphs" folder
    graph_image_output_path = os.path.join(graphs_folder, f"{year}_graph.png")
    plt.tight_layout()
    plt.savefig(graph_image_output_path)
    plt.close()

    # Lets the user know when the graph has been created
    print(f"The dual axis graph image has been saved to: Q1_Graphs")

if __name__ == "__main__":
    main(sys.argv[1])