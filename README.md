# Japanese Text to LaTeX IPA/Pinyin Converter

[![Build Status](https://travis-ci.org/your-username/your-repository.svg?branch=master)](https://travis-ci.org/your-username/your-repository)

## 日语文本转LaTeX国际音标/拼音转换器

这个仓库的功能是将日语转换为国际音标（IPA）或拼音，并以LaTeX格式输出。输出格式为`\anno{日语单词}{对应的国际音标}`。这种格式配合TexStudio可以渲染逐词IPA对照的日语文本，方便学习。

This repository provides a tool to convert Japanese text into International Phonetic Alphabet (IPA) or Pinyin, formatted for LaTeX. The output format is `\anno{Japanese word}{Corresponding IPA}`. This format works seamlessly with TexStudio to render Japanese text with word-by-word IPA annotations, facilitating language learning.


![示例](示例.png)

Example Image: `示例.png`


This repository utilizes `https://github.com/ku-nlp/jumanpp` for Japanese Kanji to Kana conversion.

该仓库使用`https://github.com/ku-nlp/jumanpp`进行日语汉字到假名的转换。

This Python code has two modes of operation:

该python代码有两种运行模式：

1. Interactive mode: Input a word and get the corresponding IPA or Pinyin.
   交互模式：输入单词，然后输出对应的IPA或拼音。
2. File mode: Automatically imports content from `input.txt` in the current directory, converts it, and outputs the result to `output.txt`.
   文件模式：自动导入当前目录下的`input.txt`中的内容，转换后导入到`output.txt`中。


## Juman++ Installation Instructions / Juman++安装教程

Below are the instructions for installing Juman++, a morphological analyzer used by this project.

以下是juman++的安装教程，juman++是本项目使用的形态分析器。

### Step 1: Install Necessary Tools and Dependencies / 步骤一：安装必要的工具和依赖

1. **Install Visual Studio 2017 or later / 安装 Visual Studio 2017 或更新版本**
   - Download and install [Visual Studio](https://visualstudio.microsoft.com/) (Community Edition recommended. Ensure the "Desktop development with C++" workload is selected during installation to include the necessary compiler and tools).
2. **Install CMake / 安装 CMake**
   - Download and install [CMake](https://cmake.org/download/). Ensure that CMake is added to the system `PATH` during installation.
3. **Install pre-compiled protobuf library (Optional) / 安装预编译的 protobuf 库（可选）**
   - If needed, install `libprotobuf` and `protobuf-compiler` via [vcpkg](https://github.com/microsoft/vcpkg):
     ```bash
     git clone https://github.com/microsoft/vcpkg.git
     cd vcpkg
     .\bootstrap-vcpkg.bat
     .\vcpkg.exe install protobuf
     ```

### Step 2: Download Pre-trained Model / 步骤二：下载预训练模型

1. Go to the [Juman++ Releases page](https://github.com/ku-nlp/jumanpp/releases).
2. Download the latest source package.
3. Extract the source package (twice) to the E: drive, for example, `E:\jumanpp-2.0.0-rc4\`.

### Step 3: Configuration and Build / 步骤三：配置和构建

1. **Create a build directory / 创建构建目录**
   ```bash
   mkdir build
   cd build
   ```
2. **Run CMake configuration / 运行 CMake 配置**

In the build directory, run using a newer version of PowerShell [https://github.com/PowerShell/PowerShell/releases] (preferably as administrator):

   ```bash
   cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=E:\jumanpp
   ```
   - **Explanation / 说明**:
     - `-DCMAKE_BUILD_TYPE=Release`: Optimizes the build for performance.
     - `-DCMAKE_INSTALL_PREFIX`: Specifies the installation path. Here it is set to `E:\jumanpp`, which you can change as needed.

3. **Compile and install / 编译和安装**

In the `E:\jumanpp-2.0.0-rc4\build` directory, find the generated `jumanpp.sln` file and open it with Visual Studio.

* **Select Build Configuration / 选择编译配置**: In the second menu bar at the top of Visual Studio, make sure the "Release" configuration is selected, not the default "Debug" configuration, to optimize performance.
* **Build Solution / 编译解决方案**: In the first menu bar at the top, select "Build" > "Build Solution," or press Ctrl + Shift + B. Wait for the compilation process to complete. After compilation, the generated binary files will be located in the `E:\jumanpp` directory.


### Step 4: Configure Environment Variables / 步骤四：配置环境变量

Add the Juman++ installation directory to the system `PATH` so that the `jumanpp` command can be used in any command prompt. For example:

将 Juman++ 的安装目录添加到系统 `PATH` 中，以便在任何命令提示符下使用 `jumanpp` 命令。例如：

`E:\jumanpp-2.0.0-rc4\build\src\jumandic\Release\`

and

`E:\jumanpp-2.0.0-rc4\model\`

