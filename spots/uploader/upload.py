"""Grabs information about each map location and uploads it to GCS"""

import json
import pandas as pd

from place import Place

DEBUG = True

PLACES_INPUT_FILENAME = 'matt & caroline _).csv'
DEBUG_PLACES = 3

def get_place_objects(df):
    """Convert df to place objects"""
    # Limit rows to reduce cost on debug runs
    if DEBUG:
        print(f'INFO: Debug mode enabled, limiting to {DEBUG_PLACES} place(s)')
        df = df.head(DEBUG_PLACES)

    # Will read as ints with NaNs
    df = df.fillna('')
    df = df.astype(str)

    places = []
    invalid_places = 0
    for _, row in df.iterrows():
        # Clean out empty rows
        if not row['Title'] or not row['URL']: 
            invalid_places += 1
            continue

        places.append(Place(
                title=row['Title'],
                notes=row['Note'],
                tags=row['Tags'],
                url=row['URL'],
                comment=row['Comment']
            ))

    if invalid_places >= 0:
        print(f'WARN: Filtered out {invalid_places} invalid place(s) with empty title or URL')
    print(f'INFO: Read {len(places)} valid places')

    return places

def main():
    try:
        df = pd.read_csv(PLACES_INPUT_FILENAME, skiprows=2)
        places = get_place_objects(df)
    except FileNotFoundError:
        print(f'{PLACES_INPUT_FILENAME} not found')

    print(places)
    
if __name__ == '__main__':
    main()