## Overview of design decisions
This is a simple implementation of an application that deals with credit 
card information.
For disaster recovery, I chose to have a persistent layer. 
Python **shelve** library provided a dictionary-like API to store data locally.
**shelve** is built on top of **pickle**, another library to serialize data. However,
with **shelve**, since it provides a dict-like object, it's a lot more convenient.
The **shelve** data would look like this:

```
{
"Tom": [
{"card_number": "4111111111111111", "balance": 123, "limit": 1000},
{another card here}
], 
"Another person":[their cards]
}
```
I chose to have the name as the key due to Charge and Credit commands not specifying
the card number. 
Implementation details:
For Add:
- Check if card satisfies Luhn 10 and card_number not existing yet. 
After a few quick Google searches, my understanding of credit card number is that
account number is a part of every card number. Therefore, I decided to make it unique.
- One user can have many cards, as can be seen in the example of shelve above.

For Charge:
capacity = sum(limit-balance, list of cards that user owns)
- Charges will be distributed among the cards that a user owns. 
- Charges that are over the capacity will be ignored.

For Credit:
- I chose to just apply credit to the first, instead of distributing like Charge,
because I could see cases where having a negative credit balance on a specific card be
useful.

Due to my choice of storing data in **shelve**, the program will be stateful in the 
sense that it would keep a database of users, data of their cards 
(number, limit, balance) and reload every time.
If you want to start a fresh run, simply delete the local shelve object
```
rm accounts
```

## Why Python?
Python is one of the languages that I'm comfortable using. In my opinion,
it has a very readable syntax and is especially useful for spinning up a PoC.
Python is also installed by default in many popular Linux distros, such as RHEL
and Debian family, Mac OS X, etc. 

## How to run
# Code
To run code, you'll need to have Python installed. To install dedepencies, you can use
pip (https://packaging.python.org/install_requirements_linux/)
```
pip install luhn
tar -xvzf braintree.tar.gz
python3 main.py input_file.txt
```
where input_file.txt is the file that contains the commands.

# Test
With shelve being a dict-like object, it was very straightforward to write tests
```
python3 processor_test.py
```
Test functional coverage is not 100%, but it's a showcase of how I usually write unit
tests in Python.
