
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 
import socket


import pandas as pd

from rich.progress import track

qualisys_joints = [
'head',
'left_ear',
'right_ear',
'cspine',
'left_shoulder',
'right_shoulder',
'left_elbow',
'right_elbow',
'left_wrist',
'right_wrist',
'left_index',
'right_index',
'left_hip',
'right_hip',
'left_knee',
'right_knee',
'left_ankle',
'right_ankle',
'left_heel',
'right_heel',
'left_foot_index',
'right_foot_index',
]


# qualisys_marker_labels = [
# 'HeadTop',	
# 'HeadFront',
# 'HeadLeft',
# 'HeadRight',
# 'R_AntShoulder',
# 'R_PostShoulder',
# 'R_Arm',
# 'R_LatElbow',
# 'R_MedElbow',
# 'R_LatHand',
# 'R_MedHand',
# 'R_Hand',
# 'R_Thigh',
# 'R_LatKnee',
# 'R_MedKnee',
# 'R_Shin',
# 'R_LatAnkle',
# 'R_MedAnkle',
# 'R_Heel',
# 'R_LatFoot',
# 'R_MedFoot',
# 'R_Toe',
# 'L_AntShoulder',
# 'L_PostShoulder',
# 'L_LatElbow',
# 'L_MedElbow',
# 'L_LatHand',
# 'L_MedHand',
# 'L_Hand',
# 'L_Thigh',
# 'L_LatKnee',
# 'L_MedKnee',
# 'L_Shin',
# 'L_LatAnkle',
# 'L_MedAnkle',
# 'L_Heel',
# 'L_LatFoot',
# 'L_MedFoot',
# 'L_Toe',
# 'R_Back',
# 'L_Back',
# 'R_PSIS',
# 'L_PSIS',
# 'R_ASIS',
# 'L_ASIS',
# 'Chest']

# qualisys_marker_labels = [
# 'HeadLeft',
# 'HeadTop',	
# 'HeadRight',	
# 'HeadFront',	
# 'L_AntShoulder',	
# 'L_PostShoulder',	
# 'L_Arm',	
# 'L_LatElbow',	
# 'L_LatHand',	
# 'L_MedHand',	
# 'L_Hand',	
# 'R_AntShoulder',	
# 'R_PostShoulder',	
# 'R_Arm',	
# 'R_LatElbow',	
# 'R_LatHand',	
# 'R_MedHand',	
# 'R_Hand',	
# 'Chest',
# 'C7',	
# 'L_Back',	
# 'R_Back',	
# 'L_ASIS',	
# 'L_PSIS',	
# 'R_PSIS',	
# 'R_ASIS',	
# 'L_Thigh',	
# 'L_LatKnee',	
# 'L_Shin',	
# 'R_Thigh',	
# 'R_LatKnee',	
# 'R_Shin',	
# 'L_MedElbow',	
# 'R_MedElbow',	
# 'L_MedKnee',	
# 'R_MedKnee',	
# 'L_MedAnkle',	
# 'R_MedAnkle',	
# 'L_LatAnkle',	
# 'L_Heel',	
# 'L_Toe',	
# 'L_LatFoot',	
# 'L_MedFoot',	
# 'R_Heel',	
# 'R_LatAnkle',	
# 'R_Toe',	
# 'R_LatFoot',	
# 'R_MedFoot'
# ]

qualisys_marker_labels = [
    'RIC',
    'LIC',
    'RPSIS',
    'LPSIS',
    'SAC',
    'RASIS',
    'LASIS',
    'RGT',
    'LGT',
    'RLB',
    'RTh1',
    'RTh2',
    'RTh3',
    'RTh4',
    'RLFC',
    'RMFC',
    'RLTP',
    'RMTP',
    'RSh1',
    'RSh2',
    'RSh3',
    'RSh4',
    'RLMA',
    'RMMA',
    'RPHE',
    'RDHE',
    'RLHE',
    'R5TH',
    'R2ND',
    'R1ST',
    'RTOE',
    'LTh1',
    'LTh2',
    'LTh3',
    'LTh4',
    'LLFC',
    'LMFC',
    'LLTP',
    'LMTP',
    'LSh1',
    'LSh2',
    'LSh3',
    'LSh4',
    'LLMA',
    'LMMA',
    'LPHE',
    'LDHE',
    'LLHE',
    'L5TH',
    'L2ND',
    'L1ST',
    'LTOE',
    'RACR',
    'LACR',
    'STERN',
    'C7',
    'TopHead',
    'LHead',
    'RHead',
    'FrontHead',
    'RFrontShoulder',
    'RBackShoulder',
    'RLatElbow',
    'RMedElbow',
    'RMedWrist',
    'RLatWrist',
    'RHand',
    'LFrontShoulder',
    'LBackShoulder',
    'LLatElbow',
    'LMedElbow',
    'LLatWrist',
    'LMedWrist',
    'LHand',
]



