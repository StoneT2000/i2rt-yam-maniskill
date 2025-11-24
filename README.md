# I2RT YAM robot implementation for Maniskill


## Test script

```
python test.py --robot-uid yam
```

## Robot Modelling Details

Original MJCF file is sourced from [Mujoco Menagerie](https://github.com/google-deepmind/mujoco_menagerie/tree/main/i2rt_yam)

Converted initially to a URDF file via https://github.com/Yasu31/mjcf_urdf_simple_converter

Then the following modifications are made
- Change the incorrectly labelled fixed joints to prismatic, and add missing axes and limits definitions
- Add mimic joint tags between the left and right fingers
- Removed unnecessary fixed joints