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

HOME = [40, 20, 0]

BASELINE_THRESHOLD = 0.2

OPP_RADIUS = 6
OPP_SOC = 0.6

BASELINE_MAX_WEIGHT = 20
OPTIMISED_MAX_WEIGHT = 40

PIZZA_POOL_SIZE = 15


def create_deliverables(es, target=PIZZA_POOL_SIZE):
  ready_count = sum(1 for p in es.deliverables() if p.status == "ready")
  for _ in range(max(0, target - ready_count)):
      es.create_thing("Pizza")


def nearest_pizza(bot, es):
  candidates = [
      p for p in es.deliverables()
      if p.status == "ready"
      and p.contractor is None
      and p.weight <= bot.max_payload
  ]
  if not candidates:
      return None
  return min(candidates, key=lambda p: distance(bot.coordinates, p.coordinates))


def nearest_charger(bot, chargers):
  return min(chargers, key=lambda c: distance(bot.coordinates, c.coordinates))


def opportunistic_charge(bot, chargers):
  if bot.station is not None:
    return None  # already committed to a charger

  if bot.soc / bot.max_soc >= OPP_SOC:
    return None  # battery healthy enough

  for charger in chargers:
    if distance(bot.coordinates, charger.coordinates) <= OPP_RADIUS:
        return charger  # return the nearby charger

  return None


def kpis(es):
  bots = list(es.registry(kind_class="Bot").values())
  return {
  "bots":     bots,
  "units":    sum(r["units_delivered"]  for r in bots),
  "weight":   sum(r["weight_delivered"] for r in bots),
  "energy":   sum(r["energy"]           for r in bots),
  "distance": sum(r["distance"]         for r in bots),
  "broken":   sum(1 for r in bots if r["status"] == "broken"),
  }


def print_table(k, label):
  print(f"\n{'='*72}\n  {label}\n{'='*72}") # printed using f strings
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


def print_comparison(b, o):
  def chg(old, new):  # calculate percentage change
      return (new - old) / old * 100 if old else 0.0

  print(f"\n{'='*62}\n Baseline vs Optimised\n{'='*62}")
  print(f"  {'Metric':<22} {'Baseline':>10} {'Optimised':>10} {'Change':>8}")
  print("-" * 62)
  rows = [
      ("Pizzas delivered",   b['units'],    o['units'],    True),
      ("Weight delivered g", b['weight'],   o['weight'],   True),
      ("Energy consumed",    b['energy'],   o['energy'],   False),
      ("Distance travelled", b['distance'], o['distance'], False),
      ("Broken bots",        b['broken'],   o['broken'],   False),
  ]

  for name, bv, ov, up_good in rows:
      d = chg(bv, ov)
      good = (up_good and d > 0) or (not up_good and d < 0)  # fixed: higher pizzas/weight IS good
      tag = "Improved" if good else ("Worse" if d else "")
      print(f"  {name:<22} {bv:<10.1f} {ov:>10.1f} {d:>+7.1f}%{tag}")

  print("=" * 62)


def run_baseline():

  ROBOTS = 4
  DROIDS = 3
  DRONES = 4
  PIZZAS = 10
  BASELINE_CHARGERS = [40, 20]  # single central charger

  print("\n>> Baseline is running <<")
  es = ecofactory(robots=ROBOTS, droids=DROIDS, drones=DRONES,
                  chargers=BASELINE_CHARGERS, pizzas=PIZZAS)

  charger = es.chargers()[0]
  es.duration    = DURATION
  es.messages_on = False
  es.display(show=0)

  while es.active:
      create_deliverables(es)

      for bot in es.bots():
          if bot.status == 'broken':
              continue

          if bot.soc / bot.max_soc < BASELINE_THRESHOLD and not bot.station:
              bot.charge(charger)

          if bot.activity == "idle":
              for p in es.deliverables():
                  if p.status == "ready" and p.contractor is None:
                      bot.deliver(p)
                      break

              if not bot.destination:
                  bot.target_destination = HOME

          if bot.target_destination:
              bot.move()

      es.update()

  k = kpis(es)
  print_table(k, "Baseline KPIs")
  return k


def run_optimised():

  ROBOTS = 4
  DROIDS = 3
  DRONES = 4
  PIZZAS = 10
  OPP_CHARGERS = [[55, 20], [20, 10], [70, 30]]  # three distributed chargers
  OPP_THRESHOLDS = {
      "Robot": 0.28,
      "Droid": 0.22,
      "Drone": 0.30,
  }

  print("\n>> Optimised is running <<")
  es = ecofactory(robots=ROBOTS, droids=DROIDS, drones=DRONES,
                  chargers=OPP_CHARGERS, pizzas=PIZZAS)

  chargers       = es.chargers()
  es.duration    = DURATION
  es.messages_on = False
  es._max_weight = OPTIMISED_MAX_WEIGHT  # raise pizza weight ceiling
  es.display(show=0)

  while es.active:
      create_deliverables(es)

      for bot in es.bots():
          if bot.status == 'broken':
              continue

          threshold = OPP_THRESHOLDS.get(bot.kind, BASELINE_THRESHOLD)

          if bot.soc / bot.max_soc < threshold and not bot.station:
              bot.charge(nearest_charger(bot, chargers))

          elif bot.activity in ("delivering", "collecting", "moving"):
              # Opportunistic top-up whilst already travelling
              opp = opportunistic_charge(bot, chargers)
              if opp:
                  bot.charge(opp)

          if bot.activity == "idle":
              p = nearest_pizza(bot, es)
              if p:
                  bot.deliver(p)
              elif not bot.destination:
                  bot.target_destination = HOME

          if bot.target_destination:
              bot.move()

      es.update()

  k = kpis(es)
  print_table(k, "Optimised KPIs")
  return k


if __name__ == "__main__":
  plt.close("all")
  plt.ion()

  b = run_baseline()
  o = run_optimised()
  print_comparison(b, o)