import pandas as pd
import numpy as np
np.random.seed(0)

# Load dataset
df = pd.read_csv('./src/data/datasets/original_dataset.csv')

# Define data options
with open('./src/data/datasets/companies.txt', 'r') as file:
    companies_list = [line.strip() for line in file]
moods = ['Relaxation', 'Sightseeing', 'Adventure', 'Any']
times = ['Mornings', 'Evenings']
hotels = ['Hilton Hotel', 'The Hotel', 'Ibis Hotel', 'Elite Hotel', 'Novotel']

# Generate a company column
df['company'] = np.random.choice(companies_list, size=len(df))

# Generate a networking column
df['networking'] = np.random.choice([True, False], size=len(df))

# Generate a mood column
df['moods'] = np.random.choice(moods, size=len(df))

# Generate a free_time column
df['free_time'] = np.random.choice(times, size=len(df))

# Generate an accommodation column
df['accommodation'] = np.random.choice(hotels, size=len(df))

# Save the updated dataset
df.to_csv('./src/data/datasets/augmented_dataset.csv', index=False)
print('\nData has been augmented.\n')
