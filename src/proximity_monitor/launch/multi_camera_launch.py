# Copyright 2023 Intel Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DESCRIPTION #
# ----------- #
# Use this launch file to launch 2 devices.
# The Parameters available for definition in the command line for each camera are described in rs_launch.configurable_parameters
# For each device, the parameter name was changed to include an index.
# For example: to set camera_name for device1 set parameter camera_name1.
# command line example:
# ros2 launch realsense2_camera rs_multi_camera_launch.py camera_name1:=D400 device_type2:=l5. device_type1:=d4..

"""Launch realsense2_camera node."""
import os
import copy
from launch import LaunchDescription
import launch_ros.actions
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))


def set_configurable_parameters(local_params):
    return dict([(param['original_name'], LaunchConfiguration(param['name'])) for param in local_params])

def duplicate_params(general_params, posix):
    local_params = copy.deepcopy(general_params)
    for param in local_params:
        param['original_name'] = param['name']
        param['name'] += posix
    return local_params
    
def generate_launch_description():
    realsense_launch_file = os.path.join(
        get_package_share_directory('realsense2_camera'),
        'launch',
        'rs_launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(realsense_launch_file),
            launch_arguments={
                'camera_name': 'camera_back_top', 
                "serial_no":"_829212071824",
                'depth_module.profile': '424x240x6',
                'rgb_camera.profile': '320x240x6',
            }.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(realsense_launch_file),
            launch_arguments={
                'camera_name': 'camera_back_bottom', 
                "serial_no":"_829212071844",
                'depth_module.profile': '424x240x6 ',
                'rgb_camera.profile': '320x240x6',}.items(),
        ),
        # launch_ros.actions.Node(
        #     package = "depth_handler",
        #     executable = "depth_subscriber"
        # ),
        # launch_ros.actions.Node(
        #     package = "depth_handler",
        #     executable = "pcd_subscriber",
        #     name = 'pointcloud_shoulder_left',
        #     parameters = [{'camera_side': 'left'}]
        # ),
        launch_ros.actions.Node(
            package = "proximity_monitor",
            executable = "proximity_monitor",
            name = 'proximity_monitor_top',
            parameters = [{'camera_name': 'camera_back_top'},
                          {'proximity_warning_threshold': 0.2}]
        ),
        launch_ros.actions.Node (
            package = "proximity_monitor",
            executable = "proximity_monitor",
            name = 'proximity_monitor_bottom',
            parameters = [{'camera_name': 'camera_back_bottom'},
                          {'proximity_warning_threshold': 0.2}]
        ),
    ])
