# Lightweight Charts Rails Integration Reference

## Stimulus Controller Setup

### Basic Chart Controller

```javascript
// app/javascript/controllers/chart_controller.js
import { Controller } from "@hotwired/stimulus"
import { createChart, CandlestickSeries, LineSeries } from "lightweight-charts"

export default class extends Controller {
  static targets = ["container"]
  static values = { symbol: String }

  connect() {
    this.initializeChart()
  }

  disconnect() {
    if (this.chart) {
      this.chart.remove() // Clean up chart instance
    }
  }

  initializeChart() {
    const container = this.containerTarget
    
    // Set container size
    container.style.width = "100%"
    container.style.height = "500px"

    // Create chart
    this.chart = createChart(container, {
      layout: {
        textColor: "#000",
        background: { type: "solid", color: "#fff" }
      },
      timeScale: { timeVisible: true, secondsVisible: false }
    })

    // Add series
    this.candlesSeries = this.chart.addSeries(CandlestickSeries, {
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderVisible: false,
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350"
    })

    // Fit content to visible area
    this.chart.timeScale().fitContent()
  }

  updateData(event) {
    const data = event.detail.candleData

    if (this.candlesSeries) {
      this.candlesSeries.setData(data)
      this.chart.timeScale().fitContent()
    }
  }
}
```

### View with Chart Container

```erb
<%# app/views/charts/show.html.erb %>

<div data-controller="chart" data-chart-symbol-value="<%= @symbol %>">
  <div data-chart-target="container"></div>
</div>

<%# Subscribe to real-time updates %>
<%= turbo_stream_from @symbol, :price_data %>
```

## Real-Time Updates

### Pattern 1: Turbo Streams (recommended for Rails)

**Model:**

```ruby
# app/models/stock.rb
class Stock < ApplicationRecord
  include Stock::Broadcastable
end

# app/models/stock/broadcastable.rb
module Stock::Broadcastable
  extend ActiveSupport::Concern

  included do
    after_commit :broadcast_price_update
  end

  private

  def broadcast_price_update
    # Broadcast new candle/tick data to chart
    broadcast_append_to self, :price_data do
      render partial: "stocks/price_update", locals: { price: self }
    end
  end
end
```

**Controller:**

```ruby
# app/controllers/stocks_controller.rb
class StocksController < ApplicationController
  def show
    @stock = Stock.find(params[:id])
  end

  # Called via Turbo Stream when new data arrives
  def update_price
    @stock = Stock.find(params[:id])
    
    respond_to do |format|
      format.turbo_stream
      format.json { render json: @stock.current_candle }
    end
  end
end
```

**View (Turbo Stream):**

```erb
<%# app/views/stocks/update_price.turbo_stream.erb %>

<%= turbo_stream.update "chart-data" do %>
  <script type="module">
    const event = new CustomEvent('update-chart', {
      detail: {
        candleData: <%= raw @stock.current_candle.to_json %>
      }
    })
    document.dispatchEvent(event)
  </script>
<% end %>
```

**Stimulus Controller handling:**

```javascript
// app/javascript/controllers/chart_controller.js

export default class extends Controller {
  connect() {
    this.initializeChart()
    
    // Listen for Turbo Stream updates
    document.addEventListener('update-chart', (e) => {
      this.updateData(e)
    })
  }

  updateData(event) {
    const { time, open, high, low, close } = event.detail.candleData
    
    // Update the last candle or add new one
    this.candlesSeries.update({
      time,
      open,
      high,
      low,
      close
    })
  }
}
```

### Pattern 2: Direct update (for non-Rails use)

```javascript
// Simulate real-time updates
function simulateRealTimeUpdate() {
  const lastData = getLastDataPoint()
  
  // Update last candle with new OHLC
  series.update({
    time: lastData.time,
    open: lastData.open,
    high: Math.max(lastData.high, newPrice),
    low: Math.min(lastData.low, newPrice),
    close: newPrice
  })
  
  // Or add completely new candle
  series.update({
    time: Math.floor(Date.now() / 1000),
    open: newPrice,
    high: newPrice,
    low: newPrice,
    close: newPrice
  })
}

// Call on interval (e.g., every 1000ms)
setInterval(simulateRealTimeUpdate, 1000)
```