def set_axes_ranges(plot_ax,skeleton_data,ax_range):

    mx = np.nanmean(skeleton_data[:,0])
    my = np.nanmean(skeleton_data[:,1])
    mz = np.nanmean(skeleton_data[:,2])

    plot_ax.set_xlim(mx-ax_range,mx+ax_range)
    plot_ax.set_ylim(my-ax_range,my+ax_range)
    plot_ax.set_zlim(mz-ax_range,mz+ax_range)     


#1) Set your data path using your computer name
#2) Make an empty session folder with a DataArrays folder in it
#3) Put in the original qualisys MAT file 
#4) Put the matlab script in the DataArrays folder 
#5) Run the script and save out the reorganized .mat file
#6) Change the session ID in the code 
#7) Pick a frame to use 
freemocap_data_folder_path = Path(r'D:\2023-05-17_MDN_NIH_data\qtm_data')


session_ID = 'qualisys_MDN_NIH_Trial2'
debug = True
#frame_to_use = 2000
freemocap_data_array_path = freemocap_data_folder_path/session_ID/'output_data'

qualisys_data = np.load(freemocap_data_array_path/'qualisys_markers_3d.npy')
qualisys_skel_save_path = freemocap_data_array_path/'qualisysSkel_3d.npy'

num_frames = qualisys_data.shape[0]
num_markers = len(qualisys_joints)
qualisys_joints_array = np.empty([num_frames,num_markers,3])

