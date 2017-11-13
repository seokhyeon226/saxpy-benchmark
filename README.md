# SAXPY GPGPU Benchmark

This contains different implementations of SAXPY (Single Precision A * X Plus Y)
across many backends such as:
 - naive Python loop
 - Python Numpy
 - naive C++ loop
 - C++ CUDA (GPU)
 - OpenCL (both CPU and GPU) 

The implemented SAXPY is basically a single iteration of this loop:

```
  for i=0 to N:
     Y[i] += alpha * X[i]
```

We only measure the time to perform the above loop, and not other things such as 
initialization and data transfers between CPU and GPU.


# Naive Python Loop

This is a naive Python implementation using loop, something like:
```python
  x = [XVAL] * N
  y = [YVAL] * N

  for i in range(N):
      y[i] += AVAL * x[i]
```

Run [saxpy_loop.py](saxpy_loop.py) to see the result.

# Python Numpy

Improved Python version with vectorized Numpy implementation:
```python
  x = np.ones([N]) * XVAL
  y = np.ones([N]) * YVAL

  y += AVAL * x
```

Run [saxpy_numpy.py](saxpy_numpy.py) to see the result. You will need Numpy of course. 


# General C++ Instructions

The C++ codes have been tested on Windows and Mac OS. I assume the instrunctions will be
similar for Linux, but YMMV.

The general requirement is a C++-11 compliant compiler.

The "build system" is basically just a [Makefile](Makefile) which can be executed 
by both `make` or Visual Studio's `nmake`. You'll need to edit the [Makefile](Makefile) manually
to configure things, just follow the instructions in the Makefile.

Once done, run `make` or `nmake` to build the executables.

## Naive C/C++ Loop

This is naive C/C++ loop using CPU:
```c++
static void saxpy(size_t n, real_t a, real_t *x, real_t *y)
{
  for (size_t i = 0; i < n; ++i) {
      y[i] += a * x[i];
  }
}
```
See [saxpy_cpu.cpp](saxpy_cpu.cpp) for the implemention.


# CUDA

CUDA� is a parallel computing platform and programming model developed by NVIDIA for 
general computing on (NVIDIA) graphical processing units (GPGPU). Because NVIDIA is
the market leader in GPU/GPGPU, that makes CUDA the leading API for GPGPU as well and AFAIK
it is the API that is used by pretty much all higher level libraries utilizing GPGPU 
such as TensorFlow and what not.

One of the good thing about CUDA is, if you have a computer from 2008 onwards with an
NVidia GPU on it (such as GeForce 9800 GTX+ or GeForce G102M), chances are you can
use CUDA on it.  

The other good things are it has good API (subjective of course), plenty of documentations,
and good community and forum support.

Some select resources on CUDA:
 - [NVidia CUDA Zone](https://developer.nvidia.com/cuda-zone)
 - [CUDA (Wikipedia)](https://en.wikipedia.org/wiki/CUDA)
 - [Supported GPU (GeForce only)](https://www.geforce.com/hardware/technology/cuda/supported-gpus)
 - [An Even Easier Introduction to CUDA](https://devblogs.nvidia.com/parallelforall/even-easier-introduction-cuda/)


### Building and Running

Source file: [saxpy_cuda.cu](saxpy_cuda.cu)

Requirements: [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads). Make sure `nvcc` and
`nvprof` are available in the PATH of your command prompt.

Configuring: edit the [Makefile](Makefile) and include `saxpy_cuda` in `TARGET` variable
and configure the flags in Step 3 as necessary.

Building: just run `make` or `nmake`

Running: run `nvprof saxpy_cuda`, and you will see the time it takes to execute saxpy in the
output similar to this:
```
==2168== Profiling result:
Time(%)      Time     Calls       Avg       Min       Max  Name
100.00%  7.9757ms         1  7.9757ms  7.9757ms  7.9757ms  saxpy(unsigned __int64, float, float*, float*)
```


# OpenCL

Open Computing Language (OpenCL) is a framework for writing parallel programs in CPUs, GPUs,
DSPs, FPGAs, and other processors or hardware accelerators. So unlike CUDA, OpenCL is available 
across much wider range of platforms, including NVidia hardware as well, and implementations
are available from AMD, Apple, ARM, Creative, IBM, Intel, Nvidia, Samsung, etc. It's even installed
by default on MacOS since MacOS 10.7. So this sounds like a good framework to try.

OpenCL provides both C and C++ API for us. I would very much recommend using the C++
API because it's easier to use though. For comparison, here is [saxpy in C++](saxpy_ocl1.cpp) 
and here is [saxpy in C](saxpy_ocl2.cpp). You can see that C code is about five times longer 
than the C++ one (at least the core C++ code, inside `main`).

Some select resources on OpenCL:
- [OpenCL (Wikipedia)](https://en.wikipedia.org/wiki/OpenCL)
- [A Gentle Introduction to OpenCL (Dr.Dobb's)](http://www.drdobbs.com/parallel/a-gentle-introduction-to-opencl/231002854)
- [OpenCL on Visual Studio : Configuration tutorial for the confused](https://medium.com/@pratikone/opencl-on-visual-studio-configuration-tutorial-for-the-confused-3ec1c2b5f0ca)

### Installation

If you have installed NVidia CUDA SDK, actually it includes OpenCL SDK with it, in its standard
`include` and `lib` directories. So you don't have to download OpenCL SDK separately. Unfortunately,
this only supports NVidia cards, it doesn't support `cpu` target. 

For more comprehensive SDK, you can get [Intel SDK for OpenCL](https://software.intel.com/en-us/intel-opencl),
which is available for Windows and Linux. Note that this is the SDK; you still need to download
the OpenCL drivers for the hardware that you have. For example, the [Intel OpenCL driver](https://software.intel.com/en-us/articles/opencl-drivers)
provides the driver for Intel Core and Xeon processors. I assume drivers for the graphics cards
are available from the manufacturer's website, or perhaps via Windows Update mechanism.  


### Building and Running

Source: I provide two implementations, [saxpy in C++](saxpy_ocl1.cpp) and [saxpy in C](saxpy_ocl2.cpp).

Configuring: edit the [Makefile](Makefile) and include `saxpy_ocl1` and `saxpy_ocl2` in `TARGET` 
variable. Configure the flags in Step 3 as necessary.

Building: just run `make` or `nmake`

Running: running `saxpy_ocl1` or `saxpy_ocl2` without any arguments will run saxpy on default
device (in my case, it's the GPU). You can force it to run on GPU or CPU by giving it `cpu` or
`gpu` argument. 

