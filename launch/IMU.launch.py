import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # Define the path to the YAML file
    config = os.path.join(
        get_package_share_directory('my_bot'),  # Make sure this package name matches your actual package
        'config',
        'imu_parms.yaml'  # Ensure this YAML file exists in the correct location
    )

    # Create the Node for the BNO055 IMU
    node = Node(
        package='bno055',        # Name of the package
        executable='bno055', # Make sure this is the correct node executable name
        output='screen',         # Output logs to the screen
        parameters=[config]      # Load parameters from the YAML file
    )

    # Add the node to the launch description
    ld.add_action(node)

    return ld
