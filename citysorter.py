import pandas as pd

# --- SETUP ---
# Load the city data from the CSV file
print("Loading worldcities.csv...")
try:
    # Use the correct file provided by the user
    df = pd.read_csv('locations/worldcities.csv') 
except FileNotFoundError:
    print("Error: worldcities.csv not found. Make sure it's in the same folder as this script.")
    exit()

# --- DEFINE THE RULES ---

# Define major island nations by their 'iso2' country code.
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

# Define continents by their 'iso2' country codes
# This is not exhaustive, but covers the vast majority of countries.
AFRO_EURASIA_ISO2 = {
    'AD', 'AE', 'AF', 'AL', 'AM', 'AO', 'AT', 'AZ', 'BA', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BN',
    'BY', 'CD', 'CF', 'CG', 'CH', 'CI', 'CM', 'CN', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DZ', 'EE', 'EG', 'EH',
    'ER', 'ES', 'ET', 'FI', 'FO', 'FR', 'GA', 'GE', 'GG', 'GH', 'GI', 'GM', 'GN', 'GQ', 'GR', 'GW', 'HR',
    'HU', 'IL', 'IM', 'IN', 'IQ', 'IR', 'IT', 'JE', 'JO', 'KE', 'KG', 'KH', 'KM', 'KP', 'KR', 'KW', 'KZ',
    'LA', 'LB', 'LI', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MK', 'ML', 'MM', 'MN',
    'MR', 'MT', 'MW', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NL', 'NO', 'NP', 'OM', 'PK', 'PL', 'PS', 'PT', 'QA',
    'RO', 'RS', 'RU', 'RW', 'SA', 'SD', 'SE', 'SG', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SS', 'ST',
    'SY', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TM', 'TN', 'TR', 'TZ', 'UA', 'UG', 'UZ', 'VA', 'VN', 'YE',
    'ZA', 'ZM', 'ZW'
}

AMERICAS_ISO2 = {
    'AG', 'AI', 'AN', 'AR', 'AW', 'BB', 'BL', 'BM', 'BO', 'BR', 'BS', 'BZ', 'CA', 'CL', 'CO', 'CR', 'DM',
    'DO', 'EC', 'FK', 'GD', 'GF', 'GL', 'GP', 'GT', 'GY', 'HN', 'HT', 'JM', 'KN', 'KY', 'LC', 'MF', 'MQ',
    'MS', 'MX', 'NI', 'PA', 'PE', 'PM', 'PR', 'PY', 'SR', 'SV', 'TC', 'TT', 'US', 'UY', 'VC', 'VE', 'VG',
    'VI'
}

AUSTRALIA_ISO2 = {'AU'}

# --- THE LOGIC ---

def assign_landmass_group(row):
    """
    This function takes a row of the dataframe and returns its landmass group.
    """
    country_iso2 = row['iso2']
    
    # 1. Check if the city is in a known major island country first.
    if country_iso2 in ISLAND_COUNTRIES:
        # Group islands by their specific country name for clarity
        return row['country']
    
    # 2. Check which super-continent the country belongs to.
    elif country_iso2 in AFRO_EURASIA_ISO2:
        return 'Afro-Eurasia'
    elif country_iso2 in AMERICAS_ISO2:
        return 'Americas'
    elif country_iso2 in AUSTRALIA_ISO2:
        return 'Australia'
    
    # 3. Fallback for any other cases (Oceania islands, etc.)
    else:
        return 'Other'

# --- APPLY THE LOGIC & SAVE ---

print("Assigning landmass groups based on country codes...")
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