for frame_to_use in track(range(num_frames), description='Calculating Qualisys Joints'):
    ##THE (head) BASAL GANGLIA- SIGNIFICANT SOURCE OF  MOTOR CONTROL
    left_head = qualisys_marker_labels.index('LHead')
    right_head = qualisys_marker_labels.index('RHead')

    left_qualisys_left_head_XYZ = qualisys_data[frame_to_use,left_head,:]
    right_qualisys_right_head_XYZ = qualisys_data[frame_to_use,right_head,:]

    head_XYZ = np.mean([left_qualisys_left_head_XYZ,right_qualisys_right_head_XYZ],axis=0)
    head_joint_index = qualisys_joints.index('head')
    qualisys_joints_array[frame_to_use,head_joint_index,:] = head_XYZ

    left_head_marker_XYZ = qualisys_data[frame_to_use,left_head,:]
    right_head_marker_XYZ = qualisys_data[frame_to_use,right_head,:]

    left_head_joint_index = qualisys_joints.index('left_ear')
    right_head_joint_index = qualisys_joints.index('right_ear')

    qualisys_joints_array[frame_to_use,left_head_joint_index,:] = left_head_marker_XYZ
    qualisys_joints_array[frame_to_use,right_head_joint_index,:] = right_head_marker_XYZ

    ##Left wrist
    left_wrist1 = qualisys_marker_labels.index('LLatWrist') #getting the index of the marker
    left_wrist2 = qualisys_marker_labels.index('LMedWrist')
    right_latwrist = qualisys_marker_labels.index('RLatWrist')
    right_medwrist = qualisys_marker_labels.index('RMedWrist')

    left_qualisys_wrist1_XYZ = qualisys_data[frame_to_use,left_wrist1,:] #using the marker index to get the XYZ position of that marker
    left_qualisys_wrist2_XYZ = qualisys_data[frame_to_use,left_wrist2,:]
    right_qualisys_latwrist_XYZ = qualisys_data[frame_to_use,right_latwrist,:]
    right_qualisys_medwrist_XYZ = qualisys_data[frame_to_use,right_medwrist,:]

    left_wrist_XYZ = np.mean([left_qualisys_wrist1_XYZ,left_qualisys_wrist2_XYZ],axis=0) #calculating the joint XYZ position
    right_wrist_XYZ = np.mean([right_qualisys_latwrist_XYZ,right_qualisys_medwrist_XYZ],axis=0)

    left_wrist_joint_index = qualisys_joints.index('left_wrist') #getting the index of the joint
    right_wrist_joint_index = qualisys_joints.index('right_wrist')
    qualisys_joints_array[frame_to_use,left_wrist_joint_index,:] = left_wrist_XYZ #adding the XYZ position to the joint array using the joint index 
    qualisys_joints_array[frame_to_use,right_wrist_joint_index,:] = right_wrist_XYZ


    left_hand_marker_index = qualisys_marker_labels.index('LHand')
    right_hand_marker_index = qualisys_marker_labels.index('RHand')

    left_hand_XYZ = qualisys_data[frame_to_use,left_hand_marker_index,:]
    right_hand_XYZ = qualisys_data[frame_to_use,right_hand_marker_index,:]

    left_hand_joint_index = qualisys_joints.index('left_index')
    right_hand_joint_index = qualisys_joints.index('right_index')

    qualisys_joints_array[frame_to_use,left_hand_joint_index,:] = left_hand_XYZ
    qualisys_joints_array[frame_to_use,right_hand_joint_index,:] = right_hand_XYZ

    ##Both Left and Right Shoulder 
    left_antshoulder_index = qualisys_marker_labels.index('LFrontShoulder')
    left_postshoulder_index = qualisys_marker_labels.index('LBackShoulder')
    right_antshoulder_index = qualisys_marker_labels.index('RFrontShoulder')
    right_postshoulder_index = qualisys_marker_labels.index('RBackShoulder')

    left_antshoulder_XYZ = qualisys_data[frame_to_use,left_antshoulder_index,:]
    left_postshoulder_XYZ = qualisys_data[frame_to_use,left_postshoulder_index,:]
    right_antshoulder_XYZ = qualisys_data[frame_to_use,right_antshoulder_index,:]
    right_postshoulder_XYZ = qualisys_data[frame_to_use,right_postshoulder_index,:]

    left_shoulder_XYZ = np.mean([left_antshoulder_XYZ,left_postshoulder_XYZ],axis=0)
    right_shoulder_XYZ = np.mean([right_antshoulder_XYZ,right_postshoulder_XYZ],axis=0)

    left_shoulder_index = qualisys_joints.index('left_shoulder')
    right_shoulder_index = qualisys_joints.index('right_shoulder')
    qualisys_joints_array [frame_to_use,left_shoulder_index,:] = left_shoulder_XYZ
    qualisys_joints_array [frame_to_use,right_shoulder_index,:] = right_shoulder_XYZ

    ##Cervical spine
    right_shoulder_XYZ = np.mean([right_antshoulder_XYZ,right_postshoulder_XYZ],axis=0)
    left_shoulder_XYZ = np.mean([left_antshoulder_XYZ,left_postshoulder_XYZ],axis=0)

    cspine_XYZ = np.mean([right_shoulder_XYZ,left_shoulder_XYZ],axis=0)

    cspine_index = qualisys_joints.index('cspine')
    qualisys_joints_array[frame_to_use,cspine_index,:] = cspine_XYZ

    ##Both Left and Right Elbow
    left_lat_elbow_index = qualisys_marker_labels.index('LLatElbow')
    left_med_elbow_index = qualisys_marker_labels.index('LMedElbow')
    right_lat_elbow_index = qualisys_marker_labels.index('RLatElbow')
    right_med_elbow_index = qualisys_marker_labels.index('RMedElbow')

    left_lat_elbow_XYZ = qualisys_data[frame_to_use,left_lat_elbow_index,:]
    left_med_elbow_XYZ = qualisys_data[frame_to_use,left_med_elbow_index,:]
    right_lat_elbow_XYZ = qualisys_data[frame_to_use,right_lat_elbow_index,:]
    right_med_elbow_XYZ = qualisys_data[frame_to_use,right_med_elbow_index,:]

    left_elbow_XYZ = np.mean([left_lat_elbow_XYZ,left_med_elbow_XYZ],axis=0)
    right_elbow_XYZ = np.mean([right_lat_elbow_XYZ,right_med_elbow_XYZ],axis=0)

    left_elbow_index = qualisys_joints.index('left_elbow')
    right_elbow_index = qualisys_joints.index('right_elbow')
    qualisys_joints_array[frame_to_use,left_elbow_index,:] = left_elbow_XYZ
    qualisys_joints_array[frame_to_use,right_elbow_index,:] = right_elbow_XYZ

    ##Left and right knees
    left_medknee_index = qualisys_marker_labels.index('LMFC')
    left_latknee_index = qualisys_marker_labels.index('LLFC')
    right_medknee_index = qualisys_marker_labels.index('RMFC')
    right_latknee_index = qualisys_marker_labels.index('RLFC')

    left_medknee_XYZ = qualisys_data[frame_to_use,left_medknee_index,:]
    left_latknee_XYZ = qualisys_data[frame_to_use,left_latknee_index,:]
    right_medknee_XYZ = qualisys_data[frame_to_use,right_medknee_index,:]
    right_latknee_XYZ = qualisys_data[frame_to_use,right_latknee_index,:]

    left_knee_XYZ = np.mean([left_medknee_XYZ,left_latknee_XYZ],axis=0)
    right_knee_XYZ = np.mean([right_medknee_XYZ,right_latknee_XYZ],axis=0)

    left_knee_index = qualisys_joints.index('left_knee')
    right_knee_index = qualisys_joints.index('right_knee') 
    qualisys_joints_array [frame_to_use,left_knee_index,:] = left_knee_XYZ
    qualisys_joints_array [frame_to_use,right_knee_index,:] = right_knee_XYZ

    ##Left and Right Ankles
    left_medankle_index = qualisys_marker_labels.index('LMMA')
    left_latankle_index = qualisys_marker_labels.index('LLMA')
    right_medankle_index = qualisys_marker_labels.index('RMMA')
    right_latankle_index = qualisys_marker_labels.index('RLMA')

    left_medankle_XYZ = qualisys_data[frame_to_use,left_medankle_index,:]
    left_latankle_XYZ = qualisys_data[frame_to_use,left_latankle_index,:]
    right_medankle_XYZ = qualisys_data[frame_to_use,right_medankle_index,:]
    right_latankle_XYZ = qualisys_data[frame_to_use,right_latankle_index,:]

    left_ankle_XYZ = np.mean([left_medankle_XYZ,left_latankle_XYZ],axis=0)
    right_ankle_XYZ = np.mean([right_medankle_XYZ,right_latankle_XYZ],axis=0)

    left_ankle_index = qualisys_joints.index('left_ankle')
    right_ankle_index = qualisys_joints.index('right_ankle')
    qualisys_joints_array [frame_to_use,left_ankle_index,:] = left_ankle_XYZ
    qualisys_joints_array [frame_to_use,right_ankle_index,:] = right_ankle_XYZ

    ##Left and Right Foot
    left_medfoot_index = qualisys_marker_labels.index('L1ST')
    left_latfoot_index = qualisys_marker_labels.index('L5TH')
    right_medfoot_index = qualisys_marker_labels.index('R1ST')
    right_latfoot_index = qualisys_marker_labels.index('R5TH')

    left_medfoot_XYZ = qualisys_data[frame_to_use,left_medfoot_index,:]
    left_latfoot_XYZ = qualisys_data[frame_to_use,left_latfoot_index,:]
    right_medfoot_XYZ = qualisys_data[frame_to_use,right_medfoot_index,:]
    right_latfoot_XYZ = qualisys_data[frame_to_use,right_latfoot_index,:]

    left_foot_XYZ = np.mean([left_medfoot_XYZ,left_latfoot_XYZ],axis=0) #add toe marker into sum (make it a weighted sum)
    right_foot_XYZ = np.mean([right_medfoot_XYZ,right_latfoot_XYZ],axis=0)

    left_toe_index = qualisys_marker_labels.index('LTOE')
    left_toe_Y = qualisys_data[frame_to_use,left_toe_index,1]
    left_foot_XYZ[1] = left_toe_Y

    right_toe_index = qualisys_marker_labels.index('RTOE')
    right_toe_Y = qualisys_data[frame_to_use,right_toe_index,1]
    right_foot_XYZ[1] = right_toe_Y

    left_foot_index = qualisys_joints.index('left_foot_index')
    right_foot_index = qualisys_joints.index('right_foot_index')
    qualisys_joints_array [frame_to_use,left_foot_index,:] = left_foot_XYZ
    qualisys_joints_array [frame_to_use,right_foot_index,:] = right_foot_XYZ

    #Heel
    left_heel_index = qualisys_marker_labels.index('LDHE')
    left_heel_XYZ = qualisys_data[frame_to_use,left_heel_index, :]
    left_heel_joint_index= qualisys_joints.index('left_heel')
    qualisys_joints_array [frame_to_use,left_heel_joint_index,:] = left_heel_XYZ

    right_heel_index = qualisys_marker_labels.index('RDHE')
    right_heel_XYZ = qualisys_data[frame_to_use,right_heel_index, :]
    right_heel_joint_index= qualisys_joints.index('right_heel')
    qualisys_joints_array [frame_to_use,right_heel_joint_index,:] = right_heel_XYZ

    ##Hip Joint Centers 
    left_asis_index = qualisys_marker_labels.index('LASIS')
    left_psis_index = qualisys_marker_labels.index('LPSIS')
    right_asis_index = qualisys_marker_labels.index('RASIS')
    right_psis_index = qualisys_marker_labels.index('RPSIS')

    left_asis_XYZ = qualisys_data[frame_to_use,left_asis_index,:]
    left_psis_XYZ = qualisys_data[frame_to_use,left_psis_index,:]
    right_asis_XYZ = qualisys_data[frame_to_use,right_asis_index,:]
    right_psis_XYZ = qualisys_data[frame_to_use,right_psis_index,:]

    left_knee_XYZ[2] = left_knee_XYZ[2]*1.4
    right_knee_XYZ[2] = right_knee_XYZ[2]*1.4

    left_hip_XYZ = np.mean([left_asis_XYZ,left_psis_XYZ, left_knee_XYZ],axis=0) #weight the hip with knee 
    right_hip_XYZ = np.mean([right_asis_XYZ,right_psis_XYZ, right_knee_XYZ],axis=0)
    #left_hip_XYZ = 
    #right_hip_XYZ = 

    left_hip_index = qualisys_joints.index('left_hip')
    right_hip_index = qualisys_joints.index('right_hip')
    qualisys_joints_array [frame_to_use,left_hip_index,:] = left_hip_XYZ
    qualisys_joints_array [frame_to_use,right_hip_index,:] = right_hip_XYZ

