# Vacation_Planner




### Overview
This project is intended to help people plan a vacation by returning the best businesses and towns that a state offers. This code works by web scraping TripAdvisor for the best tourism towns in a state, and then querying Yelp's API to find the best businesses in each of the towns. After it is done running the code, the script will then save every town's businesses in their own csv inside of a new directory called "vacation-(state)".

### Requirements
Before running this code you need to create a new file in the directory called config_secret.json and put your Yelp API keys in there in the following format:

```
{
    "consumer_key": "YOUR_CONSUMER_KEY",
    "consumer_secret": "YOUR_CONSUMER_SECRET",
    "token": "YOUR_TOKEN",
    "token_secret": "YOUR_TOKEN_SECRET"
}
```

### Running the Code

To run this code just run the following command while in the same directory as Plan_Vacation.py

	python Plan_Vacation.py <state> <num_business> -terms <terms> -categories <categories> -output <True|False>
    
  * __state__ is a state name as a string Ex. "New York"
  * __num_business__ is the number of businesses you want returned for each term as an integer Ex. 5
  * __terms__ is an optional list of terms you're interested in seperated by spaces Ex. Food Hotel Active (Also the default)
  * __output__ is an optional boolean, if given True then a folder is created and towns are saved there (Default is False)
    
An example of this code being run looks like this:

    python Plan_Vacation.py "New Hampshire" 5 -terms food hotel active -output True
