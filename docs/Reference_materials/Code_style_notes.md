# Code style

Code is for communication: to the computer and to other programmers. 
Should always be able to answer "yes" to the question: at any moment, could I hand this to someone else?

We will follow Python conventions in R as well. For more information on R, see [here](https://mikoontz.github.io/data-carpentry-week/).

Two categories of code:
* **Libraries**: e.g. OpenBird
  * The legos; an engineering problem
  * A bunch of function definitions
  * Libraries are tested 
     * ("unit testing": testing normal & boundary cases on a single function)
* **Scripts**: 
  * the towers; like writing a document

### Style for libraries
```
# Function imports at the top
import numpy as np

# Function defs

def function():
   '''Docstring: one quick phrase
   
   Longer description
   
   Args:
    list: description/requirements
     
   Returns:
    list:
   '''
   
   # Comment liberally
   #    --> use comments as section headers
   #    --> if it takes you more than 5 seconds to understand, comment it
   
   # Not useful: set x to 0
   # It's okay to do things the "stupid way" if it's easier to understand
   x = 0
   
   # Useful: initialize population at time zero
   pop_zero = 0
   
   # Make counters descriptive (not i, but instead, num_birds)
   
   # Keep functions short--if the code takes more than one screen, consider breaking it up
```

R conventions: R allows dots in var/function names... Don't do that. Just use camelCase

### Thoughts on testing
If you find a bug, immediately write a test for it!

Avoids the "don't touch it" syndrome--you can change old code and run your tests to be sure it still works.

Python library for testing: `pytest`

### Style for scripts
Several dirs within `repository/`:
+ `calcs/` - or `src/`. Your code 
+ `man/` - your manuscript


Within calcs/src, numbered subdirectories give order of operations, contain Jupyter notebooks, results, & files, etc.

RE: Jupyter notebooks - use *literate programming*. Take advantage of text functionality and write notebook as a document. Could somebody follow along without you being there?

### Testing scripts: the "smoke test"
Make a very small example dataset where you know the output

Make a variable at the top for the path to the data file; switch that between test & actual output when needed

