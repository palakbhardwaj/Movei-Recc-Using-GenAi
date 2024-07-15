import pandas as pd

# Load the CSV dataset
df = pd.read_csv('1.csv')

# List of keywords to check for partial matches (convert to lowercase)
keywords = ["star wars", "spider", "superman", "iron man", "batman", "finding nemo", "minions", "barbie",
            "how to train your dragons", "venom", "home alone", "ben 10", "tom and jerry", "scooby-doo",
            "winnie", "frankenstein", "teen titans go" , "harry potter" , "avengers","transylvania","jurassic" , "fantastic four" , "despicable me" , "cinderella","madagascar" , "men in black","justice league","stuart little"]

# Create a function to check for partial matches
def contains_partial(keyword, text):
    return any(keyword.lower() in text.lower() for keyword in keywords)

# Update the 'adult' column based on partial matches
df['adult'] = df['original_title'].apply(lambda title: 0 if contains_partial(keywords, title) else 1)

# Save the updated dataset to a new CSV file
df.to_csv('updated_dataset.csv', index=False)
