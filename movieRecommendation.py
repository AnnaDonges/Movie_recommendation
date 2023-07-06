import pandas as pd
import numpy as np
from IPython.display import display
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

budgetGenres[['title_x', 'cast', 'director', 'keywords', 'genres']].head()


def cleanData(row):
    #get rid of spaces and capital letters in features
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""
        
#features that need to be cleaned
features = ['cast', 'keywords', 'director', 'genres']

#calling the cleanData function
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(cleanData)


def soup(features):
    #creating a soup
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' +  ' '.join(features['genres'])

#applying the soup function
budgetGenres['soup'] = budgetGenres.apply(soup, axis = 1)

#print(budgetGenres['soup'].head())

#creates CountVectorizer class and sets the parameter to stop common English words 'the, is, etc' from being considered as features
countVectorizerVar = CountVectorizer(stop_words="english")

#the fit_transform fits the countVectorizerVar on the text data and transforms it into a matrix of token counts. 
countMatrix = countVectorizerVar.fit_transform(budgetGenres['soup'])

print(countMatrix.shape)

#calculates the cosine similarity between the documents represented by the countMatrix. It takes the countMatrix as input twice since it 
# compares each document with every other document.
cosineSimilarity = cosine_similarity(countMatrix, countMatrix)

print(cosineSimilarity.shape)

#Reseting the index of budgetGenres dataframe. The current index is replaced with a default numeric index
budgetGenres = budgetGenres.reset_index()

#Mapping the titles of movies to their corresponding index values in the budgetGenres dataframe. Drop_duplicates ensures that the movie title has a unique index value.
indices = pd.Series(budgetGenres.index, index=budgetGenres['title_x']).drop_duplicates()

print(indices.head())

def getRecommendations(title, cosineSimilarity):
    idx = indices[title]
    similarScores = list(enumerate(cosineSimilarity[idx]))
    similarScores = sorted(similarScores, key=lambda x: x[1], reverse=True)
    similarScores = simScores[1:11]
    #(a,b) where a is id of movie, b is similarScore
