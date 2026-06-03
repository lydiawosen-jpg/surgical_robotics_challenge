from PyKDL import Frame, Wrench
from surgical_robotics_challenge.psm_arm import PSM
from surgical_robotics_challenge.utils import coordinate_frames


def load_selected_psm_arms(simulation_manager, cam, run_psm_one, run_psm_two, run_psm_three, tool_id=None):
    psm_by_name = {}

    psm_configs = [
        ('psm1', run_psm_one, coordinate_frames.PSM1.T_tip_cam),
        ('psm2', run_psm_two, coordinate_frames.PSM2.T_tip_cam),
        ('psm3', run_psm_three, coordinate_frames.PSM3.T_tip_cam),
    ]

    for arm_name, enabled, tip_in_camera in psm_configs:
        if not enabled:
            continue

        print('LOADING CONTROLLER FOR ', arm_name)
        psm_kwargs = {'add_joint_errors': False}
        if tool_id is not None:
            psm_kwargs['tool_id'] = tool_id

        psm = PSM(simulation_manager, arm_name, **psm_kwargs)
        if not psm.is_present():
            continue

        T_psmtip_b = psm.get_T_w_b() * cam.get_T_c_w() * tip_in_camera
        psm.set_home_pose(T_psmtip_b)
        psm_by_name[arm_name] = psm

    return psm_by_name


def apply_mtm_to_psm_command(leader, psm, T_c_b, update_dt, set_jaw_only_when_coag=False):
    if leader.clutch_button_pressed:
        leader.free_with_orientation_lock()
    elif leader.coag_button_pressed and not leader.clutch_button_pressed:
        leader.free()
    else:
        leader.hold()

    twist = leader.measured_cv() * coordinate_frames.TeleopScale.scale_factor
    cmd_xyz = psm.T_t_b_home.p
    if not leader.clutch_button_pressed:
        delta_t = T_c_b.M * twist.vel * update_dt
        cmd_xyz = cmd_xyz + delta_t
        psm.T_t_b_home.p = cmd_xyz

    T_ik = None
    if leader.coag_button_pressed:
        cmd_rpy = T_c_b.M * leader.measured_cp().M
        T_ik = Frame(cmd_rpy, cmd_xyz)
        psm.servo_cp(T_ik)

    if (not set_jaw_only_when_coag) or leader.coag_button_pressed:
        psm.set_jaw_angle(leader.get_jaw_angle())

    return cmd_xyz, T_ik