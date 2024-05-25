import pandas as pd

def get_unique_cities(filepath):
    # Load the dataset
    df = pd.read_csv(filepath)

    # Combine 'Departure City' and 'Arrival City' into one Series
    cities = pd.concat([df['Departure City'], df['Arrival City']])

    # Get unique cities and sort them
    unique_cities = cities.unique()
    unique_cities.sort()

    return unique_cities

def save_cities_to_file(cities, output_filepath):
    # Open a file to write
    with open(output_filepath, 'w') as file:
        for city in cities:
            file.write(f"{city}\n")


if __name__ == '__main__':

    # Check for duplicate travellers
    # ------------------------------

    # Load the dataset
    df = pd.read_csv('./src/data/datasets/original_dataset.csv')

    # Check for duplicates in the 'Traveller Name' column
    duplicates = df['Traveller Name'].duplicated(keep=False)

    # Print out duplicate names, if any
    if duplicates.any():
        print('\nDuplicate travellers found:\n')
        print(df.loc[duplicates, 'Traveller Name'])
    else:
        print('\nNo duplicate travellers found.')


    # Retrieve list of all cities
    # ---------------------------

    # Define the file path to the dataset
    file_path = './src/data/datasets/original_dataset.csv'
    
    # Define the output file path for cities
    output_file_path = './src/data/datasets/cities.txt'
    
    # Retrieve the unique cities
    unique_cities = get_unique_cities(file_path)
    
    # Save the unique cities to a file
    save_cities_to_file(unique_cities, output_file_path)
    
    # Print completion message
    print(f"Unique cities have been saved.\n")
