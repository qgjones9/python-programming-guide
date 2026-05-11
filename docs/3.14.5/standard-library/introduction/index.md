# [Introduction](https://docs.python.org/3/library/intro.html)

Local notes keyed to the official documentation: Introduction.


## [WebAssembly Platform ](https://docs.python.org/3/library/intro.)

WebAssembly (Wasm) is beginning to play a role in AI/ML by enabling the execution of machine learning models in web browsers and other environments without requiring native code. For example, AI/ML libraries like TensorFlow.js and ONNX.js can run on WebAssembly, making it possible to perform inference directly in the browser or in sandboxed environments. This approach increases portability and security for AI/ML workloads and eliminates the need for users to install platform-specific binaries.

### Video Resources: WebAssembly and Machine Learning

Here are some helpful video resources that discuss the intersection of WebAssembly (Wasm) and Machine Learning (ML):

[Romain Clement - Machine Learning in the Browser: Fast Iteration with ONNX & WebAssembly](https://www.youtube.com/watch?v=6kWpRAr1ic8)


Inference at the edge -> WebAssembly
ONNX


## What is ONNX?

**ONNX (Open Neural Network Exchange)** is:

- A generic ML model representation: ONNX provides a standardized way to describe the structure and operations of machine learning models, regardless of the original framework used for their development. 
- A common, open file format for AI models: ONNX defines an extensible, open-source serialization convention that allows models to be saved, shared, and loaded by compatible tools across different platforms and environments.
- Designed for decoupling training and inference: ONNX enables models trained in one framework (like PyTorch or TensorFlow) to be exported for deployment and inference in another environment, such as a specialized runtime or hardware accelerator.
- Language-agnostic: ONNX models can be created and consumed by tooling written in any programming language, making them flexible and widely usable beyond the ecosystem of the original framework.
- Backend-agnostic: ONNX models can be executed on a variety of hardware and software backends, including CPUs, GPUs, mobile devices, and even web-based environments that support WebAssembly, thanks to ONNX-compatible runtimes.
- Focused on interoperability between different frameworks and tools: ONNX acts as a bridge, allowing seamless movement of models between diverse training, optimization, and inference tools, thus reducing the barriers between separate ML ecosystems.

ONNX Models

Export models from your framework of choice
- Scikit-learn: [`sklearn-onnx`](https://onnx.ai/sklearn-onnx/)  
  *Scikit-learn models can be converted to ONNX using the `sklearn-onnx` converter, which exports compatible pipelines and models into the ONNX format for cross-platform inference.*

- PyTorch: [`torch.onnx.export`](https://pytorch.org/docs/stable/onnx.html)  
  *PyTorch provides the `torch.onnx.export` utility to export trained PyTorch models to ONNX, enabling deployment to ONNX-compatible runtimes and hardware.*

- TensorFlow: [`tf.saved_model` & `tf2onnx`](https://github.com/onnx/tensorflow-onnx)  
  *TensorFlow models are typically saved in the SavedModel format, which can be converted to ONNX using the `tf2onnx` tool for interoperability and optimized inference.*

- XGBoost: [`xgboost.to_onnx`](https://onnx.ai/onnxmltools/generated/onnxmltools.convert.common.data_types.XGBoostConverter.html)  
  *XGBoost provides ONNX export functionality through integration with tools like `onnxmltools`, allowing tree-based models to be converted to ONNX.*

- LightGBM: [`lightgbm.to_onnx`](https://github.com/onnx/onnxmltools/blob/master/docs/convert/lightgbm_converter.md)  
  *LightGBM models can be exported via ONNX using converters like `onnxmltools`, which ensures compatibility across frameworks. See also [`lightgbm.onnx` support](https://github.com/microsoft/LightGBM/issues/4725).*

- CatBoost: [`catboost.to_onnx`](https://catboost.ai/en/docs/concepts/python-reference_catboost-save_model#onnx)  
  *CatBoost enables export of trained models to ONNX format via the `save_model` method with ONNX as the target format.*

- MXNet: [`mxnet.onnx`](https://mxnet.apache.org/api/python/docs/tutorials/onnx/export_mxnet_to_onnx.html)  
  *MXNet allows exporting models into ONNX using its ONNX module for inference using ONNX runtimes or other supported platforms.*

- Keras: [`keras2onnx`](https://github.com/onnx/keras-onnx)  
  *Keras models can be converted to ONNX using the `keras2onnx` converter, supporting both standalone Keras and TensorFlow-based models.*

- FastAI: [`fastai.export_onnx`](https://fastai.github.io/fastai/export.html#exporting-to-onnx)  
  *FastAI models can be exported to ONNX format using the built-in `export_onnx` function, allowing for efficient model deployment.*

Why are computational graphs important?

- **Portability**: Computational graphs can be serialized and deserialized, making it possible to move models between different environments and frameworks.
- **Optimization**: Computational graphs can be optimized for different hardware backends, making it possible to run models on different hardware platforms.
- **Debugging**: Computational graphs can be visualized, making it possible to debug models and understand how they work.
- **Interoperability**: Computational graphs can be used to interoperate with different frameworks and tools.

Netron: [https://netron.app/](https://netron.app/)
- Visualize ONNX models to better understand model structure, debug issues, and gain insights into the flow of data and operations—making it easier to explain, audit, or optimize complex neural networks.

ONNX Runtime: [https://onnxruntime.ai/](https://onnxruntime.ai/)

## ONNX Runtime

[ONNX Runtime](https://onnxruntime.ai/) is a high-performance engine for executing ONNX models. It supports models exported from many popular machine learning frameworks, enabling deployment in diverse environments such as servers, desktops, cloud, edge devices, and mobile phones.

Key features:
- **Cross-platform support**: ONNX Runtime runs on Windows, Linux, macOS, iOS, and Android, and can be integrated in Python, C/C++, C#, Java, JavaScript (Node.js bindings and browser), and more.
- **Hardware acceleration**: It can leverage hardware backends to accelerate computations, such as CUDA (NVIDIA GPUs), DirectML, OpenVINO (Intel), TensorRT, and others, improving inference speed and efficiency on compatible devices.
- **Flexible execution**: Supports both CPU and GPU execution with automatic fallback, and includes optimizations for common model architectures.
- **Production ready**: Designed for stability and performance in production environments, with support for quantized and optimized models.
- **Extensible**: Allows custom operators and execution providers for specialized scenarios.

Typical use cases:
- Deploying trained ML models for inference in production.
- Running models efficiently on edge devices or specialized hardware.
- Integrating model inference as part of a Python, C/C++, or other language application.
- Testing and benchmarking model performance across different hardware and runtimes.

Official docs and resources:  
- [ONNX Runtime documentation](https://onnxruntime.ai/docs/)
- [ONNX Runtime GitHub](https://github.com/microsoft/onnxruntime)

What is webassembly??

- Portable compilation target
- Client and server applications
- Major broswers support (desktop and mobile)
- Fast, safe, and open
- Privacy 

### How much client-side memory is needed for WebAssembly?

The client-side memory required for WebAssembly (Wasm) depends on several factors, including:

- **Initial Memory Allocation:** WebAssembly modules explicitly declare their starting (and optionally maximum) memory allocation in their code, typically in 64KiB pages. The minimal amount of memory required equals the initial memory size declared by the module.
- **Module Requirements:** Larger and more complex applications or models require more memory than simple ones. Applications like ONNX Runtime Web or heavy ML inference in Wasm will often request tens or hundreds of megabytes.
- **Browser Overhead:** Web browsers add their own memory overhead for running JavaScript, WebAssembly, page content, and other resources.
- **Dynamic Growth:** Some WebAssembly modules may be configured to grow their linear memory at runtime, up to a maximum limit.

#### Typical Memory Usage Examples

- **Small modules (utilities, basic functions):** Often 0.5–5 MB.
- **Machine learning models in ONNX Runtime Web:** Depending on model size, typically 10–200 MB or more, including memory for the Wasm runtime, loaded model, intermediate data (tensors), and input/output buffers.
- **Games or complex applications:** 50–500 MB or more.

#### Memory Limits

- **Browser limits:** Browsers may limit total memory allocated by a page (across scripts, Wasm, DOM, etc). These limits vary by browser and platform, typically between 1 GB and 4 GB for desktop browsers, and lower for mobile devices.
- **Wasm 32-bit memory model:** Linear memory is limited to 4 GB (2^32 bytes) per module, but most modules use much less.
- **User and system constraints:** Actual available memory depends on device RAM, current system usage, and browser configuration.

#### Considerations

- You can inspect the actual memory usage of Wasm modules using browser developer tools (e.g., Chrome DevTools > Performance > Memory).
- For ONNX Runtime Web, the memory required will include the WebAssembly runtime, the loaded ONNX model, pre/post-processing buffers, and any framework-specific data.
- If a module requests more memory than is available, allocation will fail and the module will not run as intended.

**In summary:**  
_Small WebAssembly modules may use just a few megabytes, while ML inference and large apps often use tens or hundreds of MB. Memory use is mainly dictated by the module’s initial and maximum memory declaration, model size (for ML), and browser/device limits._

For more detailed and up-to-date memory guidance, see:
- [WebAssembly Memory docs (MDN)](https://developer.mozilla.org/en-US/docs/WebAssembly/Memory)
- [ONNX Runtime Web docs: Memory requirements](https://onnxruntime.ai/docs/get-started/with-web.html#performance-and-memory-considerations)

## Famous users of WebAssembly
- [JupyterLite](https://jupyterlite.readthedocs.io/en/latest/)
- [TensorFlow.js](https://www.tensorflow.org/js)
- [ONNX Runtime Web](https://onnxruntime.ai/docs/)
- [Pyodide](https://pyodide.org/en/stable//)
- [Transformerjs](https://huggingface.co/docs/transformers.js/en/index)


## Resources


https://github.com/rclement/pydata-paris-2025-modelship-demo

## [Notes on availability](notes-on-availability/index.md)
