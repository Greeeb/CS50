from logic import *

houses = [f"{i}" for i in range(1,6)]
colors = ["yellow", "blue", "red", "ivory", "green"]
nation = ["norvegian", "ukrainian", "englishman", "spaniard", "japanese"]
drink = ["water", "tea", "milk", "orange juice", "coffee"]
smoke = ["kools", "chesterfields", "old gold", "lucky strike", "parliaments"]
pet = ["fox", "horse", "snails", "dog", "zebra"]
terms = [houses, colors, nation, drink, smoke, pet]

for i in terms:
    for symbols in i:
        Symbol(symbols)

knowledge = And(
    And(Symbol("englishman"), Symbol("red")),
    And(Symbol("spaniard"), Symbol("dog")),
    And(Symbol("coffee"), Symbol("green")),
    And(Symbol("ukrainian"), Symbol("tea")),
    And(Symbol("old gold"), Symbol("snails")),
    And(Symbol("kools"), Symbol("yellow")),
    And(Symbol("milk"), Not(Symbol("1")), Not(Symbol("5"))),
    And(Symbol("norvegian"), Symbol("1")),
    And(Symbol("lucky strike"), Symbol("orange juice")),
    And(Symbol("japanese"), Symbol("parliaments")),
)

#The green house is immediately to the right of the ivory house.
temp = And()
for i in range(1,5):
    temp.add(Biconditional(And(Symbol("ivory"),Symbol(f"{i}")), And(Symbol("green"),Symbol(f"{i+1}"))))
knowledge.add(temp)

#The man who smokes Chesterfields lives in the house next to the man with the fox.
temp = And()
for i in range(1,6):
    if i == 1:
        temp.add(Biconditional(And(Symbol("chesterfields"),Symbol(f"{i}")), And(Symbol("fox"),Symbol(f"{i+1}"))))
    elif i == 5:
        temp.add(Biconditional(And(Symbol("chesterfields"),Symbol(f"{i}")), And(Symbol("fox"),Symbol(f"{i-1}"))))
    else:
        temp.add(Or(Biconditional(And(Symbol("chesterfields"),Symbol(f"{i}")), And(Symbol("fox"),Symbol(f"{i+1}"))),
                   Biconditional(And(Symbol("chesterfields"),Symbol(f"{i}")), And(Symbol("fox"),Symbol(f"{i-1}")))))
knowledge.add(temp)

#Kools are smoked in the house next to the house where the horse is kept.
temp = And()
for i in range(1,6):
    if i == 1:
        temp.add(Biconditional(And(Symbol("kools"),Symbol(f"{i}")), And(Symbol("horse"),Symbol(f"{i+1}"))))
    elif i == 5:
        temp.add(Biconditional(And(Symbol("kools"),Symbol(f"{i}")), And(Symbol("horse"),Symbol(f"{i-1}"))))
    else:
        temp.add(Or(Biconditional(And(Symbol("kools"),Symbol(f"{i}")), And(Symbol("horse"),Symbol(f"{i+1}"))),
                   Biconditional(And(Symbol("kools"),Symbol(f"{i}")), And(Symbol("horse"),Symbol(f"{i-1}")))))
knowledge.add(temp)

#The norvegian lives next to the blue house.
temp = And()
for i in range(1,6):
    if i == 1:
        temp.add(Biconditional(And(Symbol("norvegian"),Symbol(f"{i}")), And(Symbol("blue"),Symbol(f"{i+1}"))))
    elif i == 5:
        temp.add(Biconditional(And(Symbol("norvegian"),Symbol(f"{i}")), And(Symbol("blue"),Symbol(f"{i-1}"))))
    else:
        temp.add(Or(Biconditional(And(Symbol("norvegian"),Symbol(f"{i}")), And(Symbol("blue"),Symbol(f"{i+1}"))),
                   Biconditional(And(Symbol("norvegian"),Symbol(f"{i}")), And(Symbol("blue"),Symbol(f"{i-1}")))))
knowledge.add(temp)


