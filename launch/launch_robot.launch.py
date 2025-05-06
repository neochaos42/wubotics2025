import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node


def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name = 'my_bot'  # <--- CHANGE ME

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )
    oak_d_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'oak_config.yaml')
    oak_d = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'oak_d.launch.py'
        )]), launch_arguments={'params_file': oak_d_params_file}.items()
    )
    robot_localization_parms = os.path.join(get_package_share_directory(
        package_name), 'config', 'ekf.yaml')
    robot_localization = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[{'use_sim_time': 'false'}, robot_localization_parms]
    )

    robot_description = ParameterValue(Command(
        ['ros2 param get --hide-type /robot_state_publisher robot_description']), value_type=str)

    controller_params_file = os.path.join(get_package_share_directory(
        package_name), 'config', 'my_controllers.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file]
    )

    delayed_controller_manager = TimerAction(
        period=1.0, actions=[controller_manager])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )
    ess = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'ESS.launch.py'
        )]), launch_arguments={'use_sim_time': 'false'}.items()
    )
    vslam_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'vslam_config.yaml')
    vslam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'vslam.launch.py'
        )]), launch_arguments={'params_file': vslam_params_file}.items()
    )
    nvblox_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'nvblox_config.yaml')
    nvblox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'nvblox.launch.py'
        )]), launch_arguments={'params_file': nvblox_params_file}.items()
    )
    nav2_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'nav2_config.yaml')
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'nav2.launch.py'
        )]), launch_arguments={'params_file': nav2_params_file}.items()
    )                
    # Launch them all!
    return LaunchDescription([
        rsp,
        oak_d,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        ess,
        vslam,
        robot_localization,
        nvblox,
        nav2
    ])
