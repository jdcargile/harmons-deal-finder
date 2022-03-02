## Installation
1. You need to be using python version 3
2. Pull down the repository
3. Run `poetry install` to install required dependencies
4. Use the command line tool by seeing the examples below.

## Usage
```
python harmons.py search "ice cream"
```

```
python harmons.py search "ice cream" --discount-only
```

```
python harmons.py search "ice cream" --vegan
```

```
python harmons.py search "ice cream" --discount-only --vegan
```

```
python harmons.py search --discount-only --vegan --discount-percentage-highlight 10 "ice cream"
```

## Output
Example of output
![Output Example](./output-example.png "Output Example")