for color in colors:
    knowledge.add(Biconditional(And(Symbol(color),Symbol("1")), 
                              Not(Or(And(Symbol(color),Symbol("2")), 
                                     And(Symbol(color),Symbol("3")), 
                                     And(Symbol(color),Symbol("4")), 
                                     And(Symbol(color),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(color),Symbol("2")), 
                              Not(Or(And(Symbol(color),Symbol("1")), 
                                     And(Symbol(color),Symbol("3")), 
                                     And(Symbol(color),Symbol("4")), 
                                     And(Symbol(color),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(color),Symbol("3")), 
                              Not(Or(And(Symbol(color),Symbol("2")), 
                                     And(Symbol(color),Symbol("1")), 
                                     And(Symbol(color),Symbol("4")), 
                                     And(Symbol(color),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(color),Symbol("4")), 
                              Not(Or(And(Symbol(color),Symbol("2")), 
                                     And(Symbol(color),Symbol("3")), 
                                     And(Symbol(color),Symbol("1")), 
                                     And(Symbol(color),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(color),Symbol("5")), 
                              Not(Or(And(Symbol(color),Symbol("2")), 
                                     And(Symbol(color),Symbol("3")), 
                                     And(Symbol(color),Symbol("4")), 
                                     And(Symbol(color),Symbol("1"))))))

for nat in nation:
    knowledge.add(Biconditional(And(Symbol(nat),Symbol("1")), 
                              Not(Or(And(Symbol(nat),Symbol("2")), 
                                     And(Symbol(nat),Symbol("3")), 
                                     And(Symbol(nat),Symbol("4")), 
                                     And(Symbol(nat),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(nat),Symbol("2")), 
                              Not(Or(And(Symbol(nat),Symbol("1")), 
                                     And(Symbol(nat),Symbol("3")), 
                                     And(Symbol(nat),Symbol("4")), 
                                     And(Symbol(nat),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(nat),Symbol("3")), 
                              Not(Or(And(Symbol(nat),Symbol("2")), 
                                     And(Symbol(nat),Symbol("1")), 
                                     And(Symbol(nat),Symbol("4")), 
                                     And(Symbol(nat),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(nat),Symbol("4")), 
                              Not(Or(And(Symbol(nat),Symbol("2")), 
                                     And(Symbol(nat),Symbol("3")), 
                                     And(Symbol(nat),Symbol("1")), 
                                     And(Symbol(nat),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(nat),Symbol("5")), 
                              Not(Or(And(Symbol(nat),Symbol("2")), 
                                     And(Symbol(nat),Symbol("3")), 
                                     And(Symbol(nat),Symbol("4")), 
                                     And(Symbol(nat),Symbol("1"))))))

for dri in drink:
    knowledge.add(Biconditional(And(Symbol(dri),Symbol("1")), 
                              Not(Or(And(Symbol(dri),Symbol("2")), 
                                     And(Symbol(dri),Symbol("3")), 
                                     And(Symbol(dri),Symbol("4")), 
                                     And(Symbol(dri),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(dri),Symbol("2")), 
                              Not(Or(And(Symbol(dri),Symbol("1")), 
                                     And(Symbol(dri),Symbol("3")), 
                                     And(Symbol(dri),Symbol("4")), 
                                     And(Symbol(dri),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(dri),Symbol("3")), 
                              Not(Or(And(Symbol(dri),Symbol("2")), 
                                     And(Symbol(dri),Symbol("1")), 
                                     And(Symbol(dri),Symbol("4")), 
                                     And(Symbol(dri),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(dri),Symbol("4")), 
                              Not(Or(And(Symbol(dri),Symbol("2")), 
                                     And(Symbol(dri),Symbol("3")), 
                                     And(Symbol(dri),Symbol("1")), 
                                     And(Symbol(dri),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(dri),Symbol("5")), 
                              Not(Or(And(Symbol(dri),Symbol("2")), 
                                     And(Symbol(dri),Symbol("3")), 
                                     And(Symbol(dri),Symbol("4")), 
                                     And(Symbol(dri),Symbol("1"))))))

for smo in smoke:
    knowledge.add(Biconditional(And(Symbol(smo),Symbol("1")), 
                              Not(Or(And(Symbol(smo),Symbol("2")), 
                                     And(Symbol(smo),Symbol("3")), 
                                     And(Symbol(smo),Symbol("4")), 
                                     And(Symbol(smo),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(smo),Symbol("2")), 
                              Not(Or(And(Symbol(smo),Symbol("1")), 
                                     And(Symbol(smo),Symbol("3")), 
                                     And(Symbol(smo),Symbol("4")), 
                                     And(Symbol(smo),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(smo),Symbol("3")), 
                              Not(Or(And(Symbol(smo),Symbol("2")), 
                                     And(Symbol(smo),Symbol("1")), 
                                     And(Symbol(smo),Symbol("4")), 
                                     And(Symbol(smo),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(smo),Symbol("4")), 
                              Not(Or(And(Symbol(smo),Symbol("2")), 
                                     And(Symbol(smo),Symbol("3")), 
                                     And(Symbol(smo),Symbol("1")), 
                                     And(Symbol(smo),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(smo),Symbol("5")), 
                              Not(Or(And(Symbol(smo),Symbol("2")), 
                                     And(Symbol(smo),Symbol("3")), 
                                     And(Symbol(smo),Symbol("4")), 
                                     And(Symbol(smo),Symbol("1"))))))

for p in pet:
    knowledge.add(Biconditional(And(Symbol(p),Symbol("1")), 
                              Not(Or(And(Symbol(p),Symbol("2")), 
                                     And(Symbol(p),Symbol("3")), 
                                     And(Symbol(p),Symbol("4")), 
                                     And(Symbol(p),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(p),Symbol("2")), 
                              Not(Or(And(Symbol(p),Symbol("1")), 
                                     And(Symbol(p),Symbol("3")), 
                                     And(Symbol(p),Symbol("4")), 
                                     And(Symbol(p),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(p),Symbol("3")), 
                              Not(Or(And(Symbol(p),Symbol("2")), 
                                     And(Symbol(p),Symbol("1")), 
                                     And(Symbol(p),Symbol("4")), 
                                     And(Symbol(p),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(p),Symbol("4")), 
                              Not(Or(And(Symbol(p),Symbol("2")), 
                                     And(Symbol(p),Symbol("3")), 
                                     And(Symbol(p),Symbol("1")), 
                                     And(Symbol(p),Symbol("5"))))))
    knowledge.add(Biconditional(And(Symbol(p),Symbol("5")), 
                              Not(Or(And(Symbol(p),Symbol("2")), 
                                     And(Symbol(p),Symbol("3")), 
                                     And(Symbol(p),Symbol("4")), 
                                     And(Symbol(p),Symbol("1"))))))


solutions = []
for house in houses:
    for color in colors:
        for nat in nation:
            for dri in drink:
                for smo in smoke:
                    for p in pet:
                        solutions.append(And(Symbol(house), Symbol(color), Symbol(nat), Symbol(dri), Symbol(smo), Symbol(p)))


#print(temp.formula())
#print(knowledge.formula())

"""if model_check(knowledge, And(Symbol("1"), Symbol("yellow"), Symbol("norvegian"), Symbol("water"), Symbol("kools"), Symbol("fox"))):
    print(And(Symbol("1"), Symbol("yellow"), Symbol("norvegian"), Symbol("water"), Symbol("kools"), Symbol("fox")))
"""