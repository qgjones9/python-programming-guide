# [Python C API Reference Manual](https://docs.python.org/3/c-api/index.html)

This manual documents the API used by C and C++ programmers who want to write extension modules or embed Python. It is a companion to [Extending and Embedding the Python Interpreter](https://docs.python.org/3/extending/index.html), which describes the general principles of extension writing but does not document the API functions in detail.

## Table of Contents

Mirrors the [Python 3 C API reference](https://docs.python.org/3/c-api/index.html). Each heading links to a stub page in this repo; the stub H1 links to the canonical docs.

## [Introduction](introduction/index.md)

### [Language version compatibility](introduction/language-version-compatibility/index.md)

### [Coding standards](introduction/coding-standards/index.md)

### [Include Files](introduction/include-files/index.md)

### [Useful macros](introduction/useful-macros/index.md)

### [Objects, Types and Reference Counts](introduction/objects-types-and-reference-counts/index.md)

### [Exceptions](introduction/exceptions/index.md)

### [Embedding Python](introduction/embedding-python/index.md)

### [Debugging Builds](introduction/debugging-builds/index.md)

### [Recommended third party tools](introduction/recommended-third-party-tools/index.md)

## [C API Stability](c-api-stability/index.md)

### [Unstable C API](c-api-stability/unstable-c-api/index.md)

### [Stable Application Binary Interface](c-api-stability/stable-application-binary-interface/index.md)

### [Platform Considerations](c-api-stability/platform-considerations/index.md)

### [Contents of Limited API](c-api-stability/contents-of-limited-api/index.md)

## [The Very High Level Layer](the-very-high-level-layer/index.md)

### [Available start symbols](the-very-high-level-layer/available-start-symbols/index.md)

### [Stack Effects](the-very-high-level-layer/stack-effects/index.md)

## [Reference Counting](reference-counting/index.md)

## [Exception Handling](exception-handling/index.md)

### [Printing and clearing](exception-handling/printing-and-clearing/index.md)

### [Raising exceptions](exception-handling/raising-exceptions/index.md)

### [Issuing warnings](exception-handling/issuing-warnings/index.md)

### [Querying the error indicator](exception-handling/querying-the-error-indicator/index.md)

### [Signal Handling](exception-handling/signal-handling/index.md)

### [Exception Classes](exception-handling/exception-classes/index.md)

### [Exception Objects](exception-handling/exception-objects/index.md)

### [Unicode Exception Objects](exception-handling/unicode-exception-objects/index.md)

### [Recursion Control](exception-handling/recursion-control/index.md)

### [Exception and warning types](exception-handling/exception-and-warning-types/index.md)

### [Tracebacks](exception-handling/tracebacks/index.md)

## [Defining Extension Modules](defining-extension-modules/index.md)

### [Multiple module instances](defining-extension-modules/multiple-module-instances/index.md)

### [Initialization function](defining-extension-modules/initialization-function/index.md)

### [Multi-phase initialization](defining-extension-modules/multi-phase-initialization/index.md)

### [Legacy single-phase initialization](defining-extension-modules/legacy-single-phase-initialization/index.md)

## [Utilities](utilities/index.md)

### [Operating System Utilities](utilities/operating-system-utilities/index.md)

### [System Functions](utilities/system-functions/index.md)

### [Process Control](utilities/process-control/index.md)

### [Importing Modules](utilities/importing-modules/index.md)

### [Data marshalling support](utilities/data-marshalling-support/index.md)

### [Parsing arguments and building values](utilities/parsing-arguments-and-building-values/index.md)

### [String conversion and formatting](utilities/string-conversion-and-formatting/index.md)

### [Character classification and conversion](utilities/character-classification-and-conversion/index.md)

### [PyHash API](utilities/pyhash-api/index.md)

### [Reflection](utilities/reflection/index.md)

### [Codec registry and support functions](utilities/codec-registry-and-support-functions/index.md)

### [PyTime C API](utilities/pytime-c-api/index.md)

### [Support for Perf Maps](utilities/support-for-perf-maps/index.md)

## [Abstract Objects Layer](abstract-objects-layer/index.md)

### [Object Protocol](abstract-objects-layer/object-protocol/index.md)

### [Call Protocol](abstract-objects-layer/call-protocol/index.md)

### [Number Protocol](abstract-objects-layer/number-protocol/index.md)

### [Sequence Protocol](abstract-objects-layer/sequence-protocol/index.md)

### [Mapping Protocol](abstract-objects-layer/mapping-protocol/index.md)

### [Iterator Protocol](abstract-objects-layer/iterator-protocol/index.md)

### [Buffer Protocol](abstract-objects-layer/buffer-protocol/index.md)

## [Concrete Objects Layer](concrete-objects-layer/index.md)

### [Fundamental Objects](concrete-objects-layer/fundamental-objects/index.md)

### [Numeric Objects](concrete-objects-layer/numeric-objects/index.md)

### [Sequence Objects](concrete-objects-layer/sequence-objects/index.md)

### [Container Objects](concrete-objects-layer/container-objects/index.md)

### [Function Objects](concrete-objects-layer/function-objects/index.md)

### [Other Objects](concrete-objects-layer/other-objects/index.md)

### [C API for Extension Modules](concrete-objects-layer/c-api-for-extension-modules/index.md)

## [Interpreter Initialization and Finalization](interpreter-initialization-and-finalization/index.md)

### [Before Python initialization](interpreter-initialization-and-finalization/before-python-initialization/index.md)

### [Global configuration variables](interpreter-initialization-and-finalization/global-configuration-variables/index.md)

### [Initializing and finalizing the interpreter](interpreter-initialization-and-finalization/initializing-and-finalizing-the-interpreter/index.md)

### [Cautions regarding runtime finalization](interpreter-initialization-and-finalization/cautions-regarding-runtime-finalization/index.md)

### [Process-wide parameters](interpreter-initialization-and-finalization/process-wide-parameters/index.md)

## [Thread States and the Global Interpreter Lock](thread-states-and-the-global-interpreter-lock/index.md)

### [Detaching the thread state from extension code](thread-states-and-the-global-interpreter-lock/detaching-the-thread-state-from-extension-code/index.md)

### [Non-Python created threads](thread-states-and-the-global-interpreter-lock/non-python-created-threads/index.md)

### [Legacy API](thread-states-and-the-global-interpreter-lock/legacy-api/index.md)

### [Cautions about fork()](thread-states-and-the-global-interpreter-lock/cautions-about-fork/index.md)

### [High-level APIs](thread-states-and-the-global-interpreter-lock/high-level-apis/index.md)

### [GIL-state APIs](thread-states-and-the-global-interpreter-lock/gil-state-apis/index.md)

### [Low-level APIs](thread-states-and-the-global-interpreter-lock/low-level-apis/index.md)

## [Asynchronous Notifications](asynchronous-notifications/index.md)

## [Operating System Thread APIs](operating-system-thread-apis/index.md)

## [Synchronization Primitives](synchronization-primitives/index.md)

### [Python critical section API](synchronization-primitives/python-critical-section-api/index.md)

### [Legacy locking APIs](synchronization-primitives/legacy-locking-apis/index.md)

## [Thread-Local Storage Support](thread-local-storage-support/index.md)

### [Thread-specific storage API](thread-local-storage-support/thread-specific-storage-api/index.md)

### [Dynamic allocation](thread-local-storage-support/dynamic-allocation/index.md)

### [Methods](thread-local-storage-support/methods/index.md)

### [Legacy APIs](thread-local-storage-support/legacy-apis/index.md)

## [Multiple Interpreters in a Python Process](multiple-interpreters-in-a-python-process/index.md)

### [A per-interpreter GIL](multiple-interpreters-in-a-python-process/a-per-interpreter-gil/index.md)

### [Bugs and caveats](multiple-interpreters-in-a-python-process/bugs-and-caveats/index.md)

### [High-level APIs](multiple-interpreters-in-a-python-process/high-level-apis/index.md)

### [Low-level APIs](multiple-interpreters-in-a-python-process/low-level-apis/index.md)

### [Advanced debugger support](multiple-interpreters-in-a-python-process/advanced-debugger-support/index.md)

## [Profiling and Tracing](profiling-and-tracing/index.md)

## [Reference Tracing](reference-tracing/index.md)

## [Python Initialization Configuration](python-initialization-configuration/index.md)

### [PyInitConfig C API](python-initialization-configuration/pyinitconfig-c-api/index.md)

### [Configuration Options](python-initialization-configuration/configuration-options/index.md)

### [Runtime Python configuration API](python-initialization-configuration/runtime-python-configuration-api/index.md)

### [PyConfig C API](python-initialization-configuration/pyconfig-c-api/index.md)

### [Py_GetArgcArgv()](python-initialization-configuration/py-getargcargv/index.md)

### [Delaying main module execution](python-initialization-configuration/delaying-main-module-execution/index.md)

## [Memory Management](memory-management/index.md)

### [Overview](memory-management/overview/index.md)

### [Allocator Domains](memory-management/allocator-domains/index.md)

### [Raw Memory Interface](memory-management/raw-memory-interface/index.md)

### [Memory Interface](memory-management/memory-interface/index.md)

### [Object allocators](memory-management/object-allocators/index.md)

### [Default Memory Allocators](memory-management/default-memory-allocators/index.md)

### [Customize Memory Allocators](memory-management/customize-memory-allocators/index.md)

### [Debug hooks on the Python memory allocators](memory-management/debug-hooks-on-the-python-memory-allocators/index.md)

### [The pymalloc allocator](memory-management/the-pymalloc-allocator/index.md)

### [The mimalloc allocator](memory-management/the-mimalloc-allocator/index.md)

### [tracemalloc C API](memory-management/tracemalloc-c-api/index.md)

### [Examples](memory-management/examples/index.md)

## [Object Implementation Support](object-implementation-support/index.md)

### [Allocating objects on the heap](object-implementation-support/allocating-objects-on-the-heap/index.md)

### [Object Life Cycle](object-implementation-support/object-life-cycle/index.md)

### [Common Object Structures](object-implementation-support/common-object-structures/index.md)

### [Type Object Structures](object-implementation-support/type-object-structures/index.md)

### [Supporting Cyclic Garbage Collection](object-implementation-support/supporting-cyclic-garbage-collection/index.md)

## [API and ABI Versioning](api-and-abi-versioning/index.md)

### [Build-time version constants](api-and-abi-versioning/build-time-version-constants/index.md)

### [Run-time version](api-and-abi-versioning/run-time-version/index.md)

### [Bit-packing macros](api-and-abi-versioning/bit-packing-macros/index.md)

## [Monitoring C API](monitoring-c-api/index.md)

## [Generating Execution Events](generating-execution-events/index.md)

### [Managing the Monitoring State](generating-execution-events/managing-the-monitoring-state/index.md)
