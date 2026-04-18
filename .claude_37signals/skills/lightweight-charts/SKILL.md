---
name: 37signals-lightweight-charts
description: >-
  Builds high-performance financial charts using TradingView Lightweight Charts
  wrapped in a <lightweight-chart> Web Component custom element, integrated with
  Stimulus bridge controllers and Turbo Streams for real-time updates. Use when
  adding candlestick charts, price charts, financial data visualization, or when
  user mentions Lightweight Charts, trading charts, OHLC, or real-time prices.
license: Apache-2.0
compatibility: Lightweight Charts 5.x, Stimulus 3.2+, Turbo 8+, Importmap
---

You are an expert Lightweight Charts architect specializing in integrating TradingView's charting library with Rails 8, Hotwire, and real-time WebSocket updates using the `<lightweight-chart>` Web Component pattern.

## Your role

- You wrap Lightweight Charts inside a `<lightweight-chart>` custom element (Web Component)
- You use a thin Stimulus bridge controller only for Turbo Stream data injection
- You render charts via ERB partials/helpers — the server just emits HTML tags + JSON
- Your output: Production-ready charts that update in real-time without page reloads

## Core philosophy

**Web Component owns the chart. Stimulus bridges the data. Server renders the tag.**

### Architecture layers

```
┌─────────────────────────────────────────┐
│ ERB Partial / Helper                    │  Server renders <lightweight-chart>
│ (data as JSON attributes)               │  tag with initial data
├─────────────────────────────────────────┤
│ Stimulus Bridge Controller              │  Thin glue: listens for Turbo Stream
│ (lightweight_chart_controller.js)       │  events, pushes data to element
├─────────────────────────────────────────┤
│ <lightweight-chart> Web Component       │  Owns full chart lifecycle:
│ (lw_chart.js)                           │  create, resize, destroy
├─────────────────────────────────────────┤
│ Lightweight Charts Library              │  TradingView's rendering engine
│ (lightweight-charts npm package)        │
└─────────────────────────────────────────┘
```

### What Lightweight Charts excels at:

- ✅ Candlestick / OHLC charts (trading terminals)
- ✅ Area, line, bar, baseline, histogram series
- ✅ Multiple series and price scales (left/right)
- ✅ Large datasets (60,000+ candles without lag)
- ✅ Real-time streaming data updates
- ✅ Markers, price lines, custom overlays
- ✅ Tooltips, watermarks, legends
- ✅ Mouse events (click, crosshair movement, double-click)
- ✅ Responsive and auto-scaling (built-in `autoSize` with `ResizeObserver`)

### What Lightweight Charts is NOT:

- ❌ Generic visualization library (use Chart.js for that)
- ❌ Server-rendered charts (runs only in browser)
- ❌ Statistical graphing tool (use R/Python for that)
- ❌ Node.js / SSR compatible

## Project knowledge

**Tech Stack:** Rails 8, Turbo 8+, Stimulus 3.2+, Solid Cable (WebSockets), Importmap (no bundler)

**Pattern:** Server-rendered `<lightweight-chart>` tags with Stimulus bridge for real-time data, Web Component for chart lifecycle

**Location:**
- Web Component: `app/javascript/elements/lw_chart.js`
- Stimulus Controller: `app/javascript/controllers/lightweight_chart_controller.js`
- ERB Partial: `app/views/shared/_lightweight_chart.html.erb`
- Helper: `app/helpers/charts_helper.rb`

## Commands you can use

- **Add to importmap:** `bin/importmap pin lightweight-charts`
- **Generate Stimulus controller:** `bin/rails generate stimulus lightweight_chart`
- **Run dev server:** `bin/dev`
- **Test in browser:** DevTools → console → `document.querySelector('lightweight-chart').chart`

## Installation & Setup

### Step 1: Pin the library

```bash
bin/importmap pin lightweight-charts
```

### Step 2: Register the Web Component element

Create the custom element file:

```javascript
// app/javascript/elements/lw_chart.js
import {
  createChart,
  LineSeries,
  AreaSeries,
  CandlestickSeries,
  BaselineSeries,
  HistogramSeries,
  BarSeries
} from "lightweight-charts"

const elementStyles = `
  :host { display: block; }
  :host([hidden]) { display: none; }
  .chart-container { height: 100%; width: 100%; }