np.save(qualisys_skel_save_path,qualisys_joints_array)


if debug:
        frame_to_plot = 6656
        figure = plt.figure()
        ax1 = figure.add_subplot(121,projection = '3d')
        ax2 = figure.add_subplot(122, projection = '3d')
        #ax3 = figure.add_subplot(122, projection = '3d')

        ax1.scatter(qualisys_data[frame_to_plot,:,0],qualisys_data[frame_to_plot,:,1],qualisys_data[frame_to_plot,:,2],c = 'r',marker = 'o')
        ax1.scatter(qualisys_joints_array[frame_to_plot,:,0],qualisys_joints_array[frame_to_plot,:,1],qualisys_joints_array[frame_to_plot,:,2],c = 'b',marker = '.')
        set_axes_ranges(ax1,qualisys_data[frame_to_plot,:,:],1000)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('Z')

        ax2.scatter(qualisys_joints_array[frame_to_plot,:,0],qualisys_joints_array[frame_to_plot,:,1],qualisys_joints_array[frame_to_plot,:,2],c = 'b',marker = 'o')
        set_axes_ranges(ax2,qualisys_joints_array[frame_to_plot,:,:],1000)
        

        plt.show()

##Bones 
# x = [qualisys_data[0] for point in qualisys_data]
# y = [qualisys_data[1] for point in qualisys_data]
# z = [qualisys_data[3] for point in qualisys_data]
# if qualisys_data.shape[0] == 1:
#     return qualisys_data[0,0,:]
# x,y,z = zip()
# plt.plot(x,y,z)
# set_axes_ranges(ax3,qualisys_data[frame_to_use,:,:],1000)
# plt.show()

f=2