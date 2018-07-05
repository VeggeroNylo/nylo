a: 
    "this", "is", "cool"
    "a": "first letter", "b": "second one"
    x: 1, y: 2

x: 0
y: "a"

examples:
    a.0
    a.1
    a."a"
    a."b"
    a.x
    a.y
    a.(x)
    a.(y)
    a.(1+1)

-> examples.8
