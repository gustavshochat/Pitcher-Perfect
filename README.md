# Pitcher Perfect

*Building the optimal beer recommender using BeerAdvocate reviews from 1998-2011.*

![](images/Beer-Cheers-300x300.png)

## Introduction

Here I will showcase my progress towards designing a high-performance recommendation engine capable of translating user preference inputs into 
meaningful recommendations.

Originally scraped from BeerAdvocate.com, this dataset was constructed and made available by Julian McAuley of UC San Diego's Computer Science Department and in
its raw form contains roughly 1.5 million reviews **(samples/dataset_sample.csv)**. 

## Preprocessing & EDA

This dataset is quite sparse with regard to item-user pairings, comprising reviews by 33,874 users of 66,051 unique beers. 
To acheieve more substantial density I honed in on the top 1000 most-reviewed beers, cutting the total number of reviews in half to about
750,000. 

Of these beers the number of ratings range from 342 - 3290 ratings, with an average of 753.383 ratings per beer. Most of the original user
base was preserved with 27,062 users remaining, each having rated anywhere from 2 to 1034 beers with 28.84 being the average. 

The average rating across all 1000 beers is 3.91 on a 1-5 scale. The highest rated beer across all users is Heady Topper (New England style IPA) with a cumulative
rating of 4.63, the lowest Wild Blue (blueberry lager) at 1.92.

Each review is complete with 12 features including beer name, user name, beer style, taste rating, aroma rating, and overall rating. 
With overall rating values I populated a 1000 (beers) by 27,062 (users) utility matrix with every existing user-item rating **(samples/util_matrix_sample.csv)**. 

I normalized each user's ratings by subtracting their average assigned rating from all reviews given, supplementing missing ratings with values of 0. 
This effectively substitues all empty user-item pairs with the average rating given by that user, as each user's average rating is now equal to 0 with
below average ratings being negative values and above average ratings positive values. 

With every beer now existing in the same vector space, I computed the cosine similarity between every possible pair of beers and compiled the results
into a 1000 by 1000 similarity matrix **(samples/cosim_matrix_sample.csv)**.


## Model Structure and Evaluation 

The overarching concept of each model is for a user to input 5 favored beers of choice and recieve 10 recommendations in return. 

To assess the performance of each model I evaluated recommendations made to the top 10 pre-existing users with the most reviews given (substituting
their 5 highest rated beers as inputs). My metric of choice in doing so was the user's average true rating percentile across the 10 beers recommended 
to them (i.e. a performance score of 70 would imply that, on average, the beers recommended to a user fell within the 70th percentile of their ratings hierarchy). 


## Content-Based Approach (src/content_based.py)

#### Performance Score - 79

In this simple system, for each of the 5 input beers the 2 with the highest cosine similarity scores are recommended (with the exception of would-be repeats). 

In the below example I have input 5 generic American Lagers with an average overall rating of 2.94. In return I received 10 similarly common
beers with significant brand overlap to the input set, averaging a 2.67 rating on the 1-5 scale.

<ins>Example input/output:</ins>

- Input: 
  - Bud Light
  - Miller High Life
  - Coors Light
  - Pabst Blue Ribbon
  - Miller Lite

- Output: 
  - Miller Genuine Draft
  - Rolling Rock Extra Pale
  - Michelob Ultra
  - Budweiser
  - Corona Extra
  - Coors 
  - Corona Light
  - Budweiser Select
  - Heineken Lager Beer
  - Amstel Light
 
 
When tested on existing users the content-based recommender achieved a performance score of 79, meaning that its recommendations averaged in the 79th percentile of users' true rating hierarchies. 


## Collaborative Filtering: User-User (src/user_user.py)

#### Performance Score - 87

Using the input beers provided by the user, this algorithm creates a profile for the user and inserts it into the beer to user utility matrix.
For the remaining beers the averaged ratings assigned by the 10 most similar users, weighted by their cosine similarity scores to the input user, 
are assigned as predicted ratings. The 10 beers with the highest predicted ratings are returned as recommendations. 

Inputting the same 5 beers as in the previous example gave dramatically different results, averaging a 4.13 rating
across all reviews. Also defying intuition are the flavor profiles of the recommendation pool, exhibiting an array of intense IPAs and Stouts with
only two of the returned beers being lagers. 
 
 
<ins>Example input/output:</ins>

- Input: 
  - Bud Light
  - Miller High Life
  - Coors Light
  - Pabst Blue Ribbon
  - Miller Lite

- Output: 
  - Session Lager
  - Sculpin India Pale Ale
  - Sierra Nevada Stout
  - Moosehead Lager
  - Paulaner Hefe-Weissbier Naturtrüb
  - Samuel Smith's Imperial Stout
  - Orval Trappist Ale
  - Southern Pecan
  - Pliny The Elder
  - Prima Pils
 

The discrepancy in output can be explained by an implicit bias towards generally high-ranking beers exhibited by
the user-user collaborative filtering system. When inputting lower rated beers as we have done so far, even the most "similar"
users (those that have rated these beers high relative to other users) have a tendency to favor more choice beers. 

It may come as some surprise that when tested on existing users this model significantly outperformed the content-based recommender,
boasting a performance score of **87**. This outcome is likely attributable to the user base on which it is tested; highly active preexisting 
users with extremely refined preferences as showcased by their review counts of nearly 1000 on average. 


## Collaborative Filtering: Item-Item (src/item_item.py)

#### Performance Score - 84

Similar to the User-User approach, this system predicts a user's ratings for every beer in the database and makes recommendations accordingly.
For each beer, ratings are predicted using the average historical rating weighted by the total cosine similarity score across the 5 input beers.

<ins>Example input/output:</ins>

- Input: 
  - Bud Light
  - Miller High Life
  - Coors Light
  - Pabst Blue Ribbon
  - Miller Lite
  
 
 - Output: 
    - Budweiser
    - Rolling Rock Extra Pale
    - Coors
    - Corona Extra
    - Miller Genuine Draft
    - Heineken Lager Beer
    - Labatt Blue
    - Foster's Lager
    - Michelob (Original Lager)
    - Killian's Irish Red


Given the same 5 input beers these recommendations are far more sensible with regard to style and quality when compared to the user-user system. The historical average rating of this selection most closely matches that of the input pool at 2.97. 
Additionally, with a performance score of 84, this model is more equipped to satisfy the extravagent preferences of the test group than
the content-based approach.


 


