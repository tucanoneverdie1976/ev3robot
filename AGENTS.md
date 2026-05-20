# Notes for Codex Agents

This repository contains EV3DEV robot code and CAD assets. Work carefully: changes may move real motors on physical hardware.

## Project Locations

- Local repo: `D:\Work\ev3robot`
- GitHub repo: https://github.com/tucanoneverdie1976/ev3robot
- EV3DEV target: `192.168.68.60`
- SSH user: `robot`
- Remote script path: `/home/robot/beep_drive.py`

Do not commit passwords or secrets. If authentication is needed, ask the user or use a local-only secret file that is ignored by Git.

## Hardware

- Port A: EV3 large motor, drive motor
- Port B: EV3 large motor, drive motor
- A/B motor `max_speed` observed from EV3DEV: `1050`

## Current Script

- File: `beep_drive.py`
- Uses EV3DEV sysfs directly under `/sys/class/tacho-motor`
- Finds motors by EV3 output port address, not by fixed `motor0`/`motor1` numbering
- Current behavior: beep, 1 second forward, short pause, 1 second backward
- Current speed: `1050` forward and `-1050` backward

## Safety Rules

- Treat every script execution as a real robot movement.
- Earlier 3-second movement caused power loss while the robot was moving.
- Prefer short movement durations for new tests.
- After every run, send `stop` to both motors.
- For maximum-speed tests, keep the robot lifted or ensure clear open space.
- If power drops or SSH times out during motion, reconnect and stop all motors before continuing.

## Suggested Stop Command

```bash
for m in /sys/class/tacho-motor/motor*; do
  echo stop > "$m/command" 2>/dev/null || true
done
```

## Git Notes

- Keep CAD files in the repo unless the user asks to split them out.
- Before pushing, run `git status --short --branch`.
- Use concise commits that separate code changes from CAD asset changes when practical.
