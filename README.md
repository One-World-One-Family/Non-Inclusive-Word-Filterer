# Non-Inclusive Word Filterer 🔍

## Introduction
This is a small python script which scans code bases for non inclusive words and outputs a csv report of their usages to increase diversity and inclusiveness in codebases. 

## Usage

```
python wordfinder.py
```

This will create an `outfile.csv` in your working directory of the discovered words.

#### Optional Directory Argument

Optionally, pass in the directory you would like to search.

For example:

```
python wordfinder.py ~/code
```

## Steps to contribute

Everyone is welcome to contribute. 

1. just Add your name to the OWOF contributor list and you can start contributing. 
2. You can either work on an open issue or open an issue and work on it. 
3. issues can also be discussed on our Zulip Channel.



## Sample CSV output

| Root_Directory | File_Path                    | Line_Number | Snippet                        | Priority | Searched_Word | File_Extension |
|----------------|------------------------------|-------------|--------------------------------|----------|---------------|----------------|
| codebase       | ~/codebase/components/foo.js | 3           | myString = "I bought an apple" | 1        | apple         | .js            |
| codebase2      | ~/codebase2/script.rb        | 104         | DOG_CONSTANT: "woof"           | 2        | dog           | .rb            |

## Dependencies

You must have [ripgrep](https://github.com/BurntSushi/ripgrep) and python installed. The script works on both python2 and 3, and does not require any other dependencies other than ripgrep.

Ripgrep was chosen because of its blazing fast speed. To install ripgrep:

```
brew install ripgrep
```

#### Troubleshooting ripgrep

Note: recursively searching your current working directory is the default mode of operation for ripgrep, and in turn, wordfinder.py.

It's unlikely, but if you were expecting to find occurrences but did not, it's possible ripgrep didn't search any files because you have a * rule in a $HOME/.gitignore file. (ripgrep ignores .gitignore files by default.) You can fix this by adding the `--debug` flag to the ripgrep command sequence itself.

#### Ripgrep References  

[https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)


***PS**: This code might not be 100% accurate. please raise issues for corrections.*
