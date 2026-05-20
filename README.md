# EV3 Robot

EV3DEV-based robot project with LEGO EV3 large motors on output ports A and B, plus CAD files for the robot hardware layout.

## Repository

- GitHub: https://github.com/tucanoneverdie1976/ev3robot
- Local working directory: `D:\Work\ev3robot`
- Main drive test script: `beep_drive.py`

## EV3DEV Target

- Host/IP: `192.168.68.60`
- SSH user: `robot`
- Remote script path: `/home/robot/beep_drive.py`
- Do not commit passwords, tokens, or other secrets.

## Hardware Notes

- Output port A: EV3 large motor for drive
- Output port B: EV3 large motor for drive
- Observed EV3DEV `max_speed` for both motors: `1050`

## Current Drive Test

`beep_drive.py`:

1. Plays a short beep.
2. Drives forward for 1 second at speed `1050`.
3. Pauses briefly.
4. Drives backward for 1 second at speed `-1050`.
5. Stops both motors.

Run on the EV3:

```bash
python3 /home/robot/beep_drive.py
```

## Safety

- A previous 3-second high-load movement caused the EV3 to lose power while moving.
- Start new motion tests with short durations.
- Keep the robot lifted or in open space during high-speed tests.
- Send a stop command to both motors after each test run.
