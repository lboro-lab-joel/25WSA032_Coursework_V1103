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
import matplotlib.pyplot as plt

DROIDS = 3
DRONES = 4
ROBOTS = 4
PIZZAS = 10

DURATION = "1 week"

BASELINE_CHARGERS = [[40,20]]
OPTIMISED_CHARGERS = [[20, 10], [60, 10], [40, 35]]

HOME = [40, 20, 0]


BASELINE_THRESHOLD = 0.2

OPTIMISED_THRESHOLDS = {
   "Robot": 0.28, 
   "Droid": 0.22,
   "Drone": 0.30
}

OPPORTUNISTIC_RADIUS = 6
OPPORTUNISTIC_SOC = 0.6

BASELINE_MAX_WEIGHT = 20
OPTIMISED_MAX_WEIGHT = 40

PIZZA_POOL_SIZE = 15


optimum_radius = 6
charge_threshold = 30


def create_deliverables(es, target = PIZZA_POOL_SIZE):
  
  '''
  This function tries to create enough pizzas in the case they run out.
  '''
  ready_count = sum(1 for p in es.deliverables() if p.status == "ready") # Counts the number of pizzas that are available
  for _ in range(max(0, target- ready_count)): # Way to create missing pizzas
    es.create_thing("Pizza")






plt.close("all")
plt.ion()


es = ecofactory(robots = ROBOTS, drones = DRONES, droids = DROIDS, chargers = CHARGERS, pizzas = PIZZAS)

while es.active:

  for bot in es.bots():
    pass




