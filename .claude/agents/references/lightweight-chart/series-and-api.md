# Lightweight Charts Series Types & API Reference

## Series Types & Data Formats

Lightweight Charts supports 6 series types. Each has different data format requirements.

### 1. Candlestick (most common for trading)

Used for OHLC (Open, High, Low, Close) data:

```javascript
const candleSeries = chart.addSeries(CandlestickSeries, {
  upColor: "#26a69a",      // Color when close > open
  downColor: "#ef5350",     // Color when close < open
  borderVisible: false,     // Hide border around candle
  wickUpColor: "#26a69a",   // Wick color for up candle
  wickDownColor: "#ef5350"  // Wick color for down candle
})

// Data format
candleSeries.setData([
  { time: "2024-01-01", open: 100.0, high: 105.5, low: 99.0, close: 104.2 },
  { time: "2024-01-02", open: 104.2, high: 110.0, low: 103.0, close: 108.5 },
  // ... more candles
])
```

Time can be: YYYY-MM-DD string, BusinessDay object, or UTC timestamp (seconds)

### 2. Area (value + fill)

Shows data as colored area with line:

```javascript
const areaSeries = chart.addSeries(AreaSeries, {
  lineColor: "#2962FF",           // Line color
  topColor: "#2962FF",            // Top gradient color
  bottomColor: "rgba(41, 98, 255, 0.28)" // Bottom gradient color
})

areaSeries.setData([
  { time: "2024-01-01", value: 32.51 },
  { time: "2024-01-02", value: 31.11 },
  // ...
])
```

### 3. Line (simple line chart)

Connects points with a line:

```javascript
const lineSeries = chart.addSeries(LineSeries, {
  color: "#2962FF",     // Line color
  lineWidth: 2          // Pixel width
})

lineSeries.setData([
  { time: "2024-01-01", value: 32.51 },
  { time: "2024-01-02", value: 35.11 },
  // ...
])
```

### 4. Bar (Open/High/Low/Close without wicks)

```javascript
const barSeries = chart.addSeries(BarSeries, {
  upColor: "#26a69a",   // Up bar color
  downColor: "#ef5350"  // Down bar color
})

barSeries.setData([
  { time: "2024-01-01", open: 100, high: 105, low: 99, close: 104 },
  // ...
])
```

### 5. Baseline (colored area above/below baseline)

```javascript
const baselineSeries = chart.addSeries(BaselineSeries, {
  baseValue: { type: "price", price: 100 },
  topLineColor: "#26a69a",
  topFillColor1: "rgba(38, 166, 154, 0.28)",
  topFillColor2: "rgba(38, 166, 154, 0.05)",
  bottomLineColor: "#ef5350",
  bottomFillColor1: "rgba(239, 83, 80, 0.28)",
  bottomFillColor2: "rgba(239, 83, 80, 0.05)"
})

baselineSeries.setData([
  { time: "2024-01-01", value: 32.51 },
  { time: "2024-01-02", value: 31.11 },
  // ...
])
```

### 6. Histogram (vertical bars for volume)

```javascript
const histogramSeries = chart.addSeries(HistogramSeries, {
  color: "#2962FF"
})

histogramSeries.setData([
  { time: "2024-01-01", value: 5000000 },  // Volume
  { time: "2024-01-02", value: 6500000 },
  // ...
])
```

## IChartApi: Main Chart Methods

```javascript
const chart = createChart(container, options)

// Data Management
chart.addSeries(SeriesType, options)          // Add new series
chart.removeSeries(series)                    // Remove series

// Time Scale
chart.timeScale().fitContent()                // Auto-fit visible data
chart.timeScale().getVisibleRange()           // Get current visible range
chart.timeScale().setVisibleRange({ from, to }) // Set visible time range
chart.timeScale().scrollToPosition(pos)       // Scroll to position

// Price Scale
chart.priceScale("right").applyOptions({})    // Customize right price scale
chart.priceScale("left").applyOptions({})     // Customize left price scale

// Layout
chart.applyOptions({ layout: { textColor, background } })

// Size
chart.applyOptions({ width: 800, height: 600 })
chart.getChartElement()                       // Get canvas element

// Remove/Cleanup
chart.remove()                                // Clean up and remove chart

// Events (see Event Handling section)
chart.subscribeClick(handler)
chart.subscribeCrosshairMove(handler)
```

## ISeriesApi: Series Data Methods

