import aiml
import fileinput

kernel = aiml.Kernel()
kernel.learn("std-startup.xml")

while True:
    kernel.respond("load aiml b",123)
    sessionData = kernel.getSessionData(123);
    print(kernel.getPredicate("topic", 123))
    print(sessionData)
    print(kernel.getBotPredicate("topic"))
    print(kernel.respond(input()))
