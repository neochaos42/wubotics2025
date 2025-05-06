from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Depth Image Processing: Converts disparity to depth
        Node(
            package='isaac_ros_depth_image_proc',
            executable='convert_metric',
            name='disparity_to_depth',
            output='screen',
            parameters=[{
                'baseline': 0.075,
                'image_transport': 'raw'
            }],
            remappings=[
                ('input', '/ess/disparity/image'),
                ('camera_info', '/camera/left/camera_info'),
                ('output', '/camera/depth/image')
            ]
        ),

        # NVBlox Node: 3D reconstruction
        Node(
            package='isaac_ros_nvblox',
            executable='nvblox_node',
            name='nvblox_node',
            output='screen',
            parameters=[
                {'use_tf_transforms': True},
                {'global_frame': 'odom'},
                # Load configuration file for NVBlox
                LaunchConfiguration('config_file')
            ],
            remappings=[
                ('/camera/depth/image', '/camera/depth/image'),
                ('/camera/depth/camera_info', '/camera/left/camera_info'),
                ('/camera/color/image_raw', '/camera/color/image_raw'),
                ('/camera/color/camera_info', '/camera/color/camera_info')
            ]
        ),
    ])
