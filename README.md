# Surgical Robotics Challenge
This branch provides specific instructions for the [ICRA 2026 Surgical Robotics Challenge](https://surgical-robotics-ai.github.io/icra-competition-2026/index.html), which implements a peg transfer task using ROS2.

# [Discussions Forum](https://github.com/surgical-robotics-ai/surgical_robotics_challenge/discussions)
Please check out the [Discussions tab](https://github.com/surgical-robotics-ai/surgical_robotics_challenge/discussions) to ask questions, post suggestions, connect with the community, and stay up to date with the challenge.

# 1. Install AMBF and ROS Prerequisites
Clone, build, and source `ambf-3.0` using these [instructions](https://github.com/WPI-AIM/ambf/wiki/Installing-AMBF).


# 2. Clone this repo to your local machine (recommended) OR use a Dockerfile

#### Option 1: (Clone repo to your local machine)
Please refer to the [README](./scripts/README.md) in the [scripts](./scripts) folder for instructions on installing the Python package for system-wide access.

#### Option 2: (Use Dockerfile)
You can also use the provided Dockerfiles to create Docker images by following the instructions here:
https://github.com/surgical-robotics-ai/docker_surgical_robotics_challenge


# 3. Running the simulation
[Source](https://github.com/WPI-AIM/ambf/wiki/Installing-AMBF#step-3) the ROS workspace containing AMBF, either in every terminal window that interacts with SRC or once in your `.bashrc` file.

Navigate to the `surgical_robotics_challenge` folder, which is `~/surgical_robotics_challenge` if you cloned it in your home directory.
Run the following in your terminal:
 ```bash
 ./run_env_pegboard_symmetric_with_wall.sh
 ```
A pair of windows showing a pegboard environment should appear.
 
  <p align="center">
  <img src=Media/sample_scene_pegboard_symmetric.png width="480"/>
  </p>

### 3a. The launch file:
To understand the launch file, refer to this [link](https://github.com/WPI-AIM/ambf/wiki/Selecting-Robots).


### 3b. Simulated Cameras
The simulated camera(s) are defined in the world file ([`world_stereo.yaml`](./ADF/world/world_stereo.yaml)), which is selected in [`launch.yaml`](./launch.yaml).
To enable the camera(s) to publish scene images or depth data, follow the [instructions](https://github.com/WPI-AIM/ambf/wiki/Camera-feed-and-depth-camera) on this page.

### 3c. Camera Coordinate frames
Camera coordinate frames, and the difference between the AMBF and `OpenCV` camera conventions, are described in [camera_conventions.md](./docs/camera_conventions.md).

### 3d. Resetting the Simulation
You can press `CTRL+R` to reset the rigid bodies in the simulation and `CTRL+V` to reset the camera pose.

### 3e. Launch Arguments
To manually control which objects are spawned in the scene, review the `.sh` scripts in this folder. For a full list of arguments that can be passed to AMBF, refer to these [instructions](https://github.com/WPI-AIM/ambf/wiki/Command-Line-Arguments).


# 4. Interacting with Simulated Robots using Python Scripts:
Please see the scripts in the [`scripts`](./scripts) folder.

## 4a. The Collaborative Robotics Toolkit Interface (CRTK):
To enable the CRTK interface for the PSMs and ECM in SRC, run the following script after starting SRC.
```bash
cd scripts/surgical_robotics_challenge
python launch_crtk_interface --scene False
```

The `scene` argument above is relevant for the suturing environment with entry and exit holes, so it should be disabled (`False`) for other environments, including the pegboard used for the ICRA 2026 challenge.


# 5. Controlling via Input Devices
The code in the `scripts` folder allows various input devices, including dVRK MTMs, Geomagic Touch, Phantom Omni, and Quest 3, to control the simulated PSMs. The ICRA 2026 challenge uses the Quest 3 hand controllers for teleoperation. The Quest 3 runs a Unity app that sends/receives CRTK-compatible JSON messages via UDP, in the format used by [sawSocketStreamer](https://github.com/jhu-saw/sawSocketStreamer). These are converted to CRTK-compatible ROS2 topics via the `udp_crtk_bridge.py` Python script, which is started by:

```
python udp_crtk_bridge.py
```

Refer to the `README` in the `scripts` folder for further information.

# 6. Citation
If you find this work useful, please cite it as:

```bibtex
@article{munawar2022open,
  title={Open Simulation Environment for Learning and Practice of Robot-Assisted Surgical Suturing},
  author={Munawar, Adnan and Wu, Jie Ying and Fischer, Gregory S and Taylor, Russell H and Kazanzides, Peter},
  journal={IEEE Robotics and Automation Letters},
  volume={7},
  number={2},
  pages={3843--3850},
  year={2022},
  publisher={IEEE}
}
```