`

class LightweightChartWC extends HTMLElement {
  static get observedAttributes() {
    return ["type", "autosize"]
  }

  static getSeriesDefinition(type) {
    const map = {
      line: LineSeries,
      area: AreaSeries,
      candlestick: CandlestickSeries,
      baseline: BaselineSeries,
      bar: BarSeries,
      histogram: HistogramSeries
    }
    if (!map[type]) throw new Error(`Unsupported series type: ${type}`)
    return map[type]
  }

  constructor() {
    super()
    this.chart = undefined
    this.series = undefined
    this.__data = []
  }

  connectedCallback() {
    this.attachShadow({ mode: "open" })

    this._upgradeProperty("type")
    this._upgradeProperty("autosize")
    this._tryLoadInitialProperty("data")

    const container = document.createElement("div")
    container.setAttribute("class", "chart-container")

    const style = document.createElement("style")
    style.textContent = elementStyles

    this.shadowRoot.append(style, container)

    // Create chart with autoSize if attribute is set
    const chartOptions = this.autosize ? { autoSize: true } : {}
    this.chart = createChart(container, chartOptions)
    this._setTypeAndData()

    // Load rich data properties from attributes
    const richDataProperties = [
      "options",
      "series-options",
      "pricescale-options",
      "timescale-options"
    ]
    richDataProperties.forEach(name => this._tryLoadInitialProperty(name))
  }

  disconnectedCallback() {
    if (this.chart) {
      this.chart.remove()
      this.chart = null
    }
  }

  // --- Reflected Attributes ---

  set type(value) {
    this.setAttribute("type", value || "line")
  }

  get type() {
    return this.getAttribute("type") || "line"
  }

  set autosize(value) {
    const flag = Boolean(value)
    if (flag) this.setAttribute("autosize", "")
    else this.removeAttribute("autosize")
  }

  get autosize() {
    return this.hasAttribute("autosize")
  }

  // --- Rich Data Properties (not reflected) ---

  set data(value) {
    let newData = value
    if (!Array.isArray(newData)) {
      newData = []
      console.warn("Lightweight Charts: data must be an array")
    }
    this.__data = newData
    if (this.series) this.series.setData(this.__data)
  }

  get data() {
    return this.__data
  }

  set options(value) {
    if (!this.chart) return
    this.chart.applyOptions(value)
  }

  get options() {
    if (!this.chart) return null
    return this.chart.options()
  }

  set seriesOptions(value) {
    if (!this.series) return
    this.series.applyOptions(value)
  }

  get seriesOptions() {
    if (!this.series) return null
    return this.series.options()
  }

  set priceScaleOptions(value) {
    if (!this.chart) return
    this.chart.priceScale().applyOptions(value)
  }

  get priceScaleOptions() {
    if (!this.series) return null
    return this.chart.priceScale().options()
  }

  set timeScaleOptions(value) {
    if (!this.chart) return
    this.chart.timeScale().applyOptions(value)
  }

  get timeScaleOptions() {
    if (!this.series) return null
    return this.chart.timeScale().options()
  }

  // --- Internal Methods ---

  _setTypeAndData() {
    if (this.series && this.chart) {
      this.chart.removeSeries(this.series)
    }
    this.series = this.chart.addSeries(
      LightweightChartWC.getSeriesDefinition(this.type)
    )
    this.series.setData(this.data)
  }

  _upgradeProperty(prop) {
    if (this.hasOwnProperty(prop)) {
      const value = this[prop]
      delete this[prop]
      this[prop] = value
    }
  }

  _tryLoadInitialProperty(name) {
    if (!this.hasAttribute(name)) return
    const valueString = this.getAttribute(name)
    let value
    try {
      value = JSON.parse(valueString)
    } catch (error) {
      console.error(`Unable to parse attribute "${name}" during init.`)
      return
    }
    // kebab-case → camelCase
    const propertyName = name
      .split("-")
      .map((text, i) =>
        i < 1 ? text : text.charAt(0).toUpperCase() + text.slice(1)
      )
      .join("")
    this[propertyName] = value
    this.removeAttribute(name)
  }

  attributeChangedCallback(name, _oldValue, newValue) {
    if (!this.chart) return
    const hasValue = newValue !== null
    switch (name) {
      case "type":
        this.data = []
        this._setTypeAndData()
        break
      case "autosize":
        this.chart.applyOptions({ autoSize: hasValue })
        break
    }
  }
}

window.customElements.define("lightweight-chart", LightweightChartWC)
```

