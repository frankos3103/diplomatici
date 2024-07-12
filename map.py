from game import *
from colors import *


por = Region("POR")
spa = Region("SPA")
bre = Region("BRE")
gas = Region("GAS")
mar = Region("MAR")
pic = Region("PIC")
par = Region("PAR")
bur = Region("BUR")
hol = Region("HOL")
bel = Region("BEL")
den = Region("DEN")
kie = Region("KIE")
ruh = Region("RUH")
ber = Region("BER")
mun = Region("MUN")
tyr = Region("TYR")
pie = Region("PIE")
tus = Region("TUS")
rom = Region("ROM")
nap = Region("NAP")
ven = Region("VEN")
apu = Region("APU")
sil = Region("SIL")
boh = Region("BOH")
vie = Region("VIE")
tri = Region("TRI")
alb = Region("ALB")
gre = Region("GRE")
bud = Region("BUD")
ser = Region("SER")
rum = Region("RUM")
bul = Region("BUL")

por.borders = (spa,)
spa.borders = (por, gas, mar)
bre.borders = (pic, gas, par)
gas.borders = (bre, pic, par, bur, mar, spa)
mar.borders = (spa, gas, bur, pie)
pic.borders = (bre, par, bur, bel)
par.borders = (bre, pic, bur, gas)
bur.borders = (mar, gas, par, pic, bel, ruh, mun)
hol.borders = (kie, bel)
bel.borders = (hol, ruh, bur, pic)
den.borders = (kie,)
kie.borders = (hol, den, ber, mun, ruh)
ruh.borders = (bur, bel, hol, kie, mun)
ber.borders = (kie, sil, mun)
mun.borders = (bur, ruh, kie, ber, sil, boh, tyr)
tyr.borders = (mun, boh, vie, tri, ven, pie)
pie.borders = (mar, tyr, ven, tus)
tus.borders = (pie, ven, rom)
rom.borders = (tus, ven, apu, nap)
nap.borders = (rom, apu)
ven.borders = (apu, rom, tus, pie, tyr, tri)
apu.borders = (nap, rom, ven)
sil.borders = (ber, mun, boh)
boh.borders = (sil, mun, tyr, vie)
vie.borders = (boh, tyr, tri, bud)
tri.borders = (ven, tyr, vie, bud, ser, alb)
alb.borders = (tri, ser, gre)
gre.borders = (alb, ser, bul)
bud.borders = (vie, tri, ser, rum)
ser.borders = (gre, alb, tri, bud, rum, bul)
rum.borders = (bud, ser, bul)
bul.borders = (gre, ser, rum)



germany = Empire("germany")
france = Empire("france")
italy = Empire("italy")
austria = Empire("austria")


bre.startEmpire = france
par.startEmpire = france
mar.startEmpire = france
kie.startEmpire = germany
ber.startEmpire = germany
mun.startEmpire = germany
ven.startEmpire = italy
rom.startEmpire = italy
nap.startEmpire = italy
vie.startEmpire = austria
bud.startEmpire = austria
tri.startEmpire = austria

for i in (por, spa, bre, par, mar, hol, bel, den, kie, ber, mun, rom, nap, ven, vie, tri, gre, bud, ser, rum, bul):
    i.isCenter = True

bre.newUnit(Unit(france)) 
par.newUnit(Unit(france)) 
mar.newUnit(Unit(france)) 
kie.newUnit(Unit(germany))
ber.newUnit(Unit(germany))
mun.newUnit(Unit(germany))
ven.newUnit(Unit(italy))
rom.newUnit(Unit(italy))
nap.newUnit(Unit(italy))
vie.newUnit(Unit(austria))
bud.newUnit(Unit(austria))
tri.newUnit(Unit(austria))


def printmap(season = None):

    with open('map.txt', 'r') as file:
        map = file.read()


    for region in Region.regionList:

        if isinstance(region.controlledBy, Empire):
            match region.controlledBy.name:
                case "germany":
                    map = map.replace(region.name, green(region.name))
                case "france":
                    map = map.replace(region.name, red(region.name))
                case "italy":
                    map = map.replace(region.name, blue(region.name))
                case "austria":
                    map = map.replace(region.name, yellow(region.name))

        name = region.name.lower()

        if region.occupant.name == None:
            if region.standoff == True:
                map = map.replace(name, " X ")
            else:
                map = map.replace(name, "   ")
            continue
        string = "   "

        match region.occupant.name:
            case "germany":
                string = green("■")
            case "france":
                string = red("■")
            case "italy":
                string = blue("■")
            case "austria":
                string = yellow("■")            
            case _:
                string = " "

        if region.loser.name != None:
            match region.loser.name:
                case "germany":
                    string += green(" □")
                case "france":
                    string += red(" □")
                case "italy":
                    string += blue(" □")
                case "austria":
                    string += yellow(" □") 
        else:
            string += "  "

        map = map.replace(name, string)

    print(map)

    if season != None:
        print(season)

printmap()
