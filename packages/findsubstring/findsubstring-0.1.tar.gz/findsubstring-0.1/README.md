# findsubstring
*Python3 module to find a substring on a string.*

Based on Karl Knechtel's answer on Stack Overflow:
https://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python

## Installation
### Install with pip
```
pip3 install -U findsubstring
```

## Usage
```
In [1]: import findsubstring

In [2]: list(
    findsubstring.find_all(
        str_="spam spam spam spam",
        substring="spam"
        )
    )

Out[2]: [0, 5, 10, 15]
```
