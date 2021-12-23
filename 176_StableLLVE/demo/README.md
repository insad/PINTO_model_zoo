# Demo projects

## StableLLVE with ONNX Runtime in Python
```
python demo_StableLLVE_onnx.py
```

If you want to change the model, specify it with an argument.
```python
    parser.add_argument(
        "--model",
        type=str,
        default='stablellve_180x320/stablellve_180x320.onnx',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='180,320',
    )
```

## StableLLVE with TensorFlow Lite in Python
```
python demo_StableLLVE_tflite.py
```

If you want to change the model, specify it with an argument.
```python
    parser.add_argument(
        "--model",
        type=str,
        default='stablellve_180x320/model_float16_quant.tflite',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='180,320',
    )
```


