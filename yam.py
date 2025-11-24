import sapien
from mani_skill import ASSET_DIR
from mani_skill.agents.base_agent import BaseAgent, Keyframe
from mani_skill.agents.controllers import *
from mani_skill.agents.registration import register_agent
from mani_skill.sensors.camera import CameraConfig


@register_agent() # uncomment this if you want to register the agent so you can instantiate it by ID when creating environments
class YAM(BaseAgent):
    uid = "yam"
    urdf_path = f"./assets/yam.urdf"  # You can use f"{PACKAGE_ASSET_DIR}" to reference a urdf file in the mani_skill /assets package folder

    # you may need to use this modify the friction values of some links in order to make it possible to e.g. grasp objects or avoid sliding on the floor
    urdf_config = dict()
    keyframes = dict(
        zero=Keyframe(pose=sapien.Pose(), qpos=[0, 0, 0, 0, 0, 0, 0, 0])
    )
    @property
    def _controller_configs(self):
        arm_joint_pos = PDJointPosControllerConfig(
            joint_names=[
                "joint1",
                "joint2",
                "joint3",
                "joint4",
                "joint5",
                "joint6"
            ],
            lower=None,
            upper=None,
            stiffness=1e3,
            damping=1e2,
            normalize_action=False,
        )
        gripper_joint_pos = PDJointPosControllerConfig(
            joint_names=[
                "left_finger"
            ],
            lower=None,
            upper=None,
            stiffness=1e3,
            damping=1e2,
            normalize_action=False,
        )
        passive = PassiveControllerConfig(
            joint_names=["right_finger"],
            damping=0,
        )

        return dict(
            pd_joint_pos=dict(arm=arm_joint_pos, gripper=gripper_joint_pos, passive=passive)
        )