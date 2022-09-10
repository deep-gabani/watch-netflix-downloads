# Watch Netflix Downloads

- This is a pet project of mine which I made in spare time.
- Netflix downloaded files are not directly watchable in common players. It is a try to convert them & watch.
- Here is an attempt to make a system to convert the Netflix downloaded file formats (.nfv and .nfa) into playable forms.


## Installation

Install `ffmpeg` using this command:
```bash
sudo apt-get install ffmpeg libsm6 libxext6  -y
```

Then install the requirements using this command:
```bash
pip install -r requirements.txt
```

## Usage

pre-process
```
usage: preprocess.py [-h] -f FOLDER -n NAME

Preprocess the netflix directory.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Video folder
  -n NAME, --name NAME  Video name
```

watch
```
usage: watch_netflix_folder.py [-h] -f FOLDER

Preprocess the netflix directory.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Video folder
```
