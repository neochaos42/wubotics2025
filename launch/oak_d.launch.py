from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='depthai_ros_driver',
            executable='depthai_ros_driver_node',
            name='oak_d_camera',
            output='screen',
            parameters=[
                {'camera_model': 'OAK-D'},
                {'rgb_resolution': '1080P'},
                {'fps': 30},
                {'enable_depth': True},
                {'depth_mode': 'ULTRA_ACCURATE'},
                {'confidence_threshold': 200},
            ],
            remappings=[
                ('/rgb/image_raw', '/camera/color/image_raw'),
                ('/stereo/depth', '/camera/depth/image_raw'),
            ]
        )
    ])