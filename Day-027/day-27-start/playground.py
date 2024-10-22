def add(*args):
    # type args -> tuple
    print(args)
    print(args[0])
    sum = 0
    for n in args:
        sum += n
    return sum

# print(add(1, 2, 3, 4, 5))


def calculate(n, **kwargs):
    # type kwargs -> dictionary
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)

    # print(kwargs["add"])
    n += kwargs["add"]
    n *= kwargs["multiply"]
    # print(n)

class Car:

    def __init__(self, **kw):
        # self.make = kw["make"]
        # self.model = kw["model"]
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.colour = kw.get("colour")

my_car = Car(make="Nissan")
print(my_car.model)






calculate(2, add=3, multiply=5)