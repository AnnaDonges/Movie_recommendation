import pandas as pd
import numpy as np
from IPython.display import display
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

while True:
    # Set the path for the output CSV file
    output_path = "C:/Users/ad29203/Desktop/GHP/Movie_recommendation/output.csv"

    # Import CSV files
    #path = "C:/Users/ad29203/Desktop/GHP/Movie_recommendation"
    budgetGenres = pd.read_csv("budgetGenres.csv")
    castCreditCrew = pd.read_csv("castCrewTitle.csv")

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

    #print(countMatrix.shape)

    #calculates the cosine similarity between the documents represented by the countMatrix. It takes the countMatrix as input twice since it 
    # compares each document with every other document.
    cosineSimilarity = cosine_similarity(countMatrix, countMatrix)

    #print(cosineSimilarity.shape)

    #Reseting the index of budgetGenres dataframe. The current index is replaced with a default numeric index
    budgetGenres = budgetGenres.reset_index()

    #Mapping the titles of movies to their corresponding index values in the budgetGenres dataframe. Drop_duplicates ensures that the movie title has a unique index value.
    indices = pd.Series(budgetGenres.index, index=budgetGenres['title_x']).drop_duplicates()

    #print(indices.head())

    def getRecommendations(title, cosineSimilarity):
        # Check if the given movie title is in the indices dictionary
        if title not in indices:
            return "Sorry, the movie is not in the data list."

        # Get the index of the movie title from the indices dictionary
        idx = indices[title]
        
        # Create a list of tuples with movie indices and their corresponding cosine similarity scores
        similarScores = list(enumerate(cosineSimilarity[idx]))
        
        # Sort the similarScores list based on the cosine similarity scores in descending order
        similarScores = sorted(similarScores, key=lambda x: x[1], reverse=True)
        
        # Get the top 10 similar movie scores (excluding the original movie itself)
        similarScores = similarScores[1:11]

        # Extract the movie indices from the similarScores list
        movieIndices = [ind[0] for ind in similarScores]
        
        # Get the movie titles from the budgetGenres dataframe using the movie indices
        movies = budgetGenres["title_x"].iloc[movieIndices]
        
        # Return the list of recommended movies
        return movies

    search_title = input("Enter a movie title: ")
    print()
    print('########### Content Based Systems ####################')
    recommendations = getRecommendations(search_title, cosineSimilarity)
    print(f"Recommendations for {search_title}:")
    print(recommendations)

    while True:
        answer = str(input('Run again? (y/n): '))
        if answer in ('y', 'n'):
            break
        print("invalid input.")
    if answer == 'y':
        continue
    else:
        print("Goodbye")
        break
    

    #whether a recommendation causes someone else will watch the movie