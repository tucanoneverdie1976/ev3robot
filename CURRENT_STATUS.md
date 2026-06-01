# Current Project Status

Last updated: 2026-06-02 00:49 KST

This file records the current known-good state so the next Codex session can continue without rediscovering the setup.

## Repository

- Local repo: `D:\Work\ev3robot`
- GitHub repo: https://github.com/tucanoneverdie1976/ev3robot
- Current branch: `main`
- Latest known commit before this status note: `f09b1b9 Add RPi ROS2 LiDAR Foxglove setup`

## EV3DEV

- Target: `192.168.68.60`
- SSH user: `robot`
- Remote test script path: `/home/robot/beep_drive.py`
- Local script: `beep_drive.py`
- Motor ports:
  - `outA`: EV3 large motor
  - `outB`: EV3 large motor
- Observed motor `max_speed`: `1050`
- Current drive test behavior:
  1. Beep.
  2. Drive forward for 1 second at `1050`.
  3. Pause briefly.
  4. Drive backward for 1 second at `-1050`.
  5. Stop both motors.
- A previous 3-second movement caused EV3 power loss while moving. Use short motion tests first.

## Raspberry Pi ROS 2

- Target: `192.168.68.57`
- SSH user: `ros2test`
- Hostname: `ros2test`
- OS observed: Ubuntu 22.04.5 LTS
- ROS 2 distro observed: Humble
- Runtime workspace: `/home/ros2test/ros2_ws`
- Tracked repo folder: `rpi_ros2/`

## YDLidar X4

- Device: `/dev/ttyUSB0`
- Stable serial path observed: `/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0`
- Working params copied to: `rpi_ros2/params/x4.yaml`
- Working launch files copied to:
  - `rpi_ros2/launch/x4.launch.py`
  - `rpi_ros2/launch/x4_foxglove.launch.py`
- Verified scan topic: `/scan`
- Verified scan frame: `laser_frame`

## Foxglove

The RPi was verified running:

```text
ros2 launch ydlidar_ros2_driver x4_foxglove.launch.py
ydlidar_ros2_driver_node
foxglove_bridge
```

Foxglove bridge was listening on:

```text
0.0.0.0:8765
```

PC Foxglove connection URL:

```text
ws://192.168.68.57:8765
```

The user confirmed that Foxglove displays the LiDAR data correctly.

## Start LiDAR + Foxglove On RPi

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch ydlidar_ros2_driver x4_foxglove.launch.py
```

## Stop LiDAR + Foxglove On RPi

```bash
pkill -f "x4_foxglove|ydlidar_ros2_driver_node|foxglove_bridge"
```

## SLAM Next Steps

Goal: run live SLAM on the Raspberry Pi using YDLidar X4 and EV3 encoder odometry.

Required ROS graph:

```text
map -> odom -> base_link -> laser_frame
```

Current status:

- `/scan` works.
- Foxglove bridge works.
- `base_link -> laser_frame` static transform still needs to be added.
- `odom -> base_link` still needs to be created from EV3 A/B motor encoders.
- `slam_toolbox` needs to be installed or verified on the RPi.
- A combined launch file should start LiDAR, static TF, odometry bridge, SLAM Toolbox, and Foxglove.

Recommended implementation order:

1. Verify/install `ros-humble-slam-toolbox` on the RPi.
2. Add a static TF publisher for `base_link -> laser_frame` using the measured LiDAR mount position.
3. Build an EV3 odometry bridge:
   - Read A/B tacho positions from EV3DEV.
   - Compute differential-drive odometry.
   - Publish `/odom`.
   - Publish TF `odom -> base_link`.
4. Launch `slam_toolbox` in online async mode.
5. Verify `/map`, `/scan`, `/odom`, and `/tf` in Foxglove.

## Do Not Commit

- Passwords or tokens.
- ROS 2 `build/`, `install/`, or `log/` directories.
- Local-only secret files such as `.env`.
