# picorg
A set of scripts to organize pictures. This is a work in progress and does not fully work at the moment.

## Installation
```python
pip install picorg
```

## Usage
```python
# Renames all images in the current working directory. It tries to use the timestamp of when the image was taken from the EXIF data. All renamed files will be moved to a folder called **OK**, and if the script cannot find a suitable name, the file will be moved to the **NOK** folder.
python -m picorg -r

# Traverses all folders listed in the settings.json file and lists all duplicated filenames and where to find them. Useful when using more than one root folder for your pictures.
python -m picorg -d
```

## Configuration
A settings file is created in <USER_HOME>/.picorg that stores the users settings.

## Developing
Install dependencies from the requirements-dev.txt file
```python
pip install -r requirements-dev.txt
```

Run tests with
```python
pytest
```
or using tox
```
tox
```