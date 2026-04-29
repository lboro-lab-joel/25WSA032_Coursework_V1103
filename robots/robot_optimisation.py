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

DROIDS = 3
DRONES = 4
ROBOTS = 4
CHARGERS = ([55, 20], [30, 40], [70, 30])
PIZZAS = 10

import matplotlib as plt
plt.close("all")
plt.ion()


optimum_radius = 6
charge_threshold = 30

setting = ecofactory(ROBOTS, DRONES, DROIDS, CHARGERS, PIZZAS)

charger = setting.chargers()[0]

BASELINE_CONFIG = {
    "charger" : [[40, 20]],
    "charge_threshold" : 0.20,
    "max_pizza_weight" : 20,
    "close_pizza" : False
}

OPTIMISED_CONFIG = {
    "charger" : [[40, 20], [30, 50], [60, 70]],
    "charge_threshold" : 0.35,
    "max_pizza_weight" : 50,
    "close_pizza" : False
}



def low_battery():
    for bot in setting.bots():
        if bot.soc/ bot.maxsoc < charge_threshold and bot.station == None:
            bot.charge(charger)




