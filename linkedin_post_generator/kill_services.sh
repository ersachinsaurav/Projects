#!/bin/bash
# LinkedIn Post Generator - Kill Services Script
# Kills all processes related to the LinkedIn Post Generator app

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   LinkedIn Post Generator - Kill Services    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

KILLED_COUNT=0

# Function to kill processes by port (only if in project directory)
kill_by_port() {
    local port=$1
    local name=$2
    local project_path=$(pwd)

    # Find PIDs using the port
    local pids=$(lsof -ti :$port 2>/dev/null || true)

    if [ -n "$pids" ]; then
        local found_any=false
        for pid in $pids; do
            local proc_info=$(ps -p $pid -o comm=,args= 2>/dev/null | head -1)

            # Only kill if it's in our project directory
            if echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
                if [ "$found_any" = false ]; then
                    echo -e "${YELLOW}🔍 Found processes on port $port ($name):${NC}"
                    found_any=true
                fi
                echo -e "   PID $pid: $proc_info"
                kill -TERM $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
            fi
        done

        if [ "$found_any" = true ]; then
            # Wait a bit for graceful shutdown
            sleep 1

            # Force kill if still running
            for pid in $pids; do
                local proc_info=$(ps -p $pid -o args= 2>/dev/null || echo "")
                if echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
                    if kill -0 $pid 2>/dev/null; then
                        echo -e "${RED}   ⚠️  Force killing PID $pid${NC}"
                        kill -KILL $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
                    fi
                fi
            done
            echo ""
        fi
    fi
}

# Function to kill processes by name pattern (only if in project directory)
kill_by_pattern() {
    local pattern=$1
    local name=$2
    local project_path=$3

    # Find PIDs matching the pattern
    local pids=$(pgrep -f "$pattern" 2>/dev/null || true)

    if [ -n "$pids" ]; then
        local found_any=false
        for pid in $pids; do
            # Skip if it's this script itself
            if [ "$pid" = "$$" ]; then
                continue
            fi

            local proc_info=$(ps -p $pid -o comm=,args= 2>/dev/null | head -1)
            # Only kill if it's in our project directory (if project_path provided)
            if [ -n "$project_path" ]; then
                if ! echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
                    continue
                fi
            fi

            if [ "$found_any" = false ]; then
                echo -e "${YELLOW}🔍 Found processes matching '$pattern' ($name):${NC}"
                found_any=true
            fi

            echo -e "   PID $pid: $proc_info"
            kill -TERM $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
        done

        if [ "$found_any" = true ]; then
            # Wait a bit for graceful shutdown
            sleep 1

            # Force kill if still running
            for pid in $pids; do
                if [ "$pid" = "$$" ]; then
                    continue
                fi
                proc_info=$(ps -p $pid -o args= 2>/dev/null || echo "")
                if [ -n "$project_path" ]; then
                    if ! echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
                        continue
                    fi
                fi
                if kill -0 $pid 2>/dev/null; then
                    echo -e "${RED}   ⚠️  Force killing PID $pid${NC}"
                    kill -KILL $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
                fi
            done
            echo ""
        fi
    fi
}

# Kill by ports (most reliable method)
# NOTE: We only kill ports if we can verify the process belongs to this project
echo -e "${BLUE}📡 Checking ports...${NC}"
kill_by_port 5170 "Backend API (FastAPI/Uvicorn)"
kill_by_port 5173 "Frontend Dev Server (Vite)"
kill_by_port 4173 "Frontend Preview Server"
# NOTE: SDXL WebUI (port 7860) is NOT killed - it's an external service
# that may be running independently. Only kill if explicitly started by this app.

# Kill by process patterns (only in this project directory)
echo -e "${BLUE}🔍 Checking process patterns...${NC}"
project_path=$(pwd)

# Uvicorn processes
kill_by_pattern "uvicorn.*backend.main:app" "Uvicorn Backend Server" "$project_path"

# Python backend processes
kill_by_pattern "python.*backend.main" "Python Backend Process" "$project_path"
kill_by_pattern "python.*-m.*uvicorn.*backend" "Uvicorn Module Process" "$project_path"

# Node/Vite processes (only in this project directory)
kill_by_pattern "node.*vite" "Vite Dev Server" "$project_path"
kill_by_pattern "vite.*dev" "Vite Dev Process" "$project_path"
kill_by_pattern "npm.*run.*dev" "NPM Dev Process" "$project_path"

# Watchfiles (uvicorn reload watcher) - only if in project
kill_by_pattern "watchfiles.*backend" "Watchfiles (Uvicorn Reload)" "$project_path"

# Python processes in THIS project directory only (be careful!)
echo -e "${BLUE}🔍 Checking Python processes in project directory...${NC}"
project_path=$(pwd)
project_pids=$(ps aux | grep -E "python.*$project_path|python.*linkedin_post_generator" | grep -v grep | grep -v "$$" | awk '{print $2}' || true)

if [ -n "$project_pids" ]; then
    for pid in $project_pids; do
        proc_info=$(ps -p $pid -o comm=,args= 2>/dev/null | head -1)
        # Only kill if it's in our project directory
        if echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
            echo -e "${YELLOW}   Found: PID $pid - $proc_info${NC}"
            kill -TERM $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
        fi
    done

    sleep 1

    # Force kill remaining
    for pid in $project_pids; do
        proc_args=$(ps -p $pid -o args= 2>/dev/null || echo "")
        if echo "$proc_args" | grep -qE "$project_path|linkedin_post_generator"; then
            if kill -0 $pid 2>/dev/null; then
                echo -e "${RED}   ⚠️  Force killing PID $pid${NC}"
                kill -KILL $pid 2>/dev/null && KILLED_COUNT=$((KILLED_COUNT + 1)) || true
            fi
        fi
    done
    echo ""
fi

# Summary
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
if [ $KILLED_COUNT -gt 0 ]; then
    echo -e "${GREEN}✅ Killed $KILLED_COUNT process(es)${NC}"
else
    echo -e "${YELLOW}ℹ️  No processes found to kill${NC}"
fi
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""

# Final verification (only check our app ports, not external services)
echo -e "${BLUE}🔍 Final check for remaining processes...${NC}"
remaining_ports=""
project_path=$(pwd)
for port in 5170 5173 4173; do
    pids=$(lsof -ti :$port 2>/dev/null || true)
    if [ -n "$pids" ]; then
        # Check if any PID belongs to our project
        for pid in $pids; do
            proc_info=$(ps -p $pid -o args= 2>/dev/null || echo "")
            if echo "$proc_info" | grep -qE "$project_path|linkedin_post_generator"; then
                remaining_ports="$remaining_ports $port"
                break
            fi
        done
    fi
done

if [ -n "$remaining_ports" ]; then
    echo -e "${RED}⚠️  Warning: Process(es) still using port(s):$remaining_ports${NC}"
    echo -e "${YELLOW}   You may need to manually kill them or restart your terminal${NC}"
else
    echo -e "${GREEN}✅ All app ports (5170, 5173, 4173) are free${NC}"
fi
echo -e "${BLUE}ℹ️  Note: External services (like SDXL on port 7860) are not checked${NC}"

echo ""