```javascript
const series = chart.addSeries(CandlestickSeries, options)

// Data
series.setData(data)                          // Set all data (replace)
series.update(dataItem)                       // Update last or add new
series.dataByIndex(logicalIndex, modeOrNull)  // Get data at logical index

// Price Lines (horizontal lines with labels)
series.createPriceLine({
  price: 105.5,
  color: "#FF0000",
  lineWidth: 2,
  lineStyle: 2,  // 0=solid, 1=dotted, 2=dashed
  axisLabelVisible: true,
  title: "Resistance"
})

// Series Options
series.applyOptions({ upColor: "#26a69a" })

// Price Scale Binding
series.priceScale()                           // Get price scale API
series.priceScale().applyOptions({
  scaleMargins: { top: 0.1, bottom: 0.1 }
})
```

## Chart Customization

### Layout Options

```javascript
const chartOptions = {
  layout: {
    textColor: "#000000",           // Price scale & time labels
    fontSize: 12,
    fontFamily: "Arial, sans-serif",
    background: {
      type: "solid",
      color: "#ffffff"              // Solid background
      // OR
      // type: "gradient"
      // color1: "#ffffff"
      // color2: "#f0f0f0"
    }
  },
  
  // Grid
  grid: {
    vertLines: { color: "#e8e8e8", visible: true },
    horzLines: { color: "#e8e8e8", visible: true }
  },

  // Crosshair (the cursor lines)
  crosshair: {
    mode: 0,                        // 0=normal, 1=magnet
    vertLine: {
      color: "#6a86ad",
      width: 2,
      style: 0,                     // 0=solid, 1=dotted, 2=dashed
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

  // Watermark (background text)
  watermark: {
    color: "rgba(0, 0, 0, 0.1)",
    text: "TradingView Lightweight Charts",
    visible: false
  }
}

chart.applyOptions(chartOptions)
```

### Time Scale Options

```javascript
chart.timeScale().applyOptions({
  timeVisible: true,              // Show time in labels
  secondsVisible: false,          // Show seconds
  fixLeftEdge: true,              // Prevent scrolling past first candle
  fixRightEdge: true,             // Prevent scrolling past last candle
  lockRange: false,               // Allow zooming/scrolling
  rightOffset: 0,                 // Space on right
  barSpacing: 6,                  // Pixels between candles
  minBarSpacing: 0.5              // Minimum pixels between candles when zoomed out
})

// Scroll to specific date
chart.timeScale().scrollToPosition(-10)  // -10 bars from end

// Get visible range
const range = chart.timeScale().getVisibleRange()
console.log(range.from, range.to)

// Fit all data in view
chart.timeScale().fitContent()
```

### Price Scale Options

```javascript
chart.priceScale("right").applyOptions({
  autoScale: true,                // Auto-scale to visible data
  autoScaleDisabled: false,
  mode: 0,                        // 0=normal, 1=log, 2=percentage
  
  scaleMargins: {
    top: 0.2,                     // 20% margin at top
    bottom: 0.2                   // 20% margin at bottom
  },

  ticksVisible: true,             // Show price ticks
  entireTextOnly: false,          // Truncate labels if needed
  
  borderVisible: true,
  borderColor: "#cccccc"
})

// Hide right price scale
chart.priceScale("right").applyOptions({ visible: false })
```

## Multiple Series with Different Scales

```javascript
// Add price series on right scale
const priceSeries = chart.addSeries(CandlestickSeries, {
  priceScaleId: "right"
})

// Add volume on left scale
const volumeSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: "left",
  color: "#26a69a"
})

// Customize scales separately
chart.priceScale("right").applyOptions({
  scaleMargins: { top: 0.2, bottom: 0.2 }
})

chart.priceScale("left").applyOptions({
  scaleMargins: { top: 0.2, bottom: 0.2 }
})

// Show both scales
chart.priceScale("left").applyOptions({ visible: true })
```

## Price Lines & Markers

```javascript
// Add horizontal price line
const priceLine = series.createPriceLine({
  price: 100.50,
  color: "#FF0000",
  lineWidth: 2,
  lineStyle: 2,                   // 2 = dashed
  axisLabelVisible: true,
  title: "Support Level",
  scaleMargin: 0.1
})

// Add markers to data points (signal/alert indicators)
series.setMarkers([
  { time: "2024-01-15", position: "aboveBar", color: "#00FF00", shape: "circle", text: "Buy" },
  { time: "2024-01-20", position: "belowBar", color: "#FF0000", shape: "arrowDown", text: "Sell" }
])

// Marker positions: "aboveBar", "belowBar", "inBar"
// Shapes: "circle", "square", "arrowUp", "arrowDown"
```
