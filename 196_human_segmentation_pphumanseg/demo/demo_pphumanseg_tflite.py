#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import argparse

import cv2 as cv
import numpy as np
import tensorflow as tf


def run_inference(interpreter, input_size, image):
    # Pre process:Resize, Standardization, Transpose, expand dimensions
    input_image = cv.resize(image, dsize=(input_size[1], input_size[0]))
    mean = [0.5, 0.5, 0.5]
    std = [0.5, 0.5, 0.5]
    input_image = (input_image / 255 - mean) / std
    input_image = input_image.astype('float32')
    input_image = np.expand_dims(input_image, axis=0)

    # Inference
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()

    output_details = interpreter.get_output_details()
    segmentation_map = interpreter.get_tensor(output_details[0]['index'])

    # Post process:squeeze
    segmentation_map = np.squeeze(segmentation_map)

    return segmentation_map


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--movie", type=str, default=None)
    parser.add_argument("--score", type=float, default=0.5)
    parser.add_argument(
        "--model",
        type=str,
        default=
        'saved_model_human_segmentation_pphumanseg/model_float16_quant.tflite',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='192,192',
    )

    args = parser.parse_args()

    model_path = args.model
    input_size = [int(i) for i in args.input_size.split(',')]

    score = args.score

    cap_device = args.device
    if args.movie is not None:
        cap_device = args.movie

    # Initialize video capture
    cap = cv.VideoCapture(cap_device)

    # Load model
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    while True:
        start_time = time.time()

        # Capture read
        ret, frame = cap.read()
        if not ret:
            break
        debug_image = copy.deepcopy(frame)

        # Inference execution
        segmentation_map = run_inference(
            interpreter,
            input_size,
            frame,
        )

        elapsed_time = time.time() - start_time

        # Draw
        debug_image = draw_debug(
            debug_image,
            elapsed_time,
            score,
            segmentation_map,
        )

        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        cv.imshow('pphumanseg Demo', debug_image)

    cap.release()
    cv.destroyAllWindows()


def draw_debug(image, elapsed_time, score, segmentation_map):
    image_width, image_height = image.shape[1], image.shape[0]

    # Match the size
    debug_image = copy.deepcopy(image)
    segmentation_map = cv.resize(
        segmentation_map,
        dsize=(image_width, image_height),
        interpolation=cv.INTER_LINEAR,
    )

    # color list
    color_image_list = []
    # ID 0:BackGround
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = (0, 0, 0)
    color_image_list.append(bg_image)
    # ID 1:Human
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = (0, 255, 0)
    color_image_list.append(bg_image)

    # Overlay segmentation map
    masks = segmentation_map.transpose(2, 0, 1)
    for index, mask in enumerate(masks):
        # Threshold check by score
        mask = np.where(mask > score, 0, 1)

        # Overlay
        mask = np.stack((mask, ) * 3, axis=-1).astype('uint8')
        mask_image = np.where(mask, debug_image, color_image_list[index])
        debug_image = cv.addWeighted(debug_image, 0.5, mask_image, 0.5, 1.0)

    # Inference elapsed time
    cv.putText(debug_image,
               "Elapsed Time : " + '{:.1f}'.format(elapsed_time * 1000) + "ms",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
               cv.LINE_AA)

    return debug_image


if __name__ == '__main__':
    main()
