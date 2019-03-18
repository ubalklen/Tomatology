# Tomatology

Using logistic regression to predict if a movie will be classified as Rotten or Fresh by Rotten Tomatoes.

## Introduction

[Rotten Tomatoes](https://www.rottentomatoes.com/) is a movie review aggregator website. It labels each movie that receives 60% or more positive reviews made by professionals as a "Fresh Tomato". Otherwise, the movie is considered a "Rotten Tomato".

Tomatology is a logistic regression to classify a movie as Fresh or Rotten before any reviews have been given.

## Data

All movie data was scraped straight from Rotten Tomatoes website using the scripts in Scraper folder. The data used to train the logistic regession model is in the xxx.json file and is comprised of 

## Feature Enginnering

I've choosen to use information about rating, genre, studio, duration, directors and cast to build the model's features. I turned rating, genre and studio into binary features, one for each avaliable option. Because applying the same procedure to directors and actors would generate many features, I selected the most known directors and actors and built features to check for the presence of each one of them in a movie.

## Model

Logistic regression is a simple yet powerful method of data classification. It draws an optimal hyperplane that best separates previously categorized data and allows one to predict which category unseen data should be labeled.

The parameters of the final model can be seem in the following table.

## Results

I was able to get the following results:

As a final test, I am running a small competition against real people on movies to be launched in 2019. More details on [Competition](/Competition.md) page.
