# Lightweight Charts Performance & Troubleshooting Reference

## Large Dataset Optimization

### Data Conflation (v5.1+)

Lightweight Charts automatically merges data points when zoomed out for performance:

```javascript
// Conflation is enabled by default, but you can configure it
const chartOptions = {
  // Data conflation automatically optimizes rendering
  // When bar spacing < 0.5px, multiple bars are merged
  conflictResolution: {
    enabled: true,
    timeScale: "minute"  // Aggregate by minute when needed
  }
}
```

### Manual Pagination for Very Large Datasets

```javascript
// Only load visible data + buffer
const loadChartData = async (from, to) => {
  const data = await fetch(`/api/candles?from=${from}&to=${to}`)
  const candles = await data.json()
  
  series.setData(candles)
  chart.timeScale().fitContent()
}

// Track visible range and load more when scrolling
chart.timeScale().subscribeVisibleTimeRangeChange((newRange) => {
  const from = newRange.from
  const to = newRange.to
  
  loadChartData(from, to)
})
```

### Performance Tips

- ✅ Use `series.update()` for real-time ticks, NOT `setData()` (replaces all data)
- ✅ Enable data conflation for 10,000+ data points
- ✅ Limit real-time update frequency to 100-500ms intervals
- ✅ Use markers sparingly; marker performance degrades with 15,000+ data points
- ✅ Consider using histogram for volume (separate from price series)
- ✅ Lazy-load historical data outside viewport

## Troubleshooting

### Chart not appearing

- Check container has CSS dimensions (width/height)
- Verify `chart.remove()` called before creating new chart
- Check browser console for errors: `createChart()` requires DOM element

### Performance lag with real-time updates

- Use `series.update()` instead of `setData()` for new ticks
- Limit update frequency to 500ms intervals
- Enable data conflation for 10,000+ data points
- Check for memory leaks: verify `chart.remove()` called on disconnect

### Crosshair/tooltip not showing

- Ensure Crosshair options are not hidden in chart options
- Check CSS `z-index` conflicts with tooltip elements
- Verify event handler `param.point` exists (not null outside chart)

### Data not updating in real-time

- Confirm `turbo_stream_from` subscription is active
- Verify Solid Cable/WebSocket connection established
- Check Stimulus controller `connect()` method runs
- Use browser DevTools Network tab to see WebSocket messages

### Large dataset performance

- Enable data conflation (v5.1+)
- Implement pagination/lazy loading
- Reduce marker count (impacts performance >15k data points)
- Use appropriate time scale: don't show all 60k candles at once

## Attribution & License

Lightweight Charts™ is provided by TradingView. The license **requires attribution**.

Add to your application:

```html
<!-- In footer or about page -->
<p>Charts powered by <a href="https://www.tradingview.com">TradingView</a></p>
```

Include in README:

```
This application uses Lightweight Charts™ by TradingView.
See https://github.com/tradingview/lightweight-charts for license and attribution details.
```

## Additional Resources

- **Official Docs:** https://tradingview.github.io/lightweight-charts/docs
- **Tutorials:** https://tradingview.github.io/lightweight-charts/tutorials
- **API Reference:** https://tradingview.github.io/lightweight-charts/docs/api
- **Examples:** https://tradingview.github.io/lightweight-charts/tutorials/demos
- **GitHub:** https://github.com/tradingview/lightweight-charts
- **Discussion:** https://github.com/tradingview/lightweight-charts/discussions
