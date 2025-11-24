import sapien
from mani_skill import ASSET_DIR
from mani_skill.agents.base_agent import BaseAgent, Keyframe
from mani_skill.agents.controllers import *
from mani_skill.agents.registration import register_agent
from mani_skill.sensors.camera import CameraConfig
import torch
from mani_skill.utils.structs import Pose
@register_agent() # uncomment this if you want to register the agent so you can instantiate it by ID when creating environments
class YAM(BaseAgent):
    uid = "yam"
    urdf_path = f"./assets/yam.urdf"  # You can use f"{PACKAGE_ASSET_DIR}" to reference a urdf file in the mani_skill /assets package folder

    # you may need to use this modify the friction values of some links in order to make it possible to e.g. grasp objects or avoid sliding on the floor
    urdf_config = dict(
        _materials=dict(
            gripper=dict(static_friction=2.0, dynamic_friction=2.0, restitution=0.0),
            
        ),
        link=dict(
            link_left_finger=dict(
                material="gripper", patch_radius=0.1, min_patch_radius=0.1
            ),
            link_right_finger=dict(
                material="gripper", patch_radius=0.1, min_patch_radius=0.1
            ),
        ),
    )
    keyframes = dict(
        zero=Keyframe(pose=sapien.Pose(), qpos=[0, 0, 0, 0, 0, 0, 0, 0])
    )
    @property
    def _controller_configs(self):

        # code below is the correct way to model the arm + mimic gripper joint
        # one problem however is maniskill defaults to creating a fixed tendon for the mimic joint (most stable we found)
        # with stiffness 1e5 to ensure the joints mimic very tightly. 
        # This high stiffness can sometimes be a problem since it may cause non gripper joints to move as well.
        # a work around is to allow setting drive targets of both fingers with PDJointPosMimicControllerConfig as done in the panda arm controller
        # which then allows 1 action to set both finger joint targets, which removes the issue above.
        # physx is wonky...

        # arm_joint_pos = PDJointPosControllerConfig(
        #     joint_names=[
        #         "joint1",
        #         "joint2",
        #         "joint3",
        #         "joint4",
        #         "joint5",
        #         "joint6"
        #     ],
        #     lower=None,
        #     upper=None,
        #     stiffness=1e4,
        #     damping=1e3,
        #     force_limit=100,
        #     normalize_action=False,
        # )
        # gripper_joint_pos = PDJointPosControllerConfig(
        #     joint_names=[
        #         "left_finger",
        #     ],
        #     lower=None,
        #     upper=None,
        #     stiffness=1e3,
        #     damping=1e2,
        #     force_limit=100,
        #     normalize_action=False,
        # )
        # passive = PassiveControllerConfig(
        #     joint_names=["right_finger"],
        #     damping=0,
        # )

        # return dict(
        #     pd_joint_pos=dict(arm=arm_joint_pos, gripper=gripper_joint_pos, passive=passive)
        # )
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
            force_limit=100,
            normalize_action=False,
        )
        gripper_joint_pos = PDJointPosMimicControllerConfig(
            joint_names=[
                "left_finger", "right_finger"
            ],
            lower=None,
            upper=None,
            stiffness=1e3,
            damping=1e2,
            force_limit=100,
            normalize_action=False,
            mimic={
                "right_finger": {"joint": "left_finger"}
            }
        )

        return dict(
            pd_joint_pos=dict(arm=arm_joint_pos, gripper=gripper_joint_pos)
        )
    
    @property
    def tcp_pose(self):
        return Pose.create_from_pq()

    def is_grasping(self, obj):
        return torch.ones((1, ), dtype=bool)
    def is_static(self, x):
        return torch.ones((1, ), dtype=bool)