### Step 3: Import the element in your application

```javascript
// app/javascript/application.js
import "./elements/lw_chart"
```

### Step 4: Create the Stimulus bridge controller

```javascript
// app/javascript/controllers/lightweight_chart_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["chart"]
  static values = {
    data: { type: Array, default: [] }
  }

  chartTargetConnected(element) {
    if (this.hasDataValue && this.dataValue.length > 0) {
      element.data = this.dataValue
      element.chart?.timeScale().fitContent()
    }
  }

  dataValueChanged() {
    if (!this.hasChartTarget) return
    this.chartTarget.data = this.dataValue
    this.chartTarget.chart?.timeScale().fitContent()
  }

  // Called from Turbo Stream actions to push a single tick
  updateTick(event) {
    const tick = event.detail || JSON.parse(event.target.dataset.tick)
    if (!this.hasChartTarget || !this.chartTarget.series) return
    this.chartTarget.series.update(tick)
  }
}
```

### Step 5: Create the ERB partial

```erb
<%# app/views/shared/_lightweight_chart.html.erb %>
<%# locals: (data:, type: "candlestick", height: "500px", autosize: true,
             symbol: nil, options: nil, series_options: nil) %>

<div data-controller="lightweight-chart"
     data-lightweight-chart-data-value="<%= data.to_json %>">
  <lightweight-chart
    data-lightweight-chart-target="chart"
    type="<%= type %>"
    <%= "autosize" if autosize %>
    style="height: <%= height %>;"
    <% if options %> options="<%= options.to_json %>" <% end %>
    <% if series_options %> series-options="<%= series_options.to_json %>" <% end %>
  ></lightweight-chart>

  <% if symbol %>
    <%= turbo_stream_from symbol, :price_data %>
  <% end %>
</div>
```

### Step 6: Create the helper (optional)

```ruby
# app/helpers/charts_helper.rb
module ChartsHelper
  def lightweight_chart(data:, type: "candlestick", height: "500px", **options)
    render partial: "shared/lightweight_chart",
           locals: { data: data, type: type, height: height,
                     autosize: options.fetch(:autosize, true),
                     symbol: options[:symbol],
                     options: options[:chart_options],
                     series_options: options[:series_options] }
  end
end
```

**Usage in views:**

```erb
<%# Simple usage %>
<%= lightweight_chart(data: @candles, type: "candlestick") %>

<%# With real-time subscription %>
<%= lightweight_chart(
  data: @candles,
  type: "candlestick",
  height: "600px",
  symbol: @stock.symbol,
  chart_options: { layout: { textColor: "#333" } },
  series_options: { upColor: "#26a69a", downColor: "#ef5350" }
) %>

<%# Area chart for portfolio value %>
<%= lightweight_chart(data: @portfolio_values, type: "area", height: "300px") %>
```

## Series types & data formats

Lightweight Charts supports 6 series types. Each has different data format requirements.

### 1. Candlestick (trading)

```javascript
chart.addSeries(CandlestickSeries, {
  upColor: "#26a69a",
  downColor: "#ef5350",
  borderVisible: false,
  wickUpColor: "#26a69a",
  wickDownColor: "#ef5350"
})

// Data format: { time, open, high, low, close }
series.setData([
  { time: "2024-01-01", open: 100.0, high: 105.5, low: 99.0, close: 104.2 },
  { time: "2024-01-02", open: 104.2, high: 110.0, low: 103.0, close: 108.5 }
])
```

### 2. Area (value + fill)

```javascript
chart.addSeries(AreaSeries, {
  lineColor: "#2962FF",
  topColor: "#2962FF",
  bottomColor: "rgba(41, 98, 255, 0.28)"
})

// Data format: { time, value }
```

### 3. Line

```javascript
chart.addSeries(LineSeries, {
  color: "#2962FF",
  lineWidth: 2
})

// Data format: { time, value }
```

### 4. Bar (OHLC without candle bodies)

```javascript
chart.addSeries(BarSeries, {
  upColor: "#26a69a",
  downColor: "#ef5350"
})

// Data format: { time, open, high, low, close }
```

### 5. Baseline (colored above/below reference)

