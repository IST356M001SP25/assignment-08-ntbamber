import pandas as pd
import streamlit as st 


#Returns locations with total fines greater than or equal to the threshhold
def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    agg_df = violations_df.groupby("location", as_index=False)["amount"].sum() #groups by location and takes sum of total amount of fines
    top_locs_df = agg_df[agg_df["amount"] >= threshold] #filters to locations where total amount of fines is greater than threshold
    return top_locs_df

#Add latitude and longitude to top locations to make them mappable
def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs_df = top_locations(violations_df, threshold) #gets top locations using top_locations function
    lat_lon_df = violations_df[["location", "lat", "lon"]].drop_duplicates(subset="location") #Gets unique lat/lon for each location
    merged = pd.merge(top_locs_df, lat_lon_df, on="location", how="left") #merges top locations with lat/lon data
    return merged[["location", "lat", "lon", "amount"]] #returns columns arranged to pass test

#Filter full dataset to only show tickets in top locations
def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs_df = top_locations(violations_df, threshold) #gets top locations using top_locations function
    top_locs_list = top_locs_df["location"].tolist() #converts top locations to list
    filtered = violations_df[violations_df["location"].isin(top_locs_list)] #filter full dataset to only show tickets in top locations
    return filtered #returns filtered dataset

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    violations_df = pd.read_csv("./cache/final_cuse_parking_violations.csv")

    # Run each function
    top_locs = top_locations(violations_df)
    top_locs_mappable = top_locations_mappable(violations_df)
    top_tickets = tickets_in_top_locations(violations_df)

    # Save to CSVs
    top_locs.to_csv("./cache/top_locations.csv", index=False)
    top_locs_mappable.to_csv("./cache/top_locations_mappable.csv", index=False)
    top_tickets.to_csv("./cache/tickets_in_top_locations.csv", index=False)
