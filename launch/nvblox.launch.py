from typing import List, Tuple
from launch import Action, LaunchDescription
from launch_ros.descriptions import ComposableNode
import isaac_ros_launch_utils as lu
from nvblox_ros_python_utils.nvblox_launch_utils import NvbloxCamera
from nvblox_ros_python_utils.nvblox_constants import NVBLOX_CONTAINER_NAME

def get_oakd_remappings() -> List[Tuple[str, str]]:
    remappings = []
    remappings.append(('camera_0/depth/image', '/oak_d/camera/depth/image'))
    remappings.append(('camera_0/depth/camera_info', '/oak_d/camera/depth/camera_info'))
    remappings.append(('camera_0/color/image', '/oak_d/camera/color/image_raw'))
    remappings.append(('camera_0/color/camera_info', '/oak_d/camera/color/camera_info'))
    return remappings

def add_nvblox(args: lu.ArgumentContainer) -> List[Action]:
    # Set the camera to OAK-D and use static mode (no segmentation or detection)
    camera = NvbloxCamera.oakd

    remappings = get_oakd_remappings()
    camera_config = lu.get_path('nvblox_examples_bringup', 'config/nvblox/specializations/nvblox_oakd.yaml')

    base_config = lu.get_path('nvblox_examples_bringup', 'config/nvblox/nvblox_base.yaml')
    parameters = [base_config, camera_config]

    # Add the nvblox node for OAK-D camera
    nvblox_node = ComposableNode(
        name='nvblox_node',
        package='nvblox_ros',
        plugin='nvblox::NvbloxNode',
        remappings=remappings,
        parameters=parameters,
    )

    actions = []
    if args.run_standalone:
        actions.append(lu.component_container(args.container_name))
    actions.append(lu.load_composable_nodes(args.container_name, [nvblox_node]))
    actions.append(
        lu.log_info(
            ["Starting nvblox with the 'OAK-D' camera."]
        )
    )
    return actions

def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('container_name', NVBLOX_CONTAINER_NAME)
    args.add_arg('run_standalone', 'False')

    args.add_opaque_function(add_nvblox)
    return LaunchDescription(args.get_launch_actions())