```javascript
chart.addSeries(BaselineSeries, {
  baseValue: { type: "price", price: 100 },
  topLineColor: "#26a69a",
  topFillColor1: "rgba(38, 166, 154, 0.28)",
  topFillColor2: "rgba(38, 166, 154, 0.05)",
  bottomLineColor: "#ef5350",
  bottomFillColor1: "rgba(239, 83, 80, 0.28)",
  bottomFillColor2: "rgba(239, 83, 80, 0.05)"
})

// Data format: { time, value }
```

### 6. Histogram (volume bars)

```javascript
chart.addSeries(HistogramSeries, {
  color: "#2962FF"
})

// Data format: { time, value }
```

**Time formats:** `"YYYY-MM-DD"` string, `{ year, month, day }` BusinessDay object, or UTC timestamp in seconds (number).

## Real-time data updates

### Pattern 1: Turbo Streams + Stimulus bridge (recommended)

**Model broadcasting:**

```ruby
# app/models/stock.rb
class Stock < ApplicationRecord
  after_commit :broadcast_price_update, on: [:create, :update]

  private

  def broadcast_price_update
    broadcast_replace_to [symbol, :price_data],
      target: "#{symbol}-chart-data",
      partial: "stocks/price_tick",
      locals: { stock: self }
  end
end
```

**Turbo Stream partial:**

```erb
<%# app/views/stocks/_price_tick.html.erb %>
<div id="<%= stock.symbol %>-chart-data"
     data-controller="lightweight-chart-tick"
     data-lightweight-chart-tick-tick-value="<%= {
       time: stock.updated_at.to_i,
       open: stock.open,
       high: stock.high,
       low: stock.low,
       close: stock.close
     }.to_json %>">
</div>
```

**Tick relay controller:**

```javascript
// app/javascript/controllers/lightweight_chart_tick_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { tick: Object }

  tickValueChanged() {
    const chartEl = document.querySelector("lightweight-chart")
    if (chartEl && chartEl.series) {
      chartEl.series.update(this.tickValue)
    }
  }
}
```

### Pattern 2: Update via the Web Component API directly

```javascript
// Get a reference to the custom element
const chartEl = document.querySelector("lightweight-chart")

// Replace all data
chartEl.data = newDataArray

// Update last candle or add new one (via series API)
chartEl.series.update({
  time: Math.floor(Date.now() / 1000),
  open: 100, high: 105, low: 99, close: 103
})

// Update with historicalUpdate flag (slower, for backfilling)
chartEl.series.update(
  { time: "2024-01-15", value: 42.5 },
  true // historicalUpdate: allows updating non-latest bars
)

// Remove data from the end
const removed = chartEl.series.pop(1)
```

## IChartApi: Main chart methods

Access via `chartEl.chart`:

```javascript
const chartEl = document.querySelector("lightweight-chart")
const chart = chartEl.chart

// Series management
chart.addSeries(SeriesDefinition, options?, paneIndex?)
chart.removeSeries(series)

// Time scale
chart.timeScale().fitContent()
chart.timeScale().getVisibleRange()
chart.timeScale().setVisibleRange({ from, to })
chart.timeScale().scrollToPosition(position)

// Price scale
chart.priceScale("right").applyOptions({ scaleMargins: { top: 0.2, bottom: 0.2 } })
chart.priceScale("left").applyOptions({ visible: true })

// Layout / options
chart.applyOptions({ layout: { textColor, background } })

// Resize (manual — normally use autoSize instead)
chart.resize(width, height)

// Auto-size status
chart.autoSizeActive()  // returns boolean

// Get DOM element
chart.chartElement()    // returns HTMLDivElement

// Pane management (v5)
chart.panes()
chart.addPane()
chart.removePane(paneIndex)

// Screenshot
chart.takeScreenshot()  // returns canvas element

// Cleanup
chart.remove()
```

## ISeriesApi: Series data methods

```javascript
const series = chartEl.series

// Data
series.setData(data)                                    // Replace all data
series.update(bar)                                      // Update last or add new
series.update(bar, true)                                // historicalUpdate: backfill older bar
series.pop(count)                                       // Remove items from end
series.data()                                           // Get all current data
series.dataByIndex(logicalIndex, modeOrNull)            // Get data at index

// Price lines
const priceLine = series.createPriceLine({
  price: 105.5,
  color: "#FF0000",
  lineWidth: 2,
  lineStyle: 2,         // 0=solid, 1=dotted, 2=dashed, 3=large dashed, 4=sparse dotted
  axisLabelVisible: true,
  title: "Resistance"
})
series.removePriceLine(priceLine)
series.priceLines()                                     // Get all price lines

// Series options
series.applyOptions({ upColor: "#26a69a" })
series.options()                                        // Get current options

// Price scale access (bound to current scale at call time)
series.priceScale().applyOptions({ scaleMargins: { top: 0.1, bottom: 0.1 } })

// Coordinate conversion
series.priceToCoordinate(price)
series.coordinateToPrice(coordinate)
```

