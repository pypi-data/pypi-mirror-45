#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:52:07 2018

@author: daniel
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def load_video(path, image_rows=640, image_cols=480):
    vid_size = os.path.getsize(path)
    frm_dims = (image_cols, image_rows)
    frm_size = image_cols * image_rows

    if path.endswith('.avi'):
        header_init_size, header_mid_size = 5677, 8
        video_raw = np.memmap(path, dtype='uint8', mode='r', shape=(vid_size,))  # 5677, 8
        video_no_init_header = video_raw[header_init_size: -1].copy()
        n_chunks = len(video_no_init_header) // (frm_size + header_mid_size)
        video_clean = video_no_init_header[
                      0:n_chunks * (frm_size + header_mid_size)].reshape(-1, frm_size + header_mid_size)[:, header_mid_size:]
        video = video_clean.reshape((-1,) + frm_dims[::-1])
    else:
        num_of_frames = vid_size // 2 // frm_size
        video = np.memmap(path, dtype='uint16', mode='r', shape=(num_of_frames,) + frm_dims)
    return video.transpose([1, 2, 0])


def load_video_old(path):
    vid_size = os.path.getsize(path)
    video = np.fromfile(path, dtype=np.uint16, count=int(vid_size/2))
    return video.reshape((-1, 480, 640), order='C').transpose([1,2,0])


def load_frame(path, frame_num=None, frm_dims=(480, 640)):

    if frame_num is None:
        assert(type(path) is tuple or type(path) is list)
        frame_num = path[1]
        path = path[0]

    if path.endswith('.avi'):
        dtype, nbytes = 'uint8', 1
        header_init_size, header_mid_size = 5677, 8
        frm_dims = frm_dims[::-1]
        rot90_n = 0
    else:
        dtype, nbytes = 'uint16', 2
        header_init_size, header_mid_size = 0, 0
        rot90_n = 3

    offset = (header_init_size + header_mid_size) + nbytes*frame_num*(frm_dims[0]*frm_dims[1] + header_mid_size)

    frame = np.memmap(path, dtype=dtype, mode='r', offset=offset,  shape=frm_dims)
    return np.rot90(frame, k=rot90_n)


def load_json_filename(cml_args, default_value):
    """
    Choose either json file name given as a command line argument, or the default json file.
    """
    if len(cml_args) == 2:
        json_filename = cml_args[1]
    else:
        json_filename = default_value

    return json_filename


# if __name__ == "__main__":
    # a = load_video(r'Z:\all_recs_front\rec_20180816_102755\video_raw.avi')
    # print(a.shape)
    # plt.imshow(a[:,:,0])
    # plt.imshow(load_frame(r'Z:\all_recs_front\rec_20180830_125019\video_raw.avi', 0))
    # plt.show()
#     os.chdir(os.path.dirname(os.path.abspath(__file__)))
#     from sys import path
#     path.append('../')
#     import paths
#     video_id = 'rec_20181004_131313'
#     path = paths.raw_data + video_id + '/video_raw'
#     video = load_video(path)