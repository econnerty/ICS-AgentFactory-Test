#Agent Factory Test File Creator
#Creates test case files for agent factory

#Author: Erik Connerty
#Date: 6/14/2023
#For the USC AI - Institute

import pandas as pd
import numpy as np
import params
from tqdm.auto import tqdm
import random

import csv

#Code to generate a basic agent file
def generate_basic_agent_file(filename, num_records):
    headers = ['id', 'type', 'country', 'county', 'municipality', 'latitude', 'longitude', 'gender', 'age', 'language', 'nationality', 'political_spectrum', 'socioeconomic_status', 'eu', 'nato_donovia', 'soldier_type', 'triad_stack_id', 'simulation_id']
    
    # Define some sample data for each field
    types = ['donovian']
    countries = ['belarus']
    counties = ['vitebsk', 'oshmyany']
    municipalities = ['33_dtg', '52_dtg']
    latitudes = [55.168346, 54.553097]
    longitudes = [27.627179, 26.047517]
    genders = ['male', 'female']
    ages = ['middle', 'old', 'young']
    languages = ['both_lang', 'donovian_lang']
    nationalities = ['donovian']
    political_spectrums = ['center', 'right', 'left']
    socioeconomic_statuses = ['lower_class', 'middle_class', 'upper_class']
    eus = ['anti_eu']
    nato_donovias = ['anti_nato_pro_donovia']
    soldier_types = ['conscript_soldier', 'contract_nco']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='~')
        writer.writerow(headers)
        for i in range(1, num_records + 1):
            row = [
                f'B-ID-{i}',
                types[i % len(types)],
                countries[i % len(countries)],
                counties[i % len(counties)],
                municipalities[i % len(municipalities)],
                latitudes[i % len(latitudes)],
                longitudes[i % len(longitudes)],
                genders[i % len(genders)],
                ages[i % len(ages)],
                languages[i % len(languages)],
                nationalities[i % len(nationalities)],
                political_spectrums[i % len(political_spectrums)],
                socioeconomic_statuses[i % len(socioeconomic_statuses)],
                eus[i % len(eus)],
                nato_donovias[i % len(nato_donovias)],
                soldier_types[i % len(soldier_types)],
                '',  # triad_stack_id
                ''  # simulation_id
            ]
            writer.writerow(row)

#Code to create some info sources   
def generate_info_source_file(filename, num_records):
    headers = ['id', 'type', 'source']
    
    # Define some sample data for each field
    ids = [f'test{i}' for i in range(1, num_records + 1)]
    types = ['information-diss-agents']
    sources = ['tv', 'internet', 'radio']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='~')
        writer.writerow(headers)
        
        for i in range(num_records):
            row = [
                ids[i % len(ids)],
                types[i % len(types)],
                sources[i % len(sources)]
            ]
            writer.writerow(row)


#Code to create a random adjacency matrix
def generate_adjacency_matrix(filename, num_agents, num_sources):
    # Generate IDs for agents and info sources
    agent_ids = [f'B-ID-{i}' for i in range(1, num_agents + 1)]
    source_ids = [f'test{i}' for i in range(1, num_sources + 1)]
    
    # Initialize the adjacency matrix
    matrix = [[0 for _ in range(num_agents + num_sources)] for _ in range(num_agents + num_sources)]
    
    # Fill in the agent-to-agent connections
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            matrix[i][j] = matrix[j][i] = round(random.random(),2)
    
    # Fill in the agent-to-source and source-to-agent connections
    for i in range(num_agents):
        for j in range(num_agents, num_agents + num_sources):
            matrix[i][j] = matrix[j][i] = random.choice([0, 1])
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        
        # Write header row
        writer.writerow([''] + agent_ids + source_ids)
        
        # Write each row of the matrix
        for i, row in enumerate(matrix):
            writer.writerow([agent_ids[i] if i < num_agents else source_ids[i - num_agents]] + row)



# Generate a source file with 4 records
generate_info_source_file('./test-files/InfoDissAgents.csv', params.NUM_OF_INFO_SOURCES)

# Generate a test file with 10 records
generate_basic_agent_file('./test-files/basicAgentsInput.csv', params.NUM_OF_AGENTS)

# Generate an adjacency matrix with 10 agents and 4 info sources
generate_adjacency_matrix('./test-files/adjacency_matrix.csv', params.NUM_OF_AGENTS, params.NUM_OF_INFO_SOURCES)