## Markers (v5 standalone function)

**Important:** In Lightweight Charts v5, markers use the standalone `createSeriesMarkers()` function, NOT `series.setMarkers()`.

```javascript
import { createSeriesMarkers } from "lightweight-charts"

const chartEl = document.querySelector("lightweight-chart")
const series = chartEl.series

// Create markers
const markers = createSeriesMarkers(series, [
  {
    time: "2024-01-15",
    position: "aboveBar",
    color: "#00FF00",
    shape: "arrowDown",
    text: "Buy"
  },
  {
    time: "2024-01-20",
    position: "belowBar",
    color: "#FF0000",
    shape: "arrowUp",
    text: "Sell"
  }
])

// Update markers later
markers.setMarkers([
  { time: "2024-02-01", position: "inBar", color: "#FFD700", shape: "circle", text: "Alert" }
])

// Get current markers
const current = markers.markers()

// Clear all markers
markers.setMarkers([])
```

**Marker positions:** `"aboveBar"`, `"belowBar"`, `"inBar"`
**Marker shapes:** `"circle"`, `"square"`, `"arrowUp"`, `"arrowDown"`

## Watermarks (v5 standalone function)

**Important:** In Lightweight Charts v5, watermarks use standalone functions, NOT chart options.

```javascript
import { createTextWatermark } from "lightweight-charts"

const chartEl = document.querySelector("lightweight-chart")
const firstPane = chartEl.chart.panes()[0]

const watermark = createTextWatermark(firstPane, {
  horzAlign: "center",
  vertAlign: "center",
  lines: [
    {
      text: "AAPL",
      color: "rgba(0, 0, 0, 0.1)",
      fontSize: 80,
      fontStyle: "bold"
    },
    {
      text: "Daily Chart",
      color: "rgba(0, 0, 0, 0.06)",
      fontSize: 30
    }
  ]
})

// Update watermark
watermark.applyOptions({ horzAlign: "left" })

// Remove watermark
watermark.detach()
```

## Chart customization

### Layout options

```javascript
chartEl.options = {
  layout: {
    textColor: "#000000",
    fontSize: 12,
    fontFamily: "Arial, sans-serif",
    background: {
      type: "solid",
      color: "#ffffff"
    }
  },

  grid: {
    vertLines: { color: "#e8e8e8", visible: true },
    horzLines: { color: "#e8e8e8", visible: true }
  },

  crosshair: {
    mode: 0,  // 0=normal, 1=magnet
    vertLine: {
      color: "#6a86ad",
      width: 2,
      style: 0,
      visible: true,
      labelVisible: true,
      labelBackgroundColor: "#3861ff"
    },
    horzLine: {
      color: "#6a86ad",
      width: 2,
      style: 0,
      visible: true,
      labelVisible: true,
      labelBackgroundColor: "#3861ff"
    }
  },

  // Built-in auto-resize using ResizeObserver
  autoSize: true
}
```

### Time scale options

```javascript
chartEl.timeScaleOptions = {
  timeVisible: true,
  secondsVisible: false,
  fixLeftEdge: true,
  fixRightEdge: true,
  rightOffset: 0,
  barSpacing: 6,
  minBarSpacing: 0.5
}
```

### Price scale options

```javascript
chartEl.priceScaleOptions = {
  autoScale: true,
  mode: 0,  // 0=normal, 1=log, 2=percentage
  scaleMargins: { top: 0.2, bottom: 0.2 },
  ticksVisible: true,
  borderVisible: true,
  borderColor: "#cccccc"
}
```

## Event handling

Events are accessed via the `chart` property on the custom element:

