Welcome to nylo
========================

|image0|

::

   print("Tau World! :D")

**Nylo** is a declarative programming language. It takes some constructs
from functional and logic paradigms, but it’s really a new paradigm
itself. It aims to be simple and clear, but powerful. It provides an
easy way to make assertions on the data a function is working on. It
also gives you the possibility to define standard behaviour if asserts
fail.

::

   fib:
       int n
       int sum_prev_fibs: fib(n-1) + fib(n-2)
       int result: if(n<2 n sum_prev_fibs)
       -> result

Contents
========

-  `How to contribute`_
-  `Present and future of project`_
-  `Features`_

   1. `It’s simple and orthogonal`_
   2. `It’s explicit and clear`_
   3. `Curried function and classes`_
   4. `Inverse function and classes`_
   5. `Functional costructs and more`_
   6. `Check if you are screwing up`_

How to contribute
-----------------

*In primis* (“firstable”), you **must** be a member of `pyTeens`_, then
**ask** @veggero!

Present and future of project
-----------------------------

This repo contains the development version of the proof-of-concept of
the programming language. The poc should be finished on the 25th of May,
but due to complications in the type and overloading systems, it might
slip further.

As soon as the proof-of-concept is finished and refined, the work on the
actual interpreter will start. It will be written in C++.

Features
--------

It’s simple and orthogonal
~~~~~~~~~~~~~~~~~~~~~~~~~~

Nylo has very few constructs. In fact, dictionaries, lists, objects,
function and classes are all the same thing:

::

   // List
   to_review:
       "Milk"
       "Sugar"
       "Salt"
       
   // Dict
   reviewed:
       "Nougat": 10
       "Honey": 9
       "Chocolate": 7
       
   // Class
   point:
       int x
       int y
       
   // Function
   double:
       int n
       r: n * 2
       -> r

It’s explicit and clear
~~~~~~~~~~~~~~~~~~~~~~~

Nylo makes everything explicit, even function calls!

::

   draw:
       on: screen
       color: color(r: 0 g: 255 b: 255)
       rectangle:
           center: point(x: 5 y: 15)
           size: point(x: 10 y: 10)

The same thing with pygame is:

::

   pygame.draw.rect(
       screen,
       (255, 0, 0),
       (5, 15, 10, 10)
   )

As you can see, Nylo is way clearer.

Curried function and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not all arguments has to be passed in the first call.

::

   add:
       int a
       int b
       -> a + b

   add(1 2) = 3
   add_three: add(3)
   add_four: add(4)
   add_three(5) = 8

Also, not all class proprieties has to be passed in the first call.

::

   point:
       int x
       int y
       
   A: point(x: 5, y: 10)

   x_axis: point(y: 0)
   y_axis: point(x: 0)

   B: x_axis(x: 5)
   C: y_axis(y: 10)

Inverse function and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can make function that also works backward:

::

   double:
       int n: result / 2
       int result: n * 2
       -> result

   double(10) = 20
   double(result: 18 -> n) = 9

And you can also have multiple ways to define classes:

::

   color:
       int r: hex[1:3].base_10
       int g: hex[3:5].base_10
       int b: hex[5:7].base_10

       str hex: '#' & r.base_16 & g.base_16 & b.base_16
       
   color(r: 255 g: 0 b: 0)
   color(hex: "#ff0000")

   color(r: 0 g: 122 b: 54 -> hex)
   color(hex: "#c8ec8e" -> r)

Functional costructs and more
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nylo has most of the functional costructs, such as map (it’s called
“for” in nylo), filter, and so on.

::

   testlist: (1, 15, 7, 25, 4, 6)

   for(testlist, *2)
   filter(testlist, <10)

   for
       testlist
       (int n -> if(n < 0, "LOW", "HIGH"))

Check if you are screwing up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Nylo, you can explicit say what you expect a variable to be like. An
exception will be raised if the condition does not apply.

::

   int[<10] low_number
   list[len=10] ten_elements_list

   list char[="0" or ="1"] binary_string
   list[len=3] list[len=3] int tictactoe_board

You can also define a standard value to return or a standard behaviour
to follow if a condition is not followed. Warning will be anyway raised.

::

   int[-> 0] k: "Hello"

   list [len=5 -> print("Wrong lenght!")       // Lenght should be 5
   ] [list[0] == 0 -> print("Wrong header!")   // First element should be 0
   ] t: 0..5

**Copyright** (c) 2017, 2018 `veggero`_. All
rights reserved.

**Copyright** (c) 2018 `pyTeens`_. All rights reserved.

**Copyright** (c) 2018 `Amerigo Guadagno`_. All rights
reserved.

.. _How to contribute: #how-to-contribute
.. _Present and future of project: present-and-future-of-project
.. _Features: #features
.. _It’s simple and orthogonal: #its-simple-and-orthogonal
.. _It’s explicit and clear: #its-explicit-and-clear
.. _Curried function and classes: #curried-function-and-classes
.. _Inverse function and classes: #inverse-function-and-classes
.. _Functional costructs and more: #functional-costructs-and-more
.. _Check if you are screwing up: #check-if-you-are-screwing-up
.. _pyTeens: https://teens.python.it
.. _veggero: https://github.com/veggero
.. _Amerigo Guadagno: https://github.com/AmerigoGuadagno

.. |image0| image:: https://raw.githubusercontent.com/pyTeens/nylo/gh-pages/docs/images/new_big_nylo_banner.png
