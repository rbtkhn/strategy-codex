# Mountain Homestead — 72-Hour Continuity Card

Use for loop **`mountain-homestead-utilities-continuity`**.

Standard: property survives **72 hours** without grid power, with heat, water, communications, and access addressed.

---

## Card header

```yaml
review_date:
season:
last_backup_power_test:
reviewer:
```

---

## Power

```yaml
backup_power_type:            # generator / battery / none
backup_power_tested:          # date / not tested
loads_supported:              # well pump / heat / fridge / comms / lights
fuel_on_hand:
fuel_days_estimate:
failure_chain_if_no_power:    # e.g. no pump → no water → frozen pipes
```

---

## Heat

```yaml
primary_heat:
backup_heat:
freeze_risk_zones:
heat_continuity_72h:          # yes / partial / no
```

---

## Water

```yaml
well_pump_requires_power:     # yes / no
backup_water_storage_gallons:
manual_non_electric_fallback:
freeze_prone_lines:
heat_tape_status:
```

---

## Communications

```yaml
primary_comms:
backup_comms:
emergency_contacts_posted:    # yes / no
```

---

## Access

```yaml
driveway_passable_72h:        # yes / seasonal risk
snow_removal_plan:
evacuation_route_1:
evacuation_route_2:
```

---

## Top continuity actions (before next weather window)

1.
2.
3.

---

## Gaps requiring maintenance backlog

```yaml
gap_1:
gap_2:
```

Strategy: [STRATEGIC-PLAN.md](../STRATEGIC-PLAN.md)
