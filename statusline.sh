#!/bin/bash

# Claude Code statusline (two lines)
# Line 1: branch ✗ | Model (effort)
# Line 2: Context % | 5h: % (time) | 7d: % (time)

input=$(cat)

# Color thresholds: green < 50%, yellow 50-79%, red >= 80%
color() {
  local pct=$1
  if [ "$pct" -ge 80 ] 2>/dev/null; then
    echo '\033[1;31m'
  elif [ "$pct" -ge 50 ] 2>/dev/null; then
    echo '\033[1;33m'
  else
    echo '\033[1;32m'
  fi
}

RESET='\033[0m'
DIM='\033[0;37m'
CYAN='\033[0;36m'
BLUE='\033[1;34m'
YELLOW='\033[0;33m'

cwd=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "$cwd" ] && cwd="$PWD"

# --- Line 1: branch ✗ | Model (effort) ---
line1=""

# Git branch + dirty
if git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1; then
  branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)
  changes=$(git -C "$cwd" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  line1="${BLUE}${branch}${RESET}"
  if [ "$changes" -gt 0 ]; then
    line1="${line1} ${YELLOW}✗${RESET}"
  fi
fi

# Model and effort
model=$(echo "$input" | jq -r '.model.display_name // empty' 2>/dev/null)
effort=$(jq -r '.effortLevel // empty' ~/.claude/settings.json 2>/dev/null)
if [ -n "$model" ]; then
  [ -n "$line1" ] && line1="${line1} | "
  line1="${line1}${CYAN}${model}${RESET}"
  if [ -n "$effort" ]; then
    line1="${line1} ${DIM}(${effort})${RESET}"
  fi
fi

now=$(date +%s)

# --- Line 2: Context | 5h | 7d ---
ctx=$(echo "$input" | jq -r '.context_window.used_percentage // 0' 2>/dev/null)
ctx_int=$(printf "%.0f" "$ctx" 2>/dev/null || echo "0")
ctx_color=$(color "$ctx_int")
line2="Context ${ctx_color}${ctx_int}%${RESET}"

five_h=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty' 2>/dev/null)
if [ -n "$five_h" ]; then
  five_int=$(printf "%.0f" "$five_h" 2>/dev/null || echo "0")
  five_color=$(color "$five_int")
  five_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty' 2>/dev/null)
  five_time=""
  if [ -n "$five_reset" ]; then
    diff=$((five_reset - now))
    if [ "$diff" -gt 0 ]; then
      hours=$((diff / 3600))
      mins=$(( (diff % 3600) / 60 ))
      if [ "$hours" -gt 0 ]; then
        five_time=" (${hours}h${mins}m)"
      else
        five_time=" (${mins}m)"
      fi
    fi
  fi
  line2="${line2} | 5h: ${five_color}${five_int}%${RESET}${five_time}"
fi

seven_d=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty' 2>/dev/null)
if [ -n "$seven_d" ]; then
  seven_int=$(printf "%.0f" "$seven_d" 2>/dev/null || echo "0")
  seven_color=$(color "$seven_int")
  seven_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty' 2>/dev/null)
  seven_time=""
  if [ -n "$seven_reset" ]; then
    diff=$((seven_reset - now))
    if [ "$diff" -gt 0 ]; then
      days=$((diff / 86400))
      hours=$(( (diff % 86400) / 3600 ))
      if [ "$days" -gt 0 ]; then
        seven_time=" (${days}d${hours}h)"
      else
        seven_time=" (${hours}h)"
      fi
    fi
  fi
  line2="${line2} | 7d: ${seven_color}${seven_int}%${RESET}${seven_time}"
fi

printf "%b\n" "$line1"
printf "%b\n" "$line2"
