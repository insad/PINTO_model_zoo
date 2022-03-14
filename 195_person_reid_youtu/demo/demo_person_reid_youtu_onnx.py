import argparse

import cv2 as cv
import numpy as np
import onnxruntime


def run_inference(onnx_session, input_size, image):
    # Pre process:Resize, Standardization, Transpose, float32 cast
    input_image = cv.resize(image, dsize=(input_size[1], input_size[0]))
    input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    input_image = (input_image / 255 - mean) / std
    input_image = input_image.transpose(2, 0, 1)
    input_image = np.expand_dims(input_image, axis=0)
    input_image = input_image.astype('float32')

    # Inference
    input_name = onnx_session.get_inputs()[0].name
    result = onnx_session.run(None, {input_name: input_image})

    # Post process:convert numpy array
    result = np.array(result[0][0])
    result = result.T[0][0]

    return result


def cos_similarity(X, Y):
    Y = Y.T

    # (768,) x (n, 768) = (n,)
    result = np.dot(X, Y) / (np.linalg.norm(X) * np.linalg.norm(Y, axis=0))

    return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        type=str,
        default='saved_model_person_reid_youtu/person_reid_youtu_2021nov.onnx',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='256,128',
    )

    args = parser.parse_args()
    model_path = args.model
    input_size = args.input_size

    input_size = [int(i) for i in input_size.split(',')]

    # Load model
    onnx_session = onnxruntime.InferenceSession(
        model_path,
        providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
    )

    # Read image
    image01 = cv.imread('image01.jpg')
    image02 = cv.imread('image02.jpg')

    # Inference
    feature_vector01 = run_inference(onnx_session, input_size, image01)
    feature_vector02 = run_inference(onnx_session, input_size, image02)

    print(cos_similarity(feature_vector01, feature_vector02))


if __name__ == '__main__':
    main()