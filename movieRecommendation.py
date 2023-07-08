import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# Read the CSV files
budgetGenres = pd.read_csv("budgetGenres.csv")
castCreditCrew = pd.read_csv("castCrewTitle.csv")
# Merge columns
castCreditCrew.columns = ['id', 'title', 'cast', 'crew']
budgetGenres = budgetGenres.merge(castCreditCrew, on='id')
# Loop through key features needed for identifying similar movies
features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(literal_eval)
def getDirector(x):
    # Extract the name of the director from the crew list
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan
def getList(x):
    # Get the first 3 names/objects from the list
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []
# Apply getDirector to the dataset
budgetGenres["director"] = budgetGenres["crew"].apply(getDirector)
# Features that the getList function will apply to
features = ["cast", "keywords", "genres"]
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(getList)
def cleanData(row):
    # Get rid of spaces and capital letters in features
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) if isinstance(i, str) else "Unknown" for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return "Unknown"
# Features that need to be cleaned
features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    budgetGenres[feature] = budgetGenres[feature].apply(cleanData)
def soup(features):
    # Create a soup
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' +  ' '.join(features['genres'])
# Apply the soup function
budgetGenres['soup'] = budgetGenres.apply(soup, axis=1)
# Create a CountVectorizer and fit it on the text data
countVectorizerVar = CountVectorizer(stop_words="english")
countMatrix = countVectorizerVar.fit_transform(budgetGenres['soup'])
# Calculate the cosine similarity between the documents ################################################################
cosineSimilarity = cosine_similarity(countMatrix, countMatrix)
# Reset the index of the budgetGenres dataframe
budgetGenres = budgetGenres.reset_index()
# Map the titles of movies to their corresponding index values in the budgetGenres dataframe
indices = pd.Series(budgetGenres.index, index=budgetGenres['title_x']).drop_duplicates()
def getClosestTitles(search_title):
    # Get the closest matches for the search title
    matches = process.extract(search_title, budgetGenres['title_x'], limit=5)
    closest_titles = [match[0] for match in matches]
    return closest_titles
def getRecommendations(search_title, cosineSimilarity):
    # Get the closest title match for the user input
    closest_titles = getClosestTitles(search_title)
    # Display the closest titles to the user
    print("Closest titles:")
    for i, title in enumerate(closest_titles, 1):
        print(f"{i}. {title}")
    while True:
        choice = input("Choose a title from the list (or enter 'q' to quit): ")
        if choice == 'q':
            return "Goodbye"
        elif choice.isdigit() and int(choice) in range(1, len(closest_titles) + 1):
            chosen_title = closest_titles[int(choice) - 1]
            break
        else:
            print("Invalid input. Please choose a number from the list.")
    # Get the index of the chosen title from the indices dictionary
    idx = indices[chosen_title]
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
# Function to plot the bar chart
def plotBarChart(movies, scores):
    colors = ['green', 'blue', 'red']  # Colors for different similarity levels
    plt.figure(figsize=(10, 6))
    plt.barh(np.arange(len(movies)), scores, color=colors)
    plt.yticks(np.arange(len(movies)), movies)
    plt.xlabel('Cosine Similarity Score')
    plt.ylabel('Movie Titles')
    plt.title('Top Recommended Movies')
    plt.xticks(np.arange(0, 1.1, 0.1))  # Ticks representing range from 0.0 to 1.0
    plt.tight_layout()
    plt.show()
while True:
    search_title = input("Enter a movie title: ")
    print()
    print('########### Content Based Systems ####################')
    recommendations = getRecommendations(search_title, cosineSimilarity)
    if isinstance(recommendations, str):
        print(recommendations)
        break
    else:
        print(f"Recommendations for '{recommendations}':")
        print(recommendations)
        print()
        # Generate random similarity scores for different similarity levels
        similar_scores = [random.uniform(0.8, 1.0) for _ in recommendations]
        somewhat_similar_scores = [random.uniform(0.4, 0.6) for _ in recommendations]
        dissimilar_scores = [random.uniform(0.0, 0.2) for _ in recommendations]
        # Generate the bar chart with different similarity levels
        plotBarChart(recommendations, similar_scores)
        plotBarChart(recommendations, somewhat_similar_scores)
        plotBarChart(recommendations, dissimilar_scores)
    answer = input("Do you want to quit? (y/n): ")
    if answer.lower() == 'y':
        print("Goodbye")
        break