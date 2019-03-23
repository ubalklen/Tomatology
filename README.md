# Tomatology

Using logistic regression to predict if a movie will be classified as Rotten or Fresh by Rotten Tomatoes.

## Introduction

[Rotten Tomatoes](https://www.rottentomatoes.com/) is a movie review aggregator website. It labels each movie that receives at least 60% of positive reviews made by professionals as a "Fresh Tomato". Otherwise, the movie is considered a "Rotten Tomato".

Tomatology is a logistic regression to classify a movie as Fresh or Rotten before any reviews have been given.

## Data

All movie data was scraped straight from Rotten Tomatoes website using the scripts in [scraper](scraper) folder.

The data used to train the logistic regession model is in the [movie_data.json](movie_data.json) file and is comprised of 9104 movies.

The file [movie_data_competition.json](movie_data_competition.json) contains 55 movies and is being used for the model's final test (see [Competition](Competition.md) page).

## Feature Enginnering

I've choosen to use information about rating, genre, studio, runtime, directors and cast to build the model's features. I turned rating, genre and studio into binary features, one for each avaliable option. Because applying the same procedure to directors and actors would generate many features, I selected the most known directors and actors and built features to check for the presence of each one of them in a movie.

## Model

Logistic regression is a simple yet powerful method of data classification. It draws an optimal hyperplane that best separates previously categorized data and allows one to predict which category unseen data should be labeled.

The [prepare_and_train.py](prepare_and_train.py) file reads all training data, prepares the inputs and trains a logisitc regression model.

The parameters of the final model can be seem in the [Parameters](Parameters.md) page.

## Results

I was able to get the following results:

```
ubalklen@Ubuntu:~/Tomatology$ python3 prepare_and_train.py
Logistic regression with training dataset
Accuracy: 0.7135795688589867

Logistic regression with validation dataset
Accuracy: 0.6930258099945085

Naive model (always predicts 1) with training dataset
Accuracy: 0.5521076479472745

Naive model with validation dataset
Accuracy: 0.5590334980779791
```

As a final test, I am running a small competition against real people on movies to be launched in 2019. More details on [Competition](Competition.md) page.
