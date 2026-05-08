class BatteryCard extends HTMLElement {
  static DEFAULT_COLOR_STOPS = [
    { value: 0, color: "#d12815" },
    { value: 20, color: "#f09d0e" },
    { value: 40, color: "#f0b40e" },
    { value: 60, color: "#cbd419" },
    { value: 80, color: "#24b548" },
    { value: 100, color: "#192cd4" },
  ];

  static DEFAULT_POWER_SCALE = {
    min: 0,
    max: 4,
    steps: 4,
    mode: "linear",
  };

  setConfig(config) {
    if (!config.batterysoc) {
      throw new Error("You need to define batterysoc");
    }

    this.config = {
      label: "",
      charging: undefined,
      discharging: undefined,
      charge_scale: {},
      discharge_scale: {},
      color_stops: BatteryCard.DEFAULT_COLOR_STOPS,
      min_height: 90,
      icon_size: undefined,
      value_size: undefined,
      bar_width: 15,
      show_zero_bars: false,
      ...config,
    };

    this._chargeScale = this._normalizeScale(this.config.charge_scale);
    this._dischargeScale = this._normalizeScale(this.config.discharge_scale);
    this._colorStops = this._normalizeColorStops(this.config.color_stops);
    this._renderBase();
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._root) {
      this._renderBase();
    }
    this._update();
  }

  _renderBase() {
    if (!this.config || this._root) return;

    this.innerHTML = `
      <ha-card class="battery-card">
        <div class="battery-card__label"></div>
        <div class="battery-card__body">
          <div class="battery-card__bar battery-card__bar--charge" title="Charging">
            <div class="battery-card__bar-fill"></div>
          </div>
          <ha-icon class="battery-card__icon" icon="mdi:battery-unknown"></ha-icon>
          <div class="battery-card__bar battery-card__bar--discharge" title="Discharging">
            <div class="battery-card__bar-fill"></div>
          </div>
          <div class="battery-card__value"></div>
        </div>
      </ha-card>
    `;

    const card = this.querySelector("ha-card");
    card.style.setProperty("--battery-card-min-height", `${Number(this.config.min_height) || 90}px`);
    card.style.setProperty("--battery-card-bar-width", `${Number(this.config.bar_width) || 15}px`);
    if (this.config.icon_size) card.style.setProperty("--battery-card-icon-size", `${Number(this.config.icon_size)}px`);
    if (this.config.value_size) card.style.setProperty("--battery-card-value-size", `${Number(this.config.value_size)}px`);

    const style = document.createElement("style");
    style.textContent = `
      .battery-card {
        height: 100%;
        min-height: var(--battery-card-min-height);
        padding: 10px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: clamp(4px, 1.5cqh, 10px);
      }
      .battery-card__label {
        text-align: center;
        font-size: clamp(0.75rem, 1.7cqh, 1rem);
        line-height: 1.15;
        font-weight: var(--tile-info-primary-font-weight, 500);
        color: var(--tile-info-primary-color, var(--primary-text-color));
        min-height: 1em;
      }
      .battery-card__body {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: var(--battery-card-bar-width) auto var(--battery-card-bar-width) minmax(2.2em, auto);
        align-items: center;
        justify-content: center;
        gap: clamp(6px, 2.5cqw, 16px);
        container-type: size;
      }
      .battery-card__bar {
        width: var(--battery-card-bar-width);
        height: min(80%, 78px);
        min-height: 34px;
        position: relative;
        overflow: hidden;
        border-radius: 999px;
        background: var(--battery-card-bar-background, #353242);
      }
      .battery-card__bar-fill {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 0%;
        border-radius: 999px;
        transition: height 250ms ease, opacity 250ms ease;
      }
      .battery-card__bar--charge .battery-card__bar-fill {
        background: var(--battery-card-charge-color, #26a62a);
      }
      .battery-card__bar--discharge .battery-card__bar-fill {
        background: var(--battery-card-discharge-color, #bd20ad);
      }
      .battery-card__icon {
        --mdc-icon-size: var(--battery-card-icon-size, clamp(48px, 65cqh, 86px));
        color: var(--primary-text-color);
      }
      .battery-card__value {
        text-align: center;
        white-space: nowrap;
        font-size: var(--battery-card-value-size, clamp(1.7rem, 36cqh, 3rem));
        line-height: 1;
        font-weight: var(--tile-info-primary-font-weight, 600);
        color: var(--tile-info-primary-color, var(--primary-text-color));
      }
    `;
    card.appendChild(style);

    this._root = card;
    this._label = this.querySelector(".battery-card__label");
    this._icon = this.querySelector(".battery-card__icon");
    this._value = this.querySelector(".battery-card__value");
    this._chargeBar = this.querySelector(".battery-card__bar--charge .battery-card__bar-fill");
    this._dischargeBar = this.querySelector(".battery-card__bar--discharge .battery-card__bar-fill");
    this._label.textContent = this.config.label || "";
  }

  _update() {
    const socState = this._getState(this.config.batterysoc);
    const soc = this._number(socState?.state);

    if (soc === undefined) {
      this._value.textContent = "—";
      this._icon.setAttribute("icon", "mdi:battery-unknown");
      this._icon.style.color = "var(--disabled-text-color)";
    } else {
      const clampedSoc = this._clamp(soc, 0, 100);
      this._value.textContent = `${Math.round(clampedSoc)}%`;
      this._icon.setAttribute("icon", this._batteryIcon(clampedSoc));
      this._icon.style.color = this._computeColor(clampedSoc);
    }

    this._setBar(this._chargeBar, this.config.charging, this._chargeScale);
    this._setBar(this._dischargeBar, this.config.discharging, this._dischargeScale);
  }

  _setBar(element, entityId, scale) {
    const value = this._number(this._getState(entityId)?.state);
    const percent = this._scaleValue(value, scale);
    element.style.height = `${percent}%`;
    element.style.opacity = percent > 0 || this.config.show_zero_bars ? "1" : "0";
  }

  _getState(entityId) {
    if (!entityId || !this._hass?.states) return undefined;
    return this._hass.states[entityId];
  }

  _number(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : undefined;
  }

  _normalizeScale(scale = {}) {
    return {
      ...BatteryCard.DEFAULT_POWER_SCALE,
      ...scale,
      min: this._number(scale.min) ?? BatteryCard.DEFAULT_POWER_SCALE.min,
      max: this._number(scale.max) ?? BatteryCard.DEFAULT_POWER_SCALE.max,
      steps: this._number(scale.steps) ?? BatteryCard.DEFAULT_POWER_SCALE.steps,
      thresholds: Array.isArray(scale.thresholds)
        ? scale.thresholds.map(Number).filter(Number.isFinite).sort((a, b) => a - b)
        : undefined,
    };
  }

  _scaleValue(value, scale) {
    if (value === undefined || value <= scale.min) return 0;

    if (scale.mode === "threshold" && scale.thresholds?.length) {
      const index = scale.thresholds.findIndex((threshold) => value <= threshold);
      const bucket = index === -1 ? scale.thresholds.length : index + 1;
      return this._clamp((bucket / scale.thresholds.length) * 100, 0, 100);
    }

    const max = Math.max(scale.max, scale.min + 0.000001);
    const percent = ((value - scale.min) / (max - scale.min)) * 100;

    if (scale.mode === "steps" && scale.steps > 0) {
      return this._clamp(Math.ceil(percent / (100 / scale.steps)) * (100 / scale.steps), 0, 100);
    }

    return this._clamp(percent, 0, 100);
  }

  _normalizeColorStops(stops) {
    const source = Array.isArray(stops) ? stops : BatteryCard.DEFAULT_COLOR_STOPS;
    return source
      .map((stop) => ({ value: Number(stop.value), color: stop.color }))
      .filter((stop) => Number.isFinite(stop.value) && stop.color)
      .sort((a, b) => a.value - b.value);
  }

  _computeColor(soc) {
    let color = this._colorStops[0]?.color || "var(--primary-text-color)";
    for (const stop of this._colorStops) {
      if (soc >= stop.value) color = stop.color;
    }
    return color;
  }

  _batteryIcon(soc) {
    if (soc <= 5) return "mdi:battery-outline";
    if (soc >= 100) return "mdi:battery";
    return `mdi:battery-${Math.min(90, Math.max(10, Math.floor(soc / 10) * 10))}`;
  }

  _clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  getGridOptions() {
    return {
      columns: 8,
      rows: 2,
      min_columns: 4,
      min_rows: 1,
    };
  }

  static getConfigForm() {
    return {
      schema: [
        { name: "label", selector: { text: {} } },
        { name: "batterysoc", required: true, selector: { entity: { domain: "sensor" } } },
        { name: "charging", selector: { entity: { domain: "sensor" } } },
        { name: "discharging", selector: { entity: { domain: "sensor" } } },
        { name: "charge_scale", selector: { object: {} } },
        { name: "discharge_scale", selector: { object: {} } },
        { name: "color_stops", selector: { object: {} } },
        { name: "min_height", selector: { number: { min: 70, max: 220, mode: "box", unit_of_measurement: "px" } } },
        { name: "bar_width", selector: { number: { min: 6, max: 40, mode: "box", unit_of_measurement: "px" } } },
        { name: "icon_size", selector: { number: { min: 32, max: 140, mode: "box", unit_of_measurement: "px" } } },
        { name: "value_size", selector: { number: { min: 18, max: 80, mode: "box", unit_of_measurement: "px" } } },
        { name: "show_zero_bars", selector: { boolean: {} } },
      ],
      computeLabel: (schema) => ({
        label: "Label",
        batterysoc: "Battery SOC entity",
        charging: "Charging entity",
        discharging: "Discharging entity",
        charge_scale: "Charging scale",
        discharge_scale: "Discharging scale",
        color_stops: "SOC color stops",
        min_height: "Minimum height",
        bar_width: "Bar width",
        icon_size: "Icon size",
        value_size: "Value text size",
        show_zero_bars: "Show zero bars",
      }[schema.name] || schema.name),
      computeHelper: (schema) => ({
        label: "Optional heading shown above the battery.",
        batterysoc: "Battery state-of-charge entity in percent.",
        charging: "Optional charging power/current entity used for the left bar.",
        discharging: "Optional discharging power/current entity used for the right bar.",
        charge_scale: "Scaling for charging bar, e.g. {min: 0, max: 5, mode: 'linear'} or mode 'steps'.",
        discharge_scale: "Scaling for discharging bar, e.g. {min: 0, max: 5, mode: 'linear'} or mode 'threshold'.",
        color_stops: "Optional SOC colors as [{value: 0, color: '#d12815'}, ...].",
        min_height: "Minimum card height used for responsive scaling.",
        bar_width: "Width of the charging/discharging bars.",
        icon_size: "Optional fixed icon size. Leave empty for responsive sizing.",
        value_size: "Optional fixed percentage text size. Leave empty for responsive sizing.",
        show_zero_bars: "Keep empty bars visible even when the value is zero.",
      }[schema.name] || ""),
    };
  }
}

if (!customElements.get("battery-card")) {
  customElements.define("battery-card", BatteryCard);
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: "battery-card",
  name: "Battery Card",
  description: "Battery SOC card with configurable charging/discharging bars.",
  preview: true,
});
