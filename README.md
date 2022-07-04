# PySpark SparkML anime recommender.

NET ROLL! (Or something like that). An anime series recommender mockup using SparkML ALS.
Contains some Cross Validation parameter testing to select best parameters for model. If you are interested in this, I recommended testing on a proper platform to prevent running into hardware limitations. 
We are using Jikan API v3 https://jikan.moe/ as our data source.
Find the reduced dataset in data. To download complete dataset refer to source.

## Usage
### Jikan
A working URL for Jikan's v3 API is needed to run the cataloguer.
You must set this url in app.py line 39:
```py
    req_jikan = JikanRequest('<URL>/v3')
```
I recommend setting up your own from: https://github.com/jikan-me/jikan-docker .

### Running the code
Clone repo.
```bash
    git clone https://github.com/RoachLok/anime-series-recommender
```

Setup python env.
```bash
    python3 -m venv .venv
```

Enable the environment running the activate script for your shell and environment.
```bash
    # Bash (Windows)
    source .venv/Scripts/activate

    # PowerShell
    .\.venv\Scripts\Activate.ps1
``` 

Install dependencies from requirements.txt.
```bash
    pip install -r requirements.txt
```

Start the app.
```bash
    python app.py
```

### Run it with docker-compose
You can run this too on docker and there is no more additional setup.
(No HDFS docker setup, SparkSession running on local).

```bash
    docker-compose up
```


## Sources

For datasets and series queries:

JIKAN:
https://jikan.moe/ 

Download .csv's from here:
    - Small : http://www.exemplarius.com/rating_complete_small.csv
    - Full  : http://www.exemplarius.com/rating_complete.csv