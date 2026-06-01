# Raspberry Pi ROS 2 Notes

This folder tracks the working YDLidar X4 and Foxglove setup from the Raspberry Pi.

## Target

- Host/IP: `192.168.68.57`
- SSH user: `ros2test`
- OS observed: Ubuntu 22.04.5 LTS
- ROS 2 distro observed: Humble
- LiDAR device: `/dev/ttyUSB0`
- Stable serial path observed: `/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0`

## Files

- `launch/x4.launch.py`: starts the YDLidar X4 ROS 2 driver.
- `launch/x4_foxglove.launch.py`: starts the YDLidar X4 ROS 2 driver and `foxglove_bridge`.
- `params/x4.yaml`: working YDLidar X4 parameters.

The launch files currently point at the RPi runtime parameter path:

```text
/home/ros2test/ros2_ws/params/x4.yaml
```

## Run On The RPi

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch ydlidar_ros2_driver x4_foxglove.launch.py
```

## Connect From Foxglove On The PC

Use a Foxglove WebSocket connection:

```text
ws://192.168.68.57:8765
```

Expected ROS 2 topic:

```text
/scan
```

The tested scan frame is:

```text
laser_frame
```

## Verified State

- `/scan` was received successfully.
- Foxglove bridge listened on `0.0.0.0:8765`.
- PC Foxglove displayed the LiDAR data.

## Stop

```bash
pkill -f "x4_foxglove|ydlidar_ros2_driver_node|foxglove_bridge"
```
