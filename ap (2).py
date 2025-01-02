import streamlit as st
import pandas as pd

# Load the data
books = pd.read_csv("C:\\Users\\Vikra\\Downloads\\dataset\\Books.csv", encoding='ISO-8859-1')
ratings = pd.read_csv("C:\\Users\\Vikra\\Downloads\\dataset (2)\\Ratings.csv", encoding='ISO-8859-1')
users = pd.read_csv("C:\\Users\\Vikra\\Downloads\\dataset (2)\\Users.csv", encoding='ISO-8859-1')

# Merge datasets
ratings_with_name = ratings.merge(books, on='ISBN')

# Prepare the data for recommendations
num_rating = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

avg_rating = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

# Combine data for popularity-based recommendations
popular_df = num_rating.merge(avg_rating, on='Book-Title')

# Streamlit app layout
st.title("Book Recommendation System")
st.header("Popular Books")

# Display popular books
st.write("Here are some of the most popular books based on ratings:")
st.dataframe(popular_df.sort_values(by=['avg_rating', 'num_ratings'], ascending=False).head(10))

# User input for custom recommendations
user_input = st.text_input("Enter a book title to find similar books:")

if user_input:
    # Find books that match the user input
    similar_books = popular_df[popular_df['Book-Title'].str.contains(user_input, case=False)]
    if not similar_books.empty:
        st.write("Similar books found:")
        st.dataframe(similar_books)
    else:
        st.write("No similar books found.")