#Agent Factory Test File Creator
#Creates test case files for agent factory

#Author: Erik Connerty
#Date: 6/14/2023
#For the USC AI - Institute

import params
import random
import numpy as np

import csv

#Code to generate a basic agent file
def generate_basic_agent_file(filename, num_records):
    headers = ['id', 'type', 'country', 'county', 'municipality', 'latitude', 'longitude', 'gender', 'age', 'language', 'nationality', 'political_spectrum', 'socioeconomic_status', 'eu', 'nato_donovia', 'soldier_type', 'triad_stack_id', 'simulation_id']
    
    # Define some sample data for each field
    types = ['basic']
    countries = ['belarus']
    counties = ['vitebsk', 'oshmyany']
    municipalities = ['elektrenai', 'dofolsky']
    latitudes = [55.168346, 54.553097]
    longitudes = [27.627179, 26.047517]
    genders = ['male', 'female']
    ages = ['middle', 'old', 'young']
    languages = ['both_lang', 'donovian_lang']
    nationalities = ['donovian']
    political_spectrums = ['center', 'right', 'left']
    socioeconomic_statuses = ['lower_class', 'middle_class', 'upper_class']
    eus = ['anti_eu']
    nato_donovias = ['proNato']
    soldier_types = ['none']
    
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

#Code to create an adjacency matrix
def generate_adjacency_matrix(filename, num_agents, num_sources, connectivity_level, trust_threshold,trust_stddev=0.1):
    # Generate IDs for agents and info sources
    agent_ids = [f'B-ID-{i}' for i in range(1, num_agents + 1)]
    source_ids = [f'test{i}' for i in range(1, num_sources + 1)]
    
    # Initialize the adjacency matrix
    matrix = [[0 for _ in range(num_agents + num_sources)] for _ in range(num_agents + num_sources)]
    
    # Fill in the agent-to-agent connections
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            trust_score = np.random.normal(trust_threshold, trust_stddev)
            trust_score = min(max(trust_score, 0), 1)  # clip the trust score to the 0-1 range
            trust_score = round(trust_score, 2)  # round to two decimal places
            matrix[i][j] = matrix[j][i] = trust_score
    
    # Fill in the agent-to-source and source-to-agent connections
    for i in range(num_agents):
        for j in range(num_agents, num_agents + num_sources):
            if random.random() <= connectivity_level:
                connection_score = 1 
            else:
                connection_score = 0
            matrix[i][j] = matrix[j][i] = connection_score
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        
        # Write header row
        writer.writerow([''] + agent_ids + source_ids)
        
        # Write each row of the matrix
        for i, row in enumerate(matrix):
            writer.writerow([agent_ids[i] if i < num_agents else source_ids[i - num_agents]] + row)

def generate_information_packets(filename, num_records, avg_sentiment, num_topics):
    headers = ['Type', 'Document ID', 'Information Source ID', 'Topic ID', 'IP-id', 'Stance']
    types = ['IPs']
    sources = ['delfi.lt', 'vz.lt', 'lrt.lt', 'sputniknews.com', 'lenta.ru']
    all_topics = ['International response to Donovian invasion', 'Lithuanian response to Donovian invasion', 'Humanitarian aid by NATO', 'Censorship of media by Donovia', 'Donovian military activity in Lithuania', 'Donovian invasion of Lithuania', 'Civil protests against Donovia', 'IDPs migrate as a result of war', 'NATO shelter in place messaging', 'Article 5 invoked by NATO', 'Criminal activity in Lithuania']
    topics = random.sample(all_topics, num_topics)
    stances = list(np.random.normal(avg_sentiment, 1, num_records)) # generate stances with normal distribution around avg_sentiment

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(1, num_records + 1):
            row = [
                types[0],
                521500 + i,
                random.choice(sources),
                random.choice(topics),
                80 + i,
                round(stances[i-1]) # round to nearest integer
            ]
            writer.writerow(row)


# Generate a source file with 4 records
generate_info_source_file('./test-files/InfoDissAgents.csv', params.NUM_OF_INFO_SOURCES)

# Generate a test file with 10 records
generate_basic_agent_file('./test-files/basicAgentsInput.csv', params.NUM_OF_AGENTS)

# Generate an adjacency matrix with 10 agents and 4 info sources, 50% connectivity level, and 0.5 trust threshold
generate_adjacency_matrix('./test-files/adjacency_matrix.csv', params.NUM_OF_AGENTS, params.NUM_OF_INFO_SOURCES, params.CONNECTIVITY_LEVEL, params.TRUST_THRESHOLD,params.TRUST_STD_DEV)

# Generate a CSV file with 10 packets, average sentiment of 0, and 2 unique topics
generate_information_packets('./test-files/IPsInput_tick_1.csv', params.NUM_OF_PACKETS, params.AVERAGE_SENTIMENT, params.UNIQUE_TOPICS)