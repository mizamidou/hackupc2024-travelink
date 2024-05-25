import pandas as pd
from utils.interest_sentiment import main as get_interest_sentiment
from utils.psychology_sentiment import main as get_psychology_sentiment

def get_simultaneous_travellers(df, new_traveller):
    """
    Identify travellers who will be in the same city during 
    the overlapping date range of a new traveller.

    Arguments
    ---------
    df (DataFrame):        The dataframe containing existing traveller data.
    new_traveller (dict):  A DataFrame row with travel info of the new traveller.
    
    Returns
    -------
    simultaneous_travellers (DataFrame):  A subset of df with entries of 
                                          people who will be in the same city 
                                          during the overlapping timeframe.

    """
    # Convert the dates in the dataframe to datetime format if not already done
    df['Arrival Date'] = pd.to_datetime(df['Arrival Date'], 
                                          format='%d/%m/%Y')
    df['Return Date'] = pd.to_datetime(df['Return Date'], 
                                       format='%d/%m/%Y')
    
    # Extract data from the new traveller row
    arrival_city = new_traveller['Arrival City']
    arrival_date = pd.to_datetime(new_traveller['Arrival Date'], 
                                    format='%d/%m/%Y')
    return_date = pd.to_datetime(new_traveller['Return Date'], 
                                 format='%d/%m/%Y')
    
    # Filter for travellers who are going to the same city
    same_city_travellers = df[df['Arrival City'] == arrival_city]

    # Filter for date overlaps
    simultaneous_travellers = same_city_travellers[
        (same_city_travellers['Arrival Date'] <= return_date) &
        (same_city_travellers['Return Date'] >= arrival_date)
    ]
    
    return simultaneous_travellers

def get_basic_similar_travellers(df, new_traveller):
    """"
    Identify travellers who share similar interests in free time and networking.
    If networking is false, it will also require matching the company name.

    Arguments
    ---------
    df (DataFrame):        The dataframe containing existing traveller data.
    new_traveller (dict):  A dictionary with new traveller's free time, 
                           networking, and possibly company information.

    Returns
    -------
    similar_travellers (DataFrame):   A subset of df with entries of people 
                                      who are similar based on the criteria.
    
    """

    # Filter for travellers who have the same free time preference
    similar_travellers = df[df['free_time'] == new_traveller['free_time']]

    # Further filter for matching mood preference
    similar_travellers = similar_travellers[
        similar_travellers['mood'] == new_traveller['mood']
    ]
    
    # Further filter for matching networking preference
    similar_travellers = similar_travellers[
        similar_travellers['networking'] == new_traveller['networking']
    ]
    
    # If networking is True, filter to only match new people,
    # i.e., people outside the company
    if new_traveller['networking']:
        similar_travellers = similar_travellers[
            similar_travellers['company'] != new_traveller['company']
        ]
    # If networking is False, only match people from the company
    else:
        similar_travellers = similar_travellers[
            similar_travellers['company'] == new_traveller['company']
        ]
    
    return similar_travellers

def get_premium_interest_matching_travellers(all_travellers, 
                                             new_traveller):
    # Get interest groups
    new_simultaneous_travellers = pd.concat([all_travellers, 
                                             new_traveller], ignore_index=True)
    grouped_travellers = get_interest_sentiment(new_simultaneous_travellers)

    # Get interest match names
    interest_match_names = None
    for cluster, names in grouped_travellers:
        if 'Me' in names.tolist():
            interest_match_names = set(names.tolist())

    matching_travellers = new_simultaneous_travellers[
        new_simultaneous_travellers['Traveller Name'].isin(interest_match_names)
    ]

    matching_travellers = matching_travellers[matching_travellers['Traveller Name'] != 'Me']
    matching_travellers = matching_travellers.iloc[:, :-3]

    return matching_travellers

def get_premium_psychology_matching_travellers(all_travellers,
                                               new_traveller):
    # Get interest groups
    new_simultaneous_travellers = pd.concat([all_travellers, 
                                             new_traveller], ignore_index=True)
    grouped_travellers = get_psychology_sentiment(new_simultaneous_travellers)

    # Get interest match names
    psychology_match_names = []
    interest_match_names = None
    for cluster, names in grouped_travellers:
        if (names['Traveller Name'] == 'Me').any():
            psychology_match_names.extend(names['Traveller Name'].tolist())

    matching_travellers = new_simultaneous_travellers[
        new_simultaneous_travellers['Traveller Name'].isin(psychology_match_names)
    ]
    
    matching_travellers = matching_travellers[matching_travellers['Traveller Name'] != 'Me']

    return matching_travellers