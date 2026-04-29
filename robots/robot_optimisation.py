"""
KPI's

Units delivered - the number of pizzas delivered
weight delivered - the weight of pizzas delivered
energy - Energy used by robot
distance - distance travelled
damage - damage taken by bot

"""

from robots.ecosystem.factory import ecofactory
from robots.ecosystem.ecosystem import distance


import matplotlib as plt
plt.close("all")
plt.ion()


optimum_radius = 6
charge_threshold = 30

setting = ecofactory(robots = 3, droids = 4, drones = 5, chargers = ([55, 20], [30, 40], [70, 30]), pizzas  = 10)

charger = setting.chargers()[0]

def low_battery():
    for bot in setting.bots():
        if bot.soc/ bot.maxsoc < charge_threshold and bot.station == None:
            bot.charge(charger)




