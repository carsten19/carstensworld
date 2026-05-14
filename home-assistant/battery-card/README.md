# Home Assistant Battery Card

Custom Lovelace card for Home Assistant that shows a battery state of charge with two vertical activity bars for charging and discharging.

- **Video:** https://youtube.com/shorts/lcRq-HvQT7c
- **File:** `battery-card.js`

![Battery Card Placeholder](https://img.shields.io/badge/Home%20Assistant-Custom%20Card-41BDF5)

## Features

- Battery SOC display with Material Design battery icons
- Configurable color stops for SOC ranges
- Separate charging and discharging bars
- Configurable scaling instead of hard-coded power limits
- Responsive layout for different dashboard cell heights
- Visual editor support with helper texts for the main options
- Works well in Home Assistant sections/grid dashboards

## Installation

1. Copy `battery-card.js` into your Home Assistant `www` directory, for example:

   ```text
   /config/www/battery-card/battery-card.js
   ```

2. Add the resource in Home Assistant:

   ```yaml
   url: /local/battery-card/battery-card.js
   type: module
   ```

   In the UI: **Settings → Dashboards → Resources → Add Resource**.

3. Add a manual card:

   ```yaml
   type: custom:battery-card
   label: Hausakku
   batterysoc: sensor.battery_state_of_charge
   charging: sensor.battery_charge_power
   discharging: sensor.battery_discharge_power
   ```

## Configuration

| Option | Required | Default | Description |
|---|---:|---|---|
| `label` | no | empty | Heading above the battery. |
| `batterysoc` | yes | — | Battery state-of-charge entity in percent. |
| `charging` | no | — | Charging power/current entity for the left bar. |
| `discharging` | no | — | Discharging power/current entity for the right bar. |
| `charge_scale` | no | `{min: 0, max: 4, steps: 4, mode: "linear"}` | Scaling for the charging bar. |
| `discharge_scale` | no | `{min: 0, max: 4, steps: 4, mode: "linear"}` | Scaling for the discharging bar. |
| `color_stops` | no | see below | SOC color thresholds. |
| `min_height` | no | `90` | Minimum card height in px for responsive layout. |
| `bar_width` | no | `14` | Width of both vertical bars in px. |
| `icon_size` | no | responsive | Fixed icon size in px. Leave unset for automatic scaling. |
| `value_size` | no | responsive | Fixed percentage text size in px. Leave unset for automatic scaling. |
| `show_zero_bars` | no | `false` | Keep empty bars visible even when the value is zero. |

## Scaling options

The old fixed limits are replaced by configurable scales.

### Linear scale

Best for power sensors with a known useful maximum.

```yaml
charge_scale:
  min: 0
  max: 5
  mode: linear

discharge_scale:
  min: 0
  max: 6
  mode: linear
```

A value halfway between `min` and `max` fills the bar to 50%.

### Step scale

Useful if you prefer chunky 25%/50%/75%/100% bar levels.

```yaml
charge_scale:
  min: 0
  max: 4
  steps: 4
  mode: steps
```

### Threshold scale

Useful for uneven thresholds.

```yaml
discharge_scale:
  mode: threshold
  thresholds:
    - 0.5
    - 1.5
    - 3
    - 5
```

Values up to the first threshold fill one bucket, values above the last threshold fill 100%.

## Color stops

Default SOC colors:

```yaml
color_stops:
  - value: 0
    color: "#d12815"
  - value: 20
    color: "#f09d0e"
  - value: 40
    color: "#f0b40e"
  - value: 60
    color: "#cbd419"
  - value: 80
    color: "#24b548"
  - value: 100
    color: "#192cd4"
```

The card uses the highest stop whose `value` is less than or equal to the current SOC.

## Full example

```yaml
type: custom:battery-card
label: Hausakku
batterysoc: sensor.solaredge_battery_state_of_charge
charging: sensor.solaredge_battery_charge_power
discharging: sensor.solaredge_battery_discharge_power
charge_scale:
  min: 0
  max: 5
  mode: linear
discharge_scale:
  min: 0
  max: 5
  mode: linear
bar_width: 14
min_height: 100
color_stops:
  - value: 0
    color: "#d12815"
  - value: 20
    color: "#f09d0e"
  - value: 50
    color: "#cbd419"
  - value: 80
    color: "#24b548"
  - value: 100
    color: "#192cd4"
```

## Notes

- `charging` and `discharging` can be omitted if you only want the SOC display.
- If your sensor uses watts instead of kilowatts, set `max` accordingly, for example `max: 5000`.
- For very small dashboard cells, leave `icon_size` and `value_size` unset so the card can scale automatically.

## License

MIT License - see the repository [LICENSE](../../LICENSE).
