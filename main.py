from game import *
from map import *

season = SeasonCycle(1901)
printmap(season)
infotext = ('"ok" per eseguire gli ordini'
           '\n"a" per aiuto con i comandi'
           '\n"q" per uscire dal gioco')
print(infotext)

while True:
    text = input()
    match text.upper():
        case "OK":
            evaluateSeason(season)
            printmap(season)
        case "Q":
            exit()
        case "A":
            print('AAA-BBB per muoversi da AAA a BBB\n'
                  'AAA S BBB per supporto difensivo a BBB\n'
                  'AAA S BBB-CCC per supporto offensivo all\'attacco BBB-CCC\n'
                  'AAA S per restare in difesa (opzione di default)')
        case _:
            inputMove(text, season.current())