## Event Handling

### Mouse Events

```javascript
// Click event
chart.subscribeClick(function(param) {
  if (!param.point) return // Click outside chart area
  
  console.log(`Clicked at ${param.point.x}, ${param.point.y}`)
  console.log(`Time: ${param.time}`)
  
  // Get price at click point for all series
  param.seriesData.forEach((seriesData, series) => {
    if (seriesData.value !== undefined) {
      console.log(`Price: ${seriesData.value}`)
    } else if (seriesData.close !== undefined) {
      console.log(`Close: ${seriesData.close}`) // Candlestick series
    }
  })
})

// Crosshair movement
chart.subscribeCrosshairMove(function(param) {
  if (!param.point) return // Mouse outside chart
  
  console.log(`Crosshair at ${param.point.x}, ${param.point.y}`)
  console.log(`Price: ${param.seriesData.get(series).value}`)
  
  // Update tooltip at param.point.x, param.point.y
})
```

### Unsubscribe from Events

```javascript
const clickHandler = (param) => { /* ... */ }

chart.subscribeClick(clickHandler)

// Later, unsubscribe
chart.unsubscribeClick(clickHandler)
```

### Stimulus Controller with Event Handling

```javascript
export default class extends Controller {
  static targets = ["container", "tooltip"]

  connect() {
    this.initializeChart()
    this.setupEventHandlers()
  }

  setupEventHandlers() {
    this.chart.subscribeClick((param) => {
      this.handleChartClick(param)
    })

    this.chart.subscribeCrosshairMove((param) => {
      this.handleCrosshairMove(param)
    })
  }

  handleChartClick(param) {
    if (!param.point || !param.time) return

    const data = param.seriesData.get(this.candlesSeries)
    const price = data.close || data.value

    // Dispatch custom event to Rails
    this.dispatch("chart-click", {
      detail: { time: param.time, price: price, x: param.point.x, y: param.point.y }
    })
  }

  handleCrosshairMove(param) {
    if (!param.point) {
      this.tooltipTarget.style.display = "none"
      return
    }

    const data = param.seriesData.get(this.candlesSeries)
    const price = data.close || data.value

    // Show tooltip
    this.tooltipTarget.style.display = "block"
    this.tooltipTarget.style.left = (param.point.x + 10) + "px"
    this.tooltipTarget.style.top = (param.point.y + 10) + "px"
    this.tooltipTarget.innerHTML = `Price: $${price.toFixed(2)}`
  }

  disconnect() {
    if (this.chart) {
      this.chart.remove()
    }
  }
}
```

## Tooltips with Stimulus

```javascript
// app/javascript/controllers/chart_controller.js
export default class extends Controller {
  static targets = ["container", "tooltip"]

  connect() {
    this.initializeChart()
    this.setupTooltip()
  }

  setupTooltip() {
    this.chart.subscribeCrosshairMove((param) => {
      if (!param.point) {
        this.tooltipTarget.style.display = "none"
        return
      }

      const data = param.seriesData.get(this.candlesSeries)
      
      let tooltipText = ""
      if (data.open !== undefined) {
        // Candlestick
        tooltipText = `O: ${data.open} H: ${data.high} L: ${data.low} C: ${data.close}`
      } else if (data.value !== undefined) {
        // Area/Line
        tooltipText = `Value: ${data.value.toFixed(2)}`
      }

      this.tooltipTarget.innerHTML = tooltipText
      this.tooltipTarget.style.left = (param.point.x + 10) + "px"
      this.tooltipTarget.style.top = (param.point.y + 10) + "px"
      this.tooltipTarget.style.display = "block"
    })
  }
}
```

```erb
<%# app/views/charts/_chart.html.erb %>

<div data-controller="chart" data-chart-symbol-value="<%= @symbol %>">
  <div data-chart-target="container" style="height: 500px;"></div>
  <div 
    data-chart-target="tooltip"
    style="position: absolute; background: #000; color: #fff; padding: 8px; 
           border-radius: 4px; font-size: 12px; display: none; z-index: 100;"
  ></div>
</div>
```

