# Demo projects

## Y-Net with ONNX Runtime in Python
```
python demo_Y-Net_onnx.py
```

If you want to change the model, specify it with an argument.
```python
    parser.add_argument(
        "--model",
        type=str,
        default='ynet_192x320/ynet_192x320.onnx',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='192,320',
    )
```

## Y-Net with TensorFlow Lite in Python
```
python demo_Y-Net_tflite.py
```

If you want to change the model, specify it with an argument.
```python
    parser.add_argument(
        "--model",
        type=str,
        default='ynet_192x320/model_float16_quant.tflite',
    )
    parser.add_argument(
        "--input_size",
        type=str,
        default='192,320',
    )
```


