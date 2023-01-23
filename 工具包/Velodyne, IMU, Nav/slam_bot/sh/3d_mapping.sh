#!/bin/bash

gnome-terminal -- bash -c "roslaunch slam_bot bot_spawn.launch"

gnome-terminal -- bash -c "rosrun teleop_twist_keyboard teleop_twist_keyboard.py"


