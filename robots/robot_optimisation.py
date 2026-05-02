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

DURATION = "1 week"


OPTIMISED_CHARGERS = [[20, 10], [60, 10], [40, 35]]

HOME = [40, 20, 0]


BASELINE_THRESHOLD = 0.2



OPP_RADIUS = 6
OPP_SOC = 0.6

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

def nearest_pizza(bot, es):
  pass

def nearest_charger(bot, chargers):
  return min(chargers, key = lambda c: distance(bot.coordinates, c.coordinates)) # this function allows the robot to find the nearest charger whilst running the code


def opportunistic_charge(bot, chargers):
     # If the bot is going to a station, don't go to this one
  if bot.station is not None:
    return None
    
  if bot.soc / bot.max_soc >= OPP_SOC:
    return None   # battery is healthy enough

  for charger in chargers:
    if distance(bot.coordinates, charger.coordinates) <= OPP_RADIUS:
      return charger # returns the closest charger given the distance is small.

  return None


def kpis(es): # This Function returns the KPI's for the system once run.
  bots = list(es.registry(kind_class = "Bot").values())
  return {
    "bots" : bots,
    "units": sum(r["units_delivered"] for r in bots), #this is tallying the number of elements in each list
    "weight": sum(r["weight_delivered"] for r in bots),
    "energy": sum(r["energy"] for r in bots),
    "distance": sum(r["distance"] for r in bots),
    "broken": sum(1 for r in bots if r["status"] == "broken"),

  }



def print_table(k, label):
    #Print a per-bot KPI table for one run. This is printed using f strings
    print(f"\n{'='*72}\n  {label}\n{'='*72}")
    print(f"{'Name':<8} {'Kind':<7} {'Status':<9} {'Units':>6} {'Weight':>8} {'Energy':>8} {'Dist':>8}")
    print("-" * 72)
    for r in k['bots']:
        flag = "  *** BROKEN ***" if r['status'] == 'broken' else ""
        print(f"{r['name']:<8} {r['kind']:<7} {r['status']:<9} "
              f"{r['units_delivered']:>6} {r['weight_delivered']:>8} "
              f"{r['energy']:>8.0f} {r['distance']:>8.1f}{flag}")
    print("-" * 72)
    print(f"{'TOTALS':<25} {k['units']:>6} {k['weight']:>8} {k['energy']:>8.0f} {k['distance']:>8.1f}")
    print(f"  Broken bots: {k['broken']}\n{'='*72}")


def print_comparison():
  pass

def run_baseline():
  # Stating the Test Variables
  DROIDS = 3
  DRONES = 4
  ROBOTS = 4
  PIZZAS = 10
  BASELINE_CHARGERS = [40,20]


  print(">> Baseline is running <<")
  es = ecofactory(robots = ROBOTS, droids = DROIDS, drones = DRONES, chargers = BASELINE_CHARGERS, pizzas = PIZZAS)

  charger, es.duration, es.messages_on = es.chargers()[0], DURATION, False
  es.display(show = 0)

  while es.active:
    for bot in es.bots():
      if bot.soc/bot.max_soc < BASELINE_THRESHOLD and not bot.station: # if the bot is less than the thresholda nd not at a charger
        bot.charge(charger)
      if bot.activity == "idle": # if the bot is available, give it a pizza
        for p in es.deliverables():
          if p.status == "ready":
            bot.deliver(p)
            break
        if not bot.destination and bot.coordinates != HOME: # When the robot is not at home
          bot.target_destination = HOME
      if bot.target_destination: # move the robot to the target destination
        bot.move()
    es.update()

    k = kpis(es)
    print_table()
    return(k)



def run_optimised():
  print(">> Optimised is running <>")

  DROIDS = 3
  DRONES = 4
  ROBOTS = 4
  PIZZAS = 10
  OPP_CHARGERS = ([55, 20], [20, 10], [70, 30])
  OPP_THRESHOLDS = {
   "Robot": 0.28, 
   "Droid": 0.22,
   "Drone": 0.30
   }

  es = ecofactory(robots = ROBOTS, drones = DRONES, droids = DROIDS, chargers = OPP_CHARGERS, pizzas = PIZZAS)
  chargers, es.duration, es.messages_on = es.charger(), DURATION, False
  es.display

  while es.active:
    for bot in es.bots():
      threshold = OPP_THRESHOLDS.get(bot.kind, BASELINE_THRESHOLD)
      if bot.soc/bot.max_soc < threshold and not bot.station:
        bot.charge(nearest_charger(bot, chargers))
      
      elif bot.activity in ("delivering", "collecting", "moving"): # Topping up whilst moving
        opp = opportunistic_charge(bot, chargers)
        
        if opp:
          bot.charge(opp)

        if bot.activity == "idle":
          p = nearest_pizza(bot, es)
          if p:
            bot.deliver(p)

          elif not bot.destination and bot.coordinates != HOME: # Go home if the Robot is not at home
            bot.target_destination = HOME

        if bot.target_destination:
          bot.move()

      es.update()

    k = kpis(es)
    print_table()
    return k
  


if __name__ == "__main__":
  plt.close("all")
  plt.ion()

  b = run_baseline()
  o = run_optimised()
  print_comparison() # This needs to be programmed to print out the KPI's





