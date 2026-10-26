
import requests
url="https://api.github.com/search/repositories?q=python&per_page=100"
response=requests.get(url)
data=response.json()
print(type(data))           
'''data (dict)
│
├── total_count
├── incomplete_results
└── items (list)
      │
      ├── [0] → repository 1 (dict)
      ├── [1] → repository 2 (dict)
      ├── [2] → repository 3 (dict)
      └── ...'''
print(data.keys())
items=data["items"]
print(type(items))
print(len(items))

first_repo=items[0]
print(type(first_repo))
print(first_repo.keys())

print(first_repo["name"])
print(first_repo["language"])
print(first_repo["stargazers_count"])
repository=[]
for repo in items:
      print(repo["name"],repo["language"],repo["stargazers_count"])
      small_dictionary={"name":repo["name"],
                        "language":repo["language"],
                        "stargazers_count":repo["stargazers_count"],
                        "full_name":repo["full_name"],
                        "forks_count":repo["forks_count"],
                        "open_issues_count":repo["open_issues_count"],
                        "watchers_count":repo["watchers_count"],
                        "created_at":repo["created_at"]
                        }
      repository.append(small_dictionary)

print(len(repository))
print(repository[:3])
      
import pandas as pd 
df=pd.DataFrame(repository)
print(df.shape)
print(df.head())
df.info()
df["language"] #Check missing values  df["language"].isna()
print(df["language"].isna().sum()) # Count missing values
print(df[df["language"].isna()]) #Show rows with missing values
print(df["name"].duplicated().sum()) # Count duplicated values
print(df[df["full_name"].duplicated(keep=False)].sort_values("full_name")) 
print(df["stargazers_count"].describe()) # Summary statistics 
 # Show the row with the maximum stargazers_count
print(df["stargazers_count"].max())
print(df[df["stargazers_count"]==df["stargazers_count"].max()])
print(df["stargazers_count"].sort_values(ascending=False).head(10)) # Show the top 10 repositories with the most stars
print(df.sort_values("stargazers_count",ascending=False).head(10)) # Show the top 10 repositories with the most stars
df['created_at'] = pd.to_datetime(df['created_at'])
print(df["created_at"].dtype)
from datetime import datetime,timezone
current_time = datetime.now(timezone.utc)
print(current_time)
df['repository_age']=(current_time-df["created_at"]).dt.days
print(df[["full_name", "created_at", "repository_age"]])
df["repository_age_years"] = df["repository_age"] / 365.25
print(df[["full_name", "created_at", "repository_age","repository_age_years"]])

print(df["repository_age_years"].max()) #Find the oldest repository
print(df[df["repository_age_years"]==df["repository_age_years"].max()]) # Oldest repository: geekcomputers/Python

print(df["stargazers_count"].max()) # find the repository with the most stars
print(df[df["stargazers_count"]==df["stargazers_count"].max()]) # Most-starred repository: vinta/awesome-python

print(df["forks_count"].max()) # find the repository with the most forks
print(df[df["forks_count"]==df["forks_count"].max()]) # Most-forked repository: Complete-Python-3-Bootcamp

print(df[df["full_name"]=="vinta/awesome-python"][["full_name","stargazers_count","forks_count"]]) # Show the number of stars and forks for the repository vinta/awesome-python

# Calculate the correlation between stargazers_count and forks_count
print(df[["stargazers_count","forks_count"]].corr())

#calculate the correlation between repository_age_years and stargazers_count
print(df[["repository_age_years","stargazers_count"]].corr())

# which programming language appear most frquently in dataset
print(df["language"].value_counts())
#find the missing values
print(df[df["language"].isna()])
# fill with "Unknown"
print(df["language"].fillna("Unknown"))
#Assign it back to the language column of df.
df["language"]=df["language"].fillna("Unknown")

#check any remaing missing values
print(df["language"].isna().sum())

print(df["language"].value_counts())

#check duplicated values in the full_name column
print(df["full_name"].duplicated().sum())
df.info()

#Check for suspicious values
print(df["stargazers_count"].min())
print(df["forks_count"].min())
print(df["open_issues_count"].min())

print(df["stargazers_count"].max())
print(df["forks_count"].max())
print(df["open_issues_count"].max())

#Understand outliers
print(df["stargazers_count"].describe())

# identify outliers using Inter Quartile Range(IQR) method
#IQR = Q3 - Q1   ans : IQR = 20063.25 and upper limit = 50840.875

#Identify potential outliers
print(df["stargazers_count"]>50840.875) # Show the rows with stargazers_count greater than 50840.875
print(df[df["stargazers_count"]>50840.875]) # Show the rows with stargazers_count greater than 50840.875

print(df.sort_values("stargazers_count",ascending=False).head(5))

# create a new column called average_stars_per_year using your existing columns: stargazers_count repository_age_years
df["average_star_by_year"]=df["stargazers_count"]/df["repository_age_years"]
print(df["average_star_by_year"].sort_values(ascending=False).head(5)) # Show the top 5 repositories with the most stars per year
print(df.sort_values("average_star_by_year",ascending=False).head(5)) # Show the top 5 repositories with the most stars per year

print(df.sort_values("forks_count",ascending=False).head(5)) # Show the top 5 repositories with the most forks

 # Show the top 5 repositories with the most forks
print(df.sort_values("forks_count",ascending=False).head(5)[["full_name","forks_count","stargazers_count"]]) # Show the top 5 repositories with the most forks

#Create a new DataFrame column named fork_to_star_ratio by dividing forks_count by stargazers_count
df["fork_to_star_ratio"]=df["forks_count"]/df["stargazers_count"]
print(df.sort_values("fork_to_star_ratio",ascending=False).head(5)[["full_name","stargazers_count","forks_count","fork_to_star_ratio"]]) # show the top 5 repositories with the highest fork to star ratio

print(df.sort_values("stargazers_count",ascending=False).head(5)[["full_name","stargazers_count","forks_count"]]) # show the top 5 repositories with the most stars and their corresponding forks count
# correlation between repository_age_years and stargazers_count
print(df[["repository_age_years","stargazers_count"]].corr())
# repositories with more stars also tend to have more open issues
print(df[["stargazers_count","open_issues_count"]].corr())

print(df["language"].value_counts())# Check the most common programming languages in the dataset

print(df.isnull().sum())# Check for missing values in the dataset
print(df["full_name"].duplicated().sum())
print(df.describe())

print(df.groupby("language")["stargazers_count"].mean()) # Calculate the average number of stars for each programming language
print(df.groupby("language")["stargazers_count"].median()) # Calculate the median number of stars for each programming language
print(df.groupby("language")["stargazers_count"].max())
print(df.groupby("language")["stargazers_count"].agg(["count","mean","median","max"])) # Calculate the count, mean, median, and max number of stars for each programming language

print(df["language"].value_counts())
print(df.isnull().sum())
print(df.isnull().sum().sum())
print(df["full_name"].duplicated().sum())
df.info()

import matplotlib.pyplot as plt
value=df["language"].value_counts()
plot=value.plot(kind="bar")
plt.title("Number of repositories by language")
plt.xlabel("Programming Language")
plt.ylabel("Number of Repositories")
plt.show()

import os

file_path = "/Users/sharadhakattalingannagari/Desktop/Src/github_repository_analysis.csv"

df.to_csv(file_path, index=False)

print("CSV saved successfully!")
print("File location:", file_path)
print("File exists:", os.path.exists(file_path))