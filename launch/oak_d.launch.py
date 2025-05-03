import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import ComposableNodeContainer


def is_launch_config_true(context, name):
    return LaunchConfiguration(name).perform(context) == "true"


def setup_launch_prefix(context, *args, **kwargs):
    use_gdb = LaunchConfiguration("use_gdb", default="false")
    use_valgrind = LaunchConfiguration("use_valgrind", default="false")
    use_perf = LaunchConfiguration("use_perf", default="false")

    launch_prefix = ""

    if use_gdb.perform(context) == "true":
        launch_prefix += "xterm -e gdb -ex run --args"
    if use_valgrind.perform(context) == "true":
        launch_prefix += "valgrind --tool=callgrind"
    if use_perf.perform(context) == "true":
        launch_prefix += (
            "perf record -g --call-graph dwarf --output=perf.out.node_name.data --"
        )

    return launch_prefix


def launch_setup(context, *args, **kwargs):
    log_level = "info"
    if context.environment.get("DEPTHAI_DEBUG") == "1":
        log_level = "debug"

    namespace = LaunchConfiguration("namespace", default="").perform(context)
    name = LaunchConfiguration("name", default="oak").perform(context)
    params_file = LaunchConfiguration("params_file").perform(context)

    launch_prefix = setup_launch_prefix(context)

    return [
        ComposableNodeContainer(
            name=f"{name}_container",
            namespace=namespace,
            package="rclcpp_components",
            executable="component_container",
            composable_node_descriptions=[
                ComposableNode(
                    package="depthai_ros_driver",
                    plugin="depthai_ros_driver::Camera",
                    name=name,
                    namespace=namespace,
                    parameters=[params_file],
                )
            ],
            arguments=["--ros-args", "--log-level", log_level],
            prefix=[launch_prefix],
            output="both",
        ),
    ]


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument("name", default_value="oak"),
        DeclareLaunchArgument("namespace", default_value=""),
        DeclareLaunchArgument("use_gdb", default_value="false"),
        DeclareLaunchArgument("use_valgrind", default_value="false"),
        DeclareLaunchArgument("use_perf", default_value="false"),
        DeclareLaunchArgument(
            "params_file",
            default_value=os.path.join(
                get_package_share_directory("my_bot"),
                "config",
                "oak_d_params.yaml",
            ),
            description="Path to the parameters file to configure the OAK-D node.",
        ),
    ]

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )