import aiml
import fileinput

kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("LOAD AIML B")

while True:
    print(kernel.respond(input()))
