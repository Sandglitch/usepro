import pandas as pd

# --- SETUP ---
# Load the city data from the CSV file
print("Loading worldcities.csv...")
try:
    df = pd.read_csv('worldcities.csv')
except FileNotFoundError:
    print("Error: worldcities.csv not found. Make sure it's in the same folder as this script.")
    exit()

# --- DEFINE THE RULES ---

# Define major island nations by their 'iso2' country code.
# You can add more codes to this list if you find other major islands.
ISLAND_COUNTRIES = {
    'GB',  # Great Britain
    'IE',  # Ireland
    'JP',  # Japan
    'ID',  # Indonesia
    'PH',  # Philippines
    'MG',  # Madagascar
    'NZ',  # New Zealand
    'LK',  # Sri Lanka
    'TW',  # Taiwan
    'CU',  # Cuba
    'IS',  # Iceland
}

# --- THE LOGIC ---

def assign_landmass_group(row):
    """
    This function takes a row of the dataframe and returns its landmass group.
    """
    # 1. Check if the city is in a known major island country first.
    if row['iso2'] in ISLAND_COUNTRIES:
        # Group by the country name, e.g., "Japan"
        return row['country']
    
    # 2. Check for single-continent landmasses.
    elif row['continent'] == 'North America':
        return 'North America'
    elif row['continent'] == 'South America':
        return 'South America'
    elif row['continent'] == 'Australia':
        return 'Australia'
    
    # 3. If it's not an island and not in the Americas/Australia,
    #    it must be on the main Afro-Eurasian landmass.
    elif row['continent'] in ['Asia', 'Europe', 'Africa']:
        return 'Afro-Eurasia'
    
    # 4. Fallback for any other cases (like Antarctica)
    else:
        return 'Other'

# --- APPLY THE LOGIC & SAVE ---

print("Assigning landmass groups...")
# Create a new 'landmass_group' column by applying our function to every row
df['landmass_group'] = df.apply(assign_landmass_group, axis=1)

# Save the new, enhanced dataframe to a new CSV file
output_filename = 'cities_with_groups.csv'
df.to_csv(output_filename, index=False)

print(f"\nSuccess! New file saved as '{output_filename}'")
print("This new file now contains a 'landmass_group' column for you to use in your app.")

# Optional: Display a count of cities in each new group
print("\nCity count per group:")
print(df['landmass_group'].value_counts())