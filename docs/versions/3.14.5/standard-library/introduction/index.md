# [Introduction](https://docs.python.org/3/library/intro.html)

## [WebAssembly Platform](https://docs.python.org/3/library/intro.)

WebAssembly (Wasm) is a technology that allows code written in languages like C, C++, and Rust to run efficiently and safely in web browsers and other platforms, without needing to be rewritten in JavaScript. It acts as a portable compilation target, enabling software to work across devices and operating systems in a fast, secure, and open way.

WebAssembly is supported by all major browsers on desktop and mobile, enabling developers to run client and server applications in the browser or embedded in other environments.

### What is WebAssembly?

| Feature              | Description |
|----------------------|-------------|
| **Portable**         | Software compiled to WebAssembly can run on any platform that supports the Wasm standard—this increases code reuse across different systems. |
| **Efficient**        | Wasm code runs at near-native speed, allowing demanding tasks like graphics, simulations, and games to run smoothly in a browser. |
| **Secure and sandboxed** | WebAssembly runs in a secure environment with limited access to the host system, helping protect users from security risks. |
| **Growing ecosystem** | Many projects utilize WebAssembly to bring language runtimes and desktop-grade applications into the browser or other constrained platforms. |

### How much client-side memory is needed for WebAssembly?

WebAssembly's memory usage depends on the specific application and its configuration. Key considerations are:

| Factor               | Description |
|----------------------|-------------|
| **Initial Allocation** | When a WebAssembly program starts, it declares how much memory it needs—typically in units called pages (each is 64KiB). |
| **Growth**             | Some applications can request more memory as they run, up to a set limit. |
| **Program Complexity** | Simple Wasm programs (like utilities or number crunchers) may use only a few MB, while complex applications (such as games or software originally built for desktop use) can use hundreds of MB. |
| **Browser Overhead**   | In addition to Wasm's own memory, browsers require extra memory for JavaScript, page content, and system resources. |
| **Platform Limits**    | Browsers may cap memory for Wasm programs—commonly ranging from 1-4 GB on desktops, and less for mobile. |

You can inspect memory usage for WebAssembly programs in browser developer tools (such as Chrome DevTools > Performance > Memory).

For more details, see:
- [WebAssembly Memory docs (MDN)](https://developer.mozilla.org/en-US/docs/WebAssembly/Memory)

## Notable projects using WebAssembly

Some widely-known projects using WebAssembly include:

| Project | Description |
|---------|-------------|
| [JupyterLite](https://jupyterlite.readthedocs.io/en/latest/) | Brings Jupyter notebooks to the browser |
| [Pyodide](https://pyodide.org/en/stable/) | Runs Python in the browser |
| [TensorFlow.js](https://www.tensorflow.org/js) | Machine learning in JavaScript |
| [ONNX Runtime Web](https://onnxruntime.ai/docs/) | Portable model execution |
| [Transformerjs](https://huggingface.co/docs/transformers.js/en/index) | Natural language processing models in JavaScript |

## Resources

https://github.com/rclement/pydata-paris-2025-modelship-demo

## Table of contents

| Module/Link | Description |
|-------------|-------------|
| [Notes on availability](notes-on-availability/index.md) | Information about which standard library modules are available on different platforms and how to check for their presence. |
