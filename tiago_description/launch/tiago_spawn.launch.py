#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    tiago_description_path = get_package_share_directory('tiago_description')
    tiago_xacro = os.path.join(tiago_description_path, 'robots', 'tiago.urdf.xacro')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', tiago_xacro])
        }]
    )

    spawn_tiago = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_tiago',
        output='screen',
        arguments=[
            '-entity', 'tiago',
            '-topic', 'robot_description',
            '-x', '0', '-y', '0', '-z', '0.1'
        ]
    )

    return LaunchDescription([
        robot_state_publisher,
        TimerAction(period=5.0, actions=[spawn_tiago])  # Prevent early spawn
    ])