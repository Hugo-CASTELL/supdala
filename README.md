# Stable marriage parcoursup-like implementation

Authors: [Hugo CASTELL](mailto:hugo.castell@etu.inp-n7.fr) and [Antoine TEXIER](mailto:antoine.texier@etu.inp-n7.fr)

Table of contents: 
1. [Introduction](#1-introduction)
2. [Data format used](#2-data-format-used)
3. [Algorithm](#3-algorithm)
4. [Implementation side](#4-implementation-side)
5. [Performance tests and results](#5-performance-tests-and-results)
6. [Reliability](#6-reliability)
7. [Run it yourself](#7-run-it-yourself)

## 1. Introduction

Parcoursup is the French national online platform used for managing applications to graduating programs.

It uses the Stable Marriage algorithm : [official documentation](https://services.dgesip.fr/T454/S764/algorithme_national_de_parcoursup).

Our project is to implement the algorithm in Python and reduce the time and space complexity between the theoretical algorithm and the implementation.

## 2. Data format used

We used json files as input using this particular structure.
```json
{
  /* Ordered preferences from most to least preferred */
  "students": {
    "Hugo": ["IUT", "ENSEEIHT", "University"],
    "Corentin": ["IUT", "ENSEEIHT", "University"],
    "Antoine": ["ENSEEIHT", "IUT"],
    "Alexis": ["ENSEEIHT", "IUT"],
    "Quentin": ["ENSEEIHT", "University", "IUT"]
  },
  "schools": {
    "IUT": ["Hugo", "Corentin", "Antoine", "Alexis", "Quentin"],
    "University": ["Alexis", "Antoine", "Corentin"],
    "ENSEEIHT": ["Antoine", "Corentin", "Hugo"]
  },
  "capacities": {
    "IUT": 1,
    "University": 2,
    "ENSEEIHT": 1
  }
}
```

## 3. Algorithm

The algorithm side is almost the exact same algorithm of Gale-Shapley with a main difference.

The courtier doesn't come back the next day to check if he is still accepted but is informed when another courtier takes his place

This has the advantage to not iterate through all courtiers each day but only unmatched ones.

```text
Input: 
  - A set of suitors (courtiers), each with an ordered preference list of people to court.
  - A set of individuals to be courted (courted persons), each with their own ordered preferences.

Initialize:
  - Day counter = 0
  - Queue of active suitors = all suitors
  - Set of available courted persons = all courted persons

Repeat while there are active suitors and available courted persons:
  - Increment day
  - For each suitor in the queue:
      - If they are unmatched and still have preferred courted persons:
          - Select their next most preferred courted person
          - Attempt a proposal (see Serenade procedure)

Output:
  - Number of days
  - Final list of suitors with matches
  - Final list of courted persons with matches
```

```text
Procedure Serenade(suitor, courted, next_day_queue, available_courted_set):

  If the courted person does not consider the suitor acceptable:
      - Do nothing (the suitor is implicitly rejected)

  Else:
   If the courted person is currently unmatched:
      - Accept the suitor
      - Record a mutual engagement

   Else:
      - Compare current partner with new suitor
      - Reject the less preferred one

      - If the new suitor is accepted:
          - Cancel previous engagement
          - Add rejected suitor to the next_day_queue (if they still have options)

      - Remove the courted person from the "rumoured to be single" set
```

<details>
<summary>But we do encourage you to check out the code for a more poetic approach while reading the comments</summary>

```python
def stable_marriage(courtiers: list[Courtier], courted_persons: list[Courted]) -> tuple[
    int | Any, list[Courtier], list[Courted]]:
    # Initialize a queue as a set so no doubles can be present
    day = 0
    tomorrow_queue: set[Courtier] = set(courtiers.copy())

    # Rumour grows fast in the village about who is still single or not
    courted_single_from_rumours = set(courted_persons.copy())

    # While there are courtiers with courted on their list and courted persons are not all already married, we continue to find stability
    while tomorrow_queue and courted_single_from_rumours:
        # A new day starts
        day += 1
        today_queue = tomorrow_queue.copy()
        tomorrow_queue.clear()

        # Every courtier that doesn't have a marriage promise will serenade today
        while today_queue:

            # Get the next courtier
            courtier = today_queue.pop()

            # Pop the most preferred courted still on his list
            courted = courtier.pop_next_courted_person_to_serenade()

            # The courtier serenades the courted
            serenade(courtier, courted, tomorrow_queue, courted_single_from_rumours)

            # If the courtier didn't succeed and the courtier still have courted on his list
            if not courtier.has_a_marriage_promise() and courtier.has_courted_persons_to_serenade():
                # He will try serenading somebody else tomorrow
                tomorrow_queue.add(courtier)

    return day, courtiers, courted_persons

def serenade(courtier: Courtier, courted: Courted, tomorrow_queue: set[Courtier], courted_single_from_rumours: set[Courted]):
    # If the courted person doesn't want of the courtier, the person doesn't even show to the window and the courtier gets a refusal
    if not courted.will_appear_at_the_window_for(courtier):
        return

    # Else the serenade starts
    else:
        # Either, the courted person has not already promised marriage and accept by default
        if not courted.has_promised_marriage():
            courted.accept_proposal(courtier)
            courtier.enjoy_and_write_marriage_promise(courted)

        # Or the courted person has already promised marriage to someone else and compare
        else:
            # The courted person debates and choose which proposal to refuse
            refused_courtier = courted.debate(courtier)

            # If our current courtier won
            if refused_courtier != courtier :
                courtier.enjoy_and_write_marriage_promise(courted)
                # The refused courtier will receive a carrier pigeon informing the cancellation of the marriage
                refused_courtier.drink_and_cross_out_marriage_promise(courted)
                if refused_courtier.has_courted_persons_to_serenade():
                    # The refused courtier will need to search love again tomorrow if there are other courted to serenade
                    tomorrow_queue.add(refused_courtier)

            # The refused courtier was drunk at the bar and let a rumour grow in the village
            # about this courted person has found love (between some bad words of course...)
            remove(courted_single_from_rumours, courted)
```

</details>

## 4. Implementation side

### 4.1 Object-Oriented Modeling

We chose OOP Model between it enables a clear separation of roles (proposer vs. decision-maker) and the encapsulation of decision logic (accept/reject) and also reusability for different configurations (students-to-schools or schools-to-students).

Each and every data structure chosen is a O(1) time and space complexity for adding, removing or accessing, either being a set or a dictionary. [Excepts courted marriage promises](#42-efficient-preference-handling--dichotomiclist).

#### `Courtier` : The one who serenades

- **Attributes:**
  - `name`: Identifier of the suitor.
  - `_ordered_courted_to_serenade`: List of courted persons to propose to, ordered by preference.
  - `_marriage_promises`: Set of courted who is engaged with.
  - `_max_marriages`: Maximum number of engagements allowed (1 if student and capacity of school if is).

- **Key Methods:**
  - `pop_next_courted_person_to_serenade()`: Returns the next preferred person to propose to.
  - `has_courted_persons_to_serenade()`: Checks if there are options left to propose to.
  - `has_a_marriage_promise()`: Returns whether the suitor is already fully matched.
  - `enjoy_and_write_marriage_promise()`: Accepts an engagement.
  - `drink_and_cross_out_marriage_promise()`: Cancels a previous engagement.

<details>
<summary>Code</summary>

```python
class Courtier:
    def __init__(self, name, ordered_courted_to_serenade: list[object], max_marriages):
        self.name = name
        self._ordered_courted_to_serenade = ordered_courted_to_serenade

        self._marriage_promises: set[object] = set([])
        self._max_marriages = max_marriages

    def has_courted_persons_to_serenade(self):
        return len(self._ordered_courted_to_serenade) > 0

    def pop_next_courted_person_to_serenade(self) -> object:
        return self._ordered_courted_to_serenade.pop(0)

    def has_a_marriage_promise(self):
        return len(self._marriage_promises) == self._max_marriages

    def enjoy_and_write_marriage_promise(self, courted: object):
        self._marriage_promises.add(courted)

    def drink_and_cross_out_marriage_promise(self, courted: object):
        remove(self._marriage_promises, courted)

    def __str__(self):
        return f"{self.name} -> {str([courted.name for courted in self._marriage_promises])}"
```
</details>

#### `Courted` : The one who receives proposals

- **Attributes:**
  - `name`: Identifier of the courted person.
  - `_preferences`: Dictionary mapping suitor names to preference ranks.
  - `_marriage_promises`: Sorted list (using `DichotomicList`) of current matches.

- **Key Methods:**
  - `will_appear_at_the_window_for(courtier)`: Returns whether the courtier is considered.
  - `has_promised_marriage()`: Checks if the courted person is fully matched.
  - `accept_proposal(courtier)`: Accepts a proposal (if under capacity).
  - `debate(courtier)`: Compares a new proposal with current matches and replaces the least preferred if necessary.

<details>
<summary>Code</summary>

```python
class Courted:
    def __init__(self, name, ordered_courtier_names, max_marriages):
        self.name = name
        self._preferences: dict[str, int] = {courtier_name: i for i, courtier_name in enumerate(ordered_courtier_names)}

        self._marriage_promises: DichotomicList = DichotomicList(max_marriages)

    def will_appear_at_the_window_for(self, courtier: Courtier) -> bool:
        return self._preferences.get(courtier.name) is not None

    def has_promised_marriage(self) -> bool:
        # As the courted is polygamous, we return the max capacity of marriages is reached
        return self._marriage_promises.is_full()

    def accept_proposal(self, courtier: Courtier) -> None:
        self._marriage_promises.insert(self._preferences[courtier.name], courtier)


    def debate(self, courtier: Courtier) -> Courtier:
        return self._marriage_promises.insert_and_pop(self._preferences[courtier.name], courtier)

    def __str__(self):
        return f"{self.name} -> {self._marriage_promises}"
```

</details>

### 4.2 Efficient Preference Handling – DichotomicList

To manage proposals and enforce capacities efficiently, we designed a custom data structure implementation for the courted marriage promises: DichotomicList.

When running the algorithm, we want to do two things when dealing with the marriage promises of a courted person :
1. The number of available marriage promises -> we must keep track of the number marriage promise and capacity
2. Replacing a courtier if a preferred comes to serenade -> we must search for a courtier to replace

For the first point, `len()` with a Python list and storing the max_capacity is enough for O(1) operations.

But for the second point, a basic list would require an O(n) search operation in order to get the desired least preferred courtier promised to reject.

We went for a different approach:
- If we have a sorted list from most to least preferred courtier in our marriage promise
- We can insert at the right place a new courtier
- And if the maximum capacity of marriages is reached : we pop the last one of the list -> the least preferred

What it permits ? Instead of an O(nb mariages promised) operation of research, inserting becomes O(log nb mariages promised) with a binary search and popping becomes O(1).

```python
class PreferenceNode:
    def __init__(self, preference, data):
        self.preference = preference
        self.data = data

    def __str__(self):
        return str(self.data.name)

class DichotomicList:
    def __init__(self, max_capacity):
        self._list = []
        self._max_capacity = max_capacity

    #
    # BINARY HERE -> O(log len(_list))
    #
    def insert(self, preference, data):
        # Creating a new node
        node = PreferenceNode(preference, data)

        # Search the index where inserting the node in order to keep the list sorted
        low = 0
        high = len(self._list) - 1
        while low < high:
            mid = (low + high) // 2
            if node.preference < self._list[mid].preference:
                high = mid
            else:
                low = mid + 1

        # Insert the node at best index
        self._list.insert(low, node)

    #
    # INSTANT POPPING HERE -> O(log len(_list)) + O(1)
    #
    def insert_and_pop(self, preference, data):
        # If the maximum accepted preference is lower than the preference of the insertion candidate, we don't try to insert
        if preference > self._list[-1].preference:
            return data

        self.insert(preference, data)

        # Pop the least preferred from the list and returns it
        return self._list.pop(-1).data

    def is_full(self):
        return len(self._list) == self._max_capacity

    def __str__(self):
        return str([str(node) for node in self._list])
```

### 4.3 Complexity summary

The worst complexity of our implementation is O(n * p * log k) :
- n : number of courtiers
- p : maximum preferences by a courtier as courtier can reference less courted than total of courted
- k : maximum capacity of courted marriage promises

```python
    # stable marriage
    # O(1) + O(1) -> checking sizes of two sets
    while tomorrow_queue and courted_single_from_rumours:
        
        day += 1 # O(1) -> access
        today_queue = tomorrow_queue.copy() # O(1) -> copy of memory pointer address
        tomorrow_queue.clear() # O(1) -> set memory address to null

        # O(1) -> checking size of set
        while today_queue:

            # O(1) + 0(1) -> access + set memory address to null
            courtier = today_queue.pop()

            # O(1) + 0(1) -> access + set memory address to null
            courted = courtier.pop_next_courted_person_to_serenade()

            # See serenade below
            serenade(courtier, courted, tomorrow_queue, courted_single_from_rumours)

            # O(1) + O(1) -> checking sizes of collections
            if not courtier.has_a_marriage_promise() and courtier.has_courted_persons_to_serenade():
                # ~O(1) -> adding new address to list
                tomorrow_queue.add(courtier)

                
    # serenade: 
    # O(1) -> checks key in a dict as hash
    if not courted.will_appear_at_the_window_for(courtier):
        return

    else:
        # O(1) -> checks size of list
        if not courted.has_promised_marriage():
            # ~O(1) -> access and assignations
            courted.accept_proposal(courtier)
            # ~O(1) -> access and assignations
            courtier.enjoy_and_write_marriage_promise(courted)

        else:
            # With Dichotomic List : O(log max_capacity) + O(1)
            refused_courtier = courted.debate(courtier)

            # O(1) -> checks hashcode
            if refused_courtier != courtier :
                # ~O(1) -> access and assignations
                courtier.enjoy_and_write_marriage_promise(courted)
                # O(1) -> remove from list
                refused_courtier.drink_and_cross_out_marriage_promise(courted)
                
                # O(1) -> checks list size
                if refused_courtier.has_courted_persons_to_serenade():
                    # O(1) (+ O(1)) -> checks hashcode and add if not present
                    tomorrow_queue.add(refused_courtier)

            # O(1) + O(1) -> remove if present in set
            remove(courted_single_from_rumours, courted)


```

## 5. Performance tests and results

Context:
Students count : 10000
Schools count : 55
Schools sum capacity : 9925
Iterations : 9022

1. Command : 
```shell
python3 -m cProfile -s cumulative perf_test.py 
```

2. Result
```markdown
 9117648 function calls (9117524 primitive calls) in **2.900 seconds**
```

## 6. Reliability

For testing if our implementation works, we started by trying multiple use case, increasing size slowly and verifying on paper if it worked well :

<details>
<summary>Basic test</summary>

```json
{
  "students": {
    "A":    ["δ", "ɣ", "α", "β"],
    "B":    ["β", "δ", "α", "ɣ"],
    "C":    ["δ", "α", "β", "ɣ"],
    "D":    ["ɣ", "β", "α", "δ"]
  },

  "schools": {
    "α":  ["A", "B", "C", "D"],
    "β":  ["A", "D", "C", "B"],
    "ɣ": ["B", "A", "C", "D"],
    "δ": ["D", "B", "C", "A"]
  },

  "capacities": {
    "α": 1,
    "β": 1,
    "ɣ": 1,
    "δ": 1
  }
}
```

</details>

<details>
<summary>Test with capacities</summary>

```json
{
  "students": {
    "Hugo": ["IUT", "ENSEEIHT", "Université"],
    "Corentin": ["IUT", "ENSEEIHT", "Université"],
    "Antoine": ["ENSEEIHT", "IUT"],
    "Alexis": ["ENSEEIHT", "IUT"],
    "Quentin": ["ENSEEIHT", "Université", "IUT"]
  },
  "schools": {
    "IUT": ["Hugo", "Corentin", "Antoine", "Alexis", "Quentin"],
    "Université": ["Alexis", "Antoine", "Corentin"],
    "ENSEEIHT": ["Antoine", "Corentin", "Hugo"]
  },
  "capacities": {
    "IUT": 1,
    "Université": 2,
    "ENSEEIHT": 1
  }
}
```

</details>

<details>
<summary>Complexified test</summary>

```json
{
  "students": {
    "Hugo": ["IUT", "ENSEEIHT", "Université"],
    "Corentin": ["IUT", "ENSEEIHT", "Université"],
    "Antoine": ["ENSEEIHT", "IUT"],
    "Alexis": ["ENSEEIHT", "IUT"],
    "Quentin": ["ENSEEIHT", "Université", "IUT"],
    "Arthur": ["IUT"],
    "Ken": ["ENSEEIHT", "IUT"],
    "Buisson": ["ENSEEIHT"]
  },
  "schools": {
    "IUT": ["Arthur", "Ken", "Hugo", "Corentin", "Antoine", "Alexis", "Quentin"],
    "Université": ["Alexis", "Antoine", "Corentin", "Buisson"],
    "ENSEEIHT": ["Buisson", "Antoine", "Corentin", "Ken", "Hugo"],
    "ISAE": ["Antoine", "Corentin", "Hugo"]
  },
  "capacities": {
    "IUT": 2,
    "Université": 2,
    "ENSEEIHT": 2,
    "ISAE": 5
  }
}

```

</details>

## 7. Run it yourself

1. Clone the project
```shell
git clone https://github.com/Hugo-CASTELL/supdala.git
```

2. Inside main.py, you can modify the sample data file used

```python
    # HERE around line 10
with open("mydata.json", "r") as f:
    pass
```

3. Then run the main.py
```shell
python3 main.py
```

4. Or run the performance tests (No output)
```shell
python3 -m cProfile -s cumulative perf_test.py 
```