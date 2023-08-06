# Merkify

Merify is a simple Merkle tree implementation, originally built in Python 3.7.1. The Merkle tree should not be used for deployment or any sophisticated software. It was built for the CS110 course at Minerva.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and for testing the package on your own.

### Prerequisites

The code is written in Python 3.7.1. To test your environment, run in Terminal (bash):

```
$ python
```

### Installing

The package can be installed through `pip` and PyPi. Run the following inside your terminal:

```
pip install Merkify
```

If given `error code 1` from `pip`, proceed to update setup tools:

```
pip install -U setuptools
```
### Use

To initialize tree with a list of items:
`any_name = Merkify(list_with_items_either_int_or_str)`

To find height of tree:
`any_name.fetch_height()`

To fetch depth values at a given depth:
`any_name.fetch_depth_value(int)`

To fetch root values (will be a hash). The root hash is the important part of our Merkle tree, including the overall hashed for all the data blocks. This hash can be found by fetching root value:
`any_name.fetch_root_value()`

### Specific example
```
test_one = [
        'Transaction name:',
        'Transaction date:',
        'Transaction detail:',
        'Transaction amount: '
    ]
    
merkle = Merkify(test_one)
print(merkle.fetch_height())
# Will print 2

print(len(merkle.fetch_depth_value(2)))
# Will print 4

print ("Root Value:", merkle.fetch_root_value())
# Will print a hash
# Ex: 9fa076efc877cdad2ebd902358ae83edca8e1e483dea731e11b1ca49b1a7ad02   
```

### Coding style tests

`pylint` used for coding style sheet with a score of 9.53/10. Code is `PEP8` compliant. To test, run:

```
pylint filedirectory/merkify.py
```

## Deployment

Deployed on PyPi [Merkify](https://pypi.org/project/Merkify/)

## Built With

* [Jupyter](https://jupyter.org/) - Used for development and testing
* [Atom](https://atom.io/) - Text editor used

## Inspration

Taken inspiration from the following implementations of Merkle trees:

* [Tierion]( https://github.com/Tierion/pymerkletools) - For the package tools and abilities to fetch height, depth, and more.
* [Sangeeth Saravanaraj]( https://github.com/sangeeths/merkle-tree) - For general implementation.
* [Jae Duk Seo]( https://github.com/JaeDukSeo/Simple-Merkle-Tree-in-Python) - For general implementation.
* [Jamie Steiner]( https://github.com/jvsteiner/merkletree) - For general implementation.


## License

This project is licensed under the MIT License.
