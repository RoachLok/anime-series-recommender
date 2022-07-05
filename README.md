# PySpark SparkML anime recommender.

NET ROLL! (Or something like that). An anime series recommender mockup using SparkML ALS.<br>
Contains some Cross Validation parameter testing to select best parameters for model. If you are interested in this, I recommended testing on a proper platform to prevent running into hardware limitations.<br>
We are using Jikan API v3 https://jikan.moe/ as our data source.<br>
Find the reduced dataset in data. To download complete dataset refer to source.<br>

## Usage

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

### Run it with Docker using docker-compose
You can also run this on docker without additional setup.<br>
(No Hadoop docker setup, SparkSession running on local).

```bash
    docker-compose up
```

## Notes
### Datasets
<hr>
Refer to sources, download your desired one an drop them in ./data .

### Jikan
<hr>
A working URL for Jikan's v3 API is needed to run the cataloguer.
You must set this url in app.py line 39:

```py
    req_jikan = JikanRequest('<URL>/v3')
```
I recommend setting up your own from: https://github.com/jikan-me/jikan-docker . Or using docker-compose.

### yt-dlp
<hr>
A yt-dlp binary is used to query youtube for videos.

Get your own from here: https://github.com/yt-dlp/yt-dlp .

Depending on where you plan on running the code you may want to change the used binary.

Change it in app.py line 40 for now.
```py
    req_ytube = YTRequest('bin/yt-dlp')
```



## Sources

For datasets and series queries:

JIKAN:
https://jikan.moe/ 

Download .csv's from here: <br>
    - Small : http://www.exemplarius.com/rating_complete_small.csv <br>
    - Full  : http://www.exemplarius.com/rating_complete.csv
