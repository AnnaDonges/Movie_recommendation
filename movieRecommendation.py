import pandas as pd
import numpy as np
from IPython.display import display
from ast import literal_eval

# Set the path for the output CSV file
output_path = "C:/Users/ad29203/Desktop/GHP/Movie_recommendation/output.csv"

# Import CSV files
path = "C:/Users/ad29203/Desktop/GHP/Movie_recommendation"
budgetGenres = pd.read_csv(path + "/budgetGenres.csv")
castCreditCrew = pd.read_csv(path + "/castCrewTitle.csv")

#budgetGenres.head()
#castCreditCrew.head()

# Merge columns
castCreditCrew.columns = ['id', 'title', 'cast', 'crew']
budgetGenres = budgetGenres.merge(castCreditCrew, on ='id')

# Display the merged dataframe as a table
#budgetGenres.head()

# Save the merged dataframe to a CSV file
#budgetGenres.to_csv(output_path, index=False)

#loop through key features needed for identifying similar movies
features = ['cast', 'crew', 'keywords', 'genres']

for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(literal_eval)

#display(budgetGenres[features].head(10)) 

def getDirector(x):
    #extract the name of the director form the crew list
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan



def getList(x):
    #get the first 3 names/objects from list
    #ex. first three cast members, first 3 genres, first 3 keywords
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    
    return []

#apply get director to dataset
budgetGenres["director"] = budgetGenres["crew"].apply(getDirector)

#features that the get list function will apply to
features = ["cast", "keywords", "genres"]

#apply get list function
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(getList)

print(budgetGenres[['title_x', 'cast', 'director', 'keywords', 'genres']].head())


def cleanData(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""
        

features = ['cast', 'keywords', 'director', 'genes']
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(cleanData)

def soup(features):
    pass