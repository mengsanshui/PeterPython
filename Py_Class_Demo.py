class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
         self.pay = int(self.pay * (1 + percent))
    def __repr__(self):
        return '[Person: %s , %s]' % (self.name, self.pay)


class Manager(Person):
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)

class MixedNames: # Define class
    data = 'spam' # Assign class attr
    def __init__(self, value): # Assign method name
        self.data = value # Assign instance attr
    def display(self):
        print(self.data, MixedNames.data)

class Super:
    def method(self):
        print('in Super.method') # Default behavior
    def delegate(self):
        self.action() # Expected to be defined
    def action(self):
        assert False, 'action method  must be defined!'

class Inheritor(Super): # Inherit method verbatim
    pass

class Replacer(Super): # Replace method completely
    def method(self):
        print('in Replacer.method')

class Extender(Super): # Extend method behavior
    def method(self):
        print('starting Extender.method')
        Super.method(self)
        print('ending Extender.method')

class Provider(Super): # Fill in a required method
    def action(self):
        print('in Provider.action')


class Prod:
    def __init__(self, value): # Accept just one argument
        self.value = value
    def __call__(self, other):
        return self.value * other


class Callback:
    def __init__(self, color): # Function + state information
        self.color = color
    def __call__(self): # Support calls with no arguments
        print('turn', self.color)

# Handlers
#cb1 = Callback('blue') # Remember blue
#cb2 = Callback('green') # Remember green
#B1 = Button(command=cb1) # Register handlers
#B2 = Button(command=cb2)
# Events
#cb1() # Prints 'turn blue'
#cb2() # Prints 'turn green'

def callback(color): # Enclosing scope versus attrs
    def oncall():
        print('turn', color)
    return oncall
#cb3 = callback('yellow') # Handler to be registered
#cb3() # On event: prints 'turn yellow'

class Callback:
    def __init__(self, color): # Class with state information
        self.color = color
    def changeColor(self): # A normal named method
        print('turn', self.color)

#cb1 = Callback('blue')
#cb2 = Callback('yellow')
#B1 = Button(command=cb1.changeColor) # Bound method: reference, don't call
#B2 = Button(command=cb2.changeColor) # Remembers function + self pair

class ListInstance:
    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):
            result += '\t%s=%s\n'% (attr, self.__dict__)
            return result

    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
                    self.__class__.__name__, # My class's name
                    id(self),                # My address
                    self.__attrnames())      # name=value list

if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(bob.name, bob.pay)
    print(sue.name, sue.pay)
    print(bob.lastName(), sue.lastName())
    sue.giveRaise(.10)
    print(sue.pay)
    print(sue)

    mix1 = MixedNames(1)
    mix2 = MixedNames(2)
    print(mix1.data, mix2.data, sep='\n')

    for klass in (Inheritor, Replacer, Extender):
        print('\n' + klass.__name__ + '...')
        klass().method()
    # klass().delegate()
    print('\nProvider...')
    x = Provider()
    x.delegate()

    c = Prod(2)
    print(c.value, c(3))