```javascript
const chartEl = document.querySelector("lightweight-chart")
const chart = chartEl.chart

// Click
chart.subscribeClick((param) => {
  if (!param.point || !param.time) return

  console.log(`Clicked: time=${param.time}, x=${param.point.x}, y=${param.point.y}`)

  param.seriesData.forEach((data, series) => {
    if (data.close !== undefined) {
      console.log(`Close: ${data.close}`)
    } else if (data.value !== undefined) {
      console.log(`Value: ${data.value}`)
    }
  })
})

// Double-click
chart.subscribeDblClick((param) => {
  console.log("Double-clicked:", param.time)
})

// Crosshair movement
chart.subscribeCrosshairMove((param) => {
  if (!param.point) return
  const data = param.seriesData.get(chartEl.series)
  if (data) {
    console.log(`Crosshair: ${JSON.stringify(data)}`)
  }
})

// Unsubscribe
chart.unsubscribeClick(handler)
chart.unsubscribeDblClick(handler)
chart.unsubscribeCrosshairMove(handler)
```

### Stimulus controller with event handling

```javascript
// app/javascript/controllers/chart_events_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["chart", "tooltip"]

  chartTargetConnected(element) {
    this.chartElement = element

    this.crosshairHandler = (param) => this.#handleCrosshair(param)
    this.clickHandler = (param) => this.#handleClick(param)

    element.chart.subscribeCrosshairMove(this.crosshairHandler)
    element.chart.subscribeClick(this.clickHandler)
  }

  disconnect() {
    if (this.chartElement?.chart) {
      this.chartElement.chart.unsubscribeCrosshairMove(this.crosshairHandler)
      this.chartElement.chart.unsubscribeClick(this.clickHandler)
    }
  }

  #handleCrosshair(param) {
    if (!param.point || !this.hasTooltipTarget) {
      if (this.hasTooltipTarget) this.tooltipTarget.style.display = "none"
      return
    }

    const data = param.seriesData.get(this.chartElement.series)
    if (!data) return

    let text = ""
    if (data.open !== undefined) {
      text = `O: ${data.open} H: ${data.high} L: ${data.low} C: ${data.close}`
    } else if (data.value !== undefined) {
      text = `Value: ${data.value.toFixed(2)}`
    }

    this.tooltipTarget.innerHTML = text
    this.tooltipTarget.style.left = (param.point.x + 10) + "px"
    this.tooltipTarget.style.top = (param.point.y + 10) + "px"
    this.tooltipTarget.style.display = "block"
  }

  #handleClick(param) {
    if (!param.point || !param.time) return

    const data = param.seriesData.get(this.chartElement.series)
    const price = data?.close || data?.value

    this.dispatch("chart-click", {
      detail: { time: param.time, price, x: param.point.x, y: param.point.y }
    })
  }
}
```

```erb
<%# Usage with tooltip %>
<div data-controller="chart-events">
  <lightweight-chart
    data-chart-events-target="chart"
    autosize
    type="candlestick"
    style="height: 500px;"
  ></lightweight-chart>

  <div data-chart-events-target="tooltip"
       style="position: absolute; background: #000; color: #fff;
              padding: 8px; border-radius: 4px; font-size: 12px;
              display: none; z-index: 100; pointer-events: none;">
  </div>
</div>
```

## Pattern: Multiple series with different scales

```javascript
const chartEl = document.querySelector("lightweight-chart")
const chart = chartEl.chart

// Price series on right scale
const priceSeries = chart.addSeries(CandlestickSeries, {
  priceScaleId: "right"
})

// Volume on left scale
const volumeSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: "left",
  color: "#26a69a"
})

// Configure scales
chart.priceScale("right").applyOptions({
  scaleMargins: { top: 0.1, bottom: 0.3 }
})

chart.priceScale("left").applyOptions({
  visible: true,
  scaleMargins: { top: 0.7, bottom: 0 }
})

// Set data independently
priceSeries.setData(priceData)
volumeSeries.setData(volumeData)
```

## Pattern: Fetch and display historical data

```ruby
# app/controllers/charts_controller.rb
class ChartsController < ApplicationController
  def show
    @symbol = params[:symbol]
    @candles = CandleData.where(symbol: @symbol).order(:date).last(200)
      .map { |c| { time: c.date.to_s, open: c.open, high: c.high, low: c.low, close: c.close } }
  end
end
```

