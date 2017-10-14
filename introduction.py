import aiml
import os

sessionId = 123
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b",sessionId)
kernel.verbose(True)


# TODO : populate this list with dictionaries (nume,age,job)
def load_persons():
    _persons = []
    if os.path.isfile("persons"):
        f = open("persons", "r")
        for line in f.readlines():
            _persons.append(eval(line))

    return _persons

def write_persons():
    f = open("persons", "w")
    for person in persons:
        f.write(str(person))


persons = load_persons()




def can_identify(nume, age, occupation):
    # check if the nume appears twice
    # fac un for care sa imi aduca persoanele
    nume_filtered = filter(lambda x : x["nume"] == nume, persons)
    if len(list(nume_filtered)) == 1:
        return True
    if age != None:
        age_filtered = filter(lambda x : x["age"] == age, nume_filtered)
        if len(list(age_filtered)) == 1:
            return True
        if occupation != None:
            job_filtered = filter(lambda x : x["job"] == occupation, age_filtered)
            if len(list(job_filtered)) == 1:
                return True

    return False


def find_age():
    kernel.setPredicate("age","",sessionId)
    kernel.setPredicate("topic","ASKAGE",sessionId)
    print(kernel.respond("secret trigger",sessionId))
    while kernel.getPredicate("age",sessionId) == "":
        print(kernel.respond(input(),sessionId))
    return kernel.getPredicate("age",sessionId)


def find_occupation():
    kernel.setPredicate("job","",sessionId)
    kernel.setPredicate("topic","ASKJOB",sessionId)
    print(kernel.respond("secret trigger",sessionId))
    while kernel.getPredicate("job",sessionId) == "":
        print(kernel.respond(input(),sessionId))
    return kernel.getPredicate("job",sessionId)

# TODO implement storing method
# If there is no entry with this person
def add_person(nume, age, occupation):
    new_person = { "nume" : nume, "age" : age, "job" : occupation}
    persons.append(new_person)
    write_persons()


# Get confirmation that all the entries are correct
def confirm():
    kernel.setPredicate("topic","CONFIRM",sessionId)
    print(kernel.respond("secret trigger",sessionId))
    while kernel.getPredicate("conf",sessionId) == "":
        print(kernel.respond(input(),sessionId))
    if kernel.getPredicate("conf",sessionId) == "TRUE":
        return True
    return False


while len(kernel.getPredicate("nume",sessionId)) == 0:
    print(kernel.getPredicate("nume",sessionId))
    print(kernel.respond(input(),sessionId))

nume = kernel.getPredicate("nume",sessionId)
age = None
occupation = None

while not can_identify(nume, age, occupation):
    if age == None:
        age = find_age()
    elif occupation == None:
        occupation = find_occupation()
    else:
        break


def get_matched_age(nume):
    for person in persons:
        if person["nume"] == nume:
            return person["age"]

def get_matched_occupation(nume, age):
    for person in persons:
        if person["nume"] == nume and person["age"] == age:
            return person["job"]

if age == None:
    age = get_matched_age(nume)

if occupation == None:
    occupation = get_matched_occupation(nume,age)

kernel.setPredicate("age",age,sessionId)
kernel.setPredicate("job",occupation, sessionId)

if not confirm():
    age = find_age()
    occupation = find_occupation()
    add_person(nume,age,occupation)
elif not can_identify(nume, age, occupation):
    add_person(nume,age,occupation)

print(kernel.respond("CHANGE TOPIC", sessionId))
while True:
    print(kernel.respond(input(),sessionId))