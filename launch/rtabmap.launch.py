import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
              # Nodelet for RGBD synchronization
        Node(
            package='nodelet',
            executable='nodelet',
            name='rgbd_sync',
            output='screen',
            parameters=[{'approx_sync': True}],
            remappings=[
                ('rgb/image', '/camera/rgb/image_rect_color'),
                ('depth/image', '/camera/depth_registered/image_raw'),
                ('rgb/camera_info', '/camera/rgb/camera_info'),
                ('rgbd_image', 'rgbd_image')  # output
            ]
        ),

        # RTAB-Map node
        Node(
            package='rtabmap_ros',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'frame_id': 'base_link',
                'subscribe_depth': False,
                'subscribe_rgbd': True,
                'subscribe_scan': True,
                'queue_size': 10,
                'RGBD/NeighborLinkRefining': True,
                'RGBD/ProximityBySpace': True,
                'RGBD/AngularUpdate': 0.01,
                'RGBD/LinearUpdate': 0.01,
                'RGBD/OptimizeFromGraphEnd': False,
                'Grid/FromDepth': False,  # occupancy grid from lidar
                'Reg/Force3DoF': True,
                'Reg/Strategy': 1,  # 1=ICP
                'Icp/VoxelSize': 0.05,
                'Icp/MaxCorrespondenceDistance': 0.1
            }],
            remappings=[
                ('odom', '/base_controller/odom'),
                ('scan', '/base_scan'),
                ('rgbd_image', 'rgbd_image')
            ]
        ),
    ])