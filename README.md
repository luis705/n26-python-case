# Marvel API characters extraction

## Usage instructions
- Generate API keys on [marvel's website](https://developer.marvel.com/)
- Put the keys on the correct variables on `keys.py`
- Run `main.py` to get a sample of the data
- The file `Case python - result.csv` contains the desired output of this case.

## Development strategy
- Make a single API call ✓
- Understand the data format by fetching only one row ✓
- Write a script that get the needed info from the first row ✓
- Write a script that requests all the dataset ✓

## API result understanding
The return of the request is a JSON file, the desired data is inside the "results" field. The value of this field is a
list of other key-value mapped objects.

Each of those key-value objects represent a different character with all the requested fields. The `id`, `name`,
`description` data are contained directly as values mapped but keys with the same names. But the `comics`, `series`,
`stories` and `events` values are contained inside another object as the available key. 

So, using the python dictionary syntax to get the data from a json file, and considering the hero variable the object of
a random hero, we can access all the needed properties as shown below.

```python
hero_id = hero['id']
hero_name = hero['name']
hero_description = hero['description']
number_of_comics = hero['comics']['available']
number_of_series = hero['series']['available']
number_of_stories = hero['stories']['available']
number_of_events = hero['events']['available']
```

## Code explanation

### Auxiliary functions

#### `generate_ts`
This function just generates a random string to be used as timestamp value on the API authorization. This parameter
could be the same string everytime, the API is called, but for security purposes I chose to generate a new random value
everytime the script is run.

#### `md5_checksum`
This function calculates the md5 hash of the string in the format described by the API documentation. For this, it
receives both public and private keys and the timestamp string, merge them in the desired way and apply the  hash
function.

#### `get_character_data`
This function extract the desired data from a character dictionary received on the API call.

### Main function
The main function is based on a iteration loop that makes the API calls. Those calls must be made inside the loop
because of the maximum response size of 100 characters. This way on each iteration the loop checks if the amount of
characters already received is equal to the total number of characters and, if so, the loop stops.

Other than that, the loop populates a list with the desired data from all characters. In the end of the loop this list
is used to create a pandas dataframe which will be saved to memory on the file `Case python - result.csv`.

