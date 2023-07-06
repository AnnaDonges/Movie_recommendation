import pandas as pd

path = "C:/Users/ad29203/Desktop/GHP/Movie_recommendation"
budgetGenres = pd.read_csv(path + "/budgetGenres.csv")
castCreditCrew = pd.read_csv(path + "/castCrewTitle.csv")

budgetGenres.head()
castCreditCrew.head()
