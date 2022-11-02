# Observer

Proof of Concept for demonstrating a way to use the browser cache as a C2
channel.
Tested with firefox on ubuntu, using the default snap install.

This monitors the directory, looking for new PNG files.
Once one is found, it attempts to extract a message using LSB encoded message,
which it then decrypts and runs as a shell command.

Doesn't use inodenotify as i had issues with using certain directories with it.

## Why?

I figured it'd be cool to demonstrate an approach to making a beacon that
doesn't try to connect out and instead relies on a watering hole approach.

## Setup


Before everything:
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Next, generate configurations:
```
python3 config_generator.py ./path/to/your/browser/cache/directory
```


For the machine running the browser:
```
python3 observer.py
```

And from the controller:
```
python3 create_message path/to/source/png path/to/output/png "whoami"
```

Then, load the output PNG in a browser and `observer.py` should pick it up.
Try appending a cachebusting string like "?blah" when you change a file.