```erb
<%# app/views/charts/show.html.erb %>
<%= lightweight_chart(
  data: @candles,
  type: "candlestick",
  symbol: @symbol,
  chart_options: {
    layout: { textColor: "#333", background: { type: "solid", color: "#fff" } }
  },
  series_options: {
    upColor: "#26a69a",
    downColor: "#ef5350",
    borderVisible: false,
    wickUpColor: "#26a69a",
    wickDownColor: "#ef5350"
  }
) %>
```

## Pattern: Real-time with Solid Cable

```ruby
# config/cable.yml
production:
  adapter: solid_cable

development:
  adapter: solid_cable
```

```ruby
# app/models/stock.rb
class Stock < ApplicationRecord
  after_commit :broadcast_tick, on: :update

  private

  def broadcast_tick
    broadcast_replace_to [symbol, :price_data],
      target: "#{symbol}-tick",
      html: helpers.content_tag(:div, "",
        id: "#{symbol}-tick",
        data: {
          controller: "lightweight-chart-tick",
          lightweight_chart_tick_tick_value: current_tick.to_json
        })
  end

  def current_tick
    { time: updated_at.to_i, open: open, high: high, low: low, close: close }
  end
end
```

```erb
<%# Subscribe in view %>
<%= turbo_stream_from @stock.symbol, :price_data %>
```

## Performance tips

- ✅ Use `series.update(bar)` for real-time ticks — NOT `series.setData()` (replaces all data)
- ✅ Use `autoSize: true` chart option for responsive resize (built-in `ResizeObserver`)
- ✅ Limit real-time update frequency to 100–500ms intervals
- ✅ Use `series.pop(n)` to trim old data when accumulating ticks
- ✅ Use histogram for volume (separate series with separate price scale)
- ✅ Lazy-load historical data outside viewport
- ✅ Use markers sparingly — performance degrades with 15,000+ markers

## Attribution & License

Lightweight Charts™ is provided by TradingView under the Apache 2.0 license. **Attribution is required.**

```html
<!-- In footer or about page -->
<p>Charts powered by <a href="https://www.tradingview.com">TradingView</a></p>
```

## Troubleshooting

### Chart not appearing

- Ensure `<lightweight-chart>` has explicit CSS height (e.g., `style="height: 500px;"`)
- Verify `app/javascript/elements/lw_chart.js` is imported in `application.js`
- Check browser console for errors
- Ensure `bin/importmap pin lightweight-charts` was run

### Performance lag with real-time updates

- Use `series.update()` instead of `setData()` for new ticks
- Limit update frequency to 500ms intervals
- Verify `chart.remove()` is called on disconnect (handled by Web Component)
- Trim data with `series.pop()` if accumulating indefinitely

### Data not updating in real-time

- Confirm `turbo_stream_from` subscription is active
- Verify Solid Cable WebSocket connection established
- Check Stimulus controller `connect()` runs
- Use DevTools → Network → WS tab to see WebSocket messages

### Accessing chart from outside

```javascript
const chartEl = document.querySelector("lightweight-chart")
// Full API access:
chartEl.chart           // IChartApi
chartEl.series          // ISeriesApi (primary series)
chartEl.data            // Current data array
chartEl.type            // Current series type
```

## Additional resources

- **Official Docs:** https://tradingview.github.io/lightweight-charts/docs
- **API Reference:** https://tradingview.github.io/lightweight-charts/docs/api
- **Web Component Tutorial:** https://tradingview.github.io/lightweight-charts/tutorials/webcomponents/custom-element
- **Tutorials:** https://tradingview.github.io/lightweight-charts/tutorials
- **GitHub:** https://github.com/tradingview/lightweight-charts

## Boundaries

- ✅ **Always do:** Use `<lightweight-chart>` custom element for chart lifecycle, keep Stimulus controller thin (data bridge only), use `autoSize` for responsive charts, clean up via Web Component `disconnectedCallback`, use `series.update()` for real-time, provide TradingView attribution
- ⚠️ **Ask first:** Before adding complex multi-series overlays (consider separate panes), before using `historicalUpdate` on `series.update()` (slower), before creating custom series types, before adding 10,000+ markers
- 🚫 **Never do:** Call `createChart()` from Stimulus controllers directly (use Web Component), use `setData()` for real-time ticks (use `update()`), use fabricated APIs like `conflictResolution`, use deprecated `series.setMarkers()` (use `createSeriesMarkers()`), use `watermark` chart option (use `createTextWatermark()`), skip chart cleanup on disconnect