## Common Patterns

### Pattern 1: Fetch and display historical data on page load

```ruby
# app/controllers/charts_controller.rb
def show
  @symbol = params[:symbol]
  @candles = fetch_historical_data(@symbol, 100) # Last 100 candles
end

private

def fetch_historical_data(symbol, count)
  # Your API call (Alpha Vantage, Finnhub, Crypto API, etc.)
  CandleData.where(symbol: symbol).last(count)
    .map { |c| { time: c.date.to_s, open: c.open, high: c.high, low: c.low, close: c.close } }
end
```

```javascript
// app/javascript/controllers/chart_controller.js
export default class extends Controller {
  static values = { initialData: Array }

  connect() {
    this.initializeChart()
    this.candlesSeries.setData(this.initialDataValue)
    this.chart.timeScale().fitContent()
  }
}
```

```erb
<%# app/views/charts/show.html.erb %>
<div data-controller="chart" data-chart-initial-data-value="<%= @candles.to_json %>">
  <div data-chart-target="container"></div>
</div>
```

### Pattern 2: Resize chart on window resize

```javascript
export default class extends Controller {
  connect() {
    this.initializeChart()
    window.addEventListener("resize", () => this.handleResize())
  }

  handleResize() {
    const container = this.containerTarget
    const width = container.clientWidth
    const height = container.clientHeight
    
    this.chart.applyOptions({ width, height })
  }

  disconnect() {
    window.removeEventListener("resize", () => this.handleResize())
    if (this.chart) this.chart.remove()
  }
}
```

### Pattern 3: Multiple charts on same page

```javascript
// app/javascript/controllers/multi_chart_controller.js
export default class extends Controller {
  static targets = ["container"]

  connect() {
    // Each container creates its own chart instance
    this.containerTargets.forEach((container, index) => {
      const chart = createChart(container)
      // Configure each chart independently
      const series = chart.addSeries(CandlestickSeries)
      series.setData(this.getDataForChart(index))
    })
  }
}
```

### Pattern 4: Real-time updates with Turbo Streams + Solid Cable

```ruby
# config/routes.rb
resource :stock do
  member do
    post :subscribe_to_updates
  end
end

# app/models/stock.rb
class Stock < ApplicationRecord
  after_commit :broadcast_update, on: :update

  private

  def broadcast_update
    broadcast_replace_to self, target: dom_id(self, :chart), partial: "stocks/chart"
  end
end

# app/channels/stock_channel.rb
class StockChannel < ApplicationCable::Channel
  def subscribed
    stock = Stock.find(params[:id])
    stream_for stock
  end
end
```

```erb
<%# app/views/stocks/_chart.html.erb %>
<%= turbo_stream_from @stock %>

<div data-controller="chart">
  <div data-chart-target="container"></div>
</div>

<script type="module">
  // Receives updates from Turbo Streams
  document.addEventListener('turbo:load', () => {
    // Chart updates via Stimulus controller
  })
</script>
```

## Solid Cable Setup for Real-Time

```ruby
# config/cable.yml - Use database adapter (no Redis required)
production:
  adapter: solid_cable
  
development:
  adapter: solid_cable
```

**Broadcasting from model:**

```ruby
# app/models/stock.rb
class Stock < ApplicationRecord
  after_update :broadcast_price_change

  def broadcast_price_change
    broadcast_append_to self, :price_updates do
      { time: Time.now.to_i, open: open, high: high, low: low, close: close }.to_json
    end
  end
end
```

**Subscribe in view:**

```erb
<%= turbo_stream_from @stock, :price_updates %>
```

**Handle in Stimulus:**

```javascript
export default class extends Controller {
  connect() {
    document.addEventListener('turbo:before-stream-render', (e) => {
      const newData = JSON.parse(e.detail.newStream.innerHTML)
      this.chart.update(newData)
    })
  }
}
```
