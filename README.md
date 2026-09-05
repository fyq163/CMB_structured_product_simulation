# CMB_structured_product_simulation
> This repository is a backup of my codes of a tool that simulates the return of structured products based on the CMB index. The tool is used to evaluate the performance of the structured products by CMB specifically.
> 
> 本repo仅用于备份我编写的一个基于CMB指数的结构化产品回报模拟工具的代码。该工具用于预测招商银行指数结构化产品的表现。

## 安装指南 / Installation Guide

### 前置要求 / Prerequisites

在开始之前，您需要安装以下工具和依赖：

Before you begin, you need to install the following tools and dependencies:

#### 1. Python 环境 / Python Environment
- **Python 3.9+** (推荐使用 Python 3.9 或更高版本 / Recommended: Python 3.9 or higher)
- 可以使用 Anaconda 或 Miniconda 来管理 Python 环境

```bash
# 创建虚拟环境（推荐）
conda create -n cmb_sim python=3.9
conda activate cmb_sim
```

#### 2. pybind11
pybind11 是用于 C++ 和 Python 互操作的库。

pybind11 is a library for seamless operability between C++ and Python.

```bash
# 使用 pip 安装
pip install pybind11

# 或使用 conda 安装
conda install -c conda-forge pybind11
```

#### 3. CMake (3.10+)
CMake 是跨平台的构建工具。

CMake is a cross-platform build tool.

```bash
# Windows - 使用 Chocolatey
choco install cmake

# 或从官网下载：https://cmake.org/download/

# Linux (Ubuntu/Debian)
sudo apt-get install cmake

# macOS
brew install cmake

# 或使用 conda
conda install cmake
```

#### 4. 构建工具 / Build Tools

**Windows:**
- **MinGW-w64** (推荐用于 Windows)
  ```bash
  # 使用 conda 安装
  conda install -c conda-forge m2w64-toolchain
  
  # 或从官网下载：https://www.mingw-w64.org/
  ```
- **Ninja** (可选，推荐使用以加快编译速度)
  ```bash
  # 使用 conda 安装
  conda install -c conda-forge ninja
  
  # 或使用 pip
  pip install ninja
  ```
- 或者使用 **Visual Studio 2017+** 及其 C++ 构建工具

**Linux:**
- **GCC** (通常已预装)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install build-essential
  
  # CentOS/RHEL
  sudo yum groupinstall "Development Tools"
  ```
- **Ninja** (可选)
  ```bash
  sudo apt-get install ninja-build
  ```

**macOS:**
- **Xcode Command Line Tools**
  ```bash
  xcode-select --install
  ```
- **Ninja** (可选)
  ```bash
  brew install ninja
  ```

### 安装步骤 / Installation Steps

#### 第一步：克隆仓库 / Step 1: Clone the Repository

```bash
git clone https://github.com/fyq163/CMB_structured_product_simulation.git
cd CMB_structured_product_simulation
```

#### 第二步：安装 Python 依赖 / Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt

# 或者直接安装核心依赖 / Or install core deps only
pip install numpy pandas sqlalchemy seaborn pybind11
```

可选依赖 / Optional dependencies:
- `arch`：仅 `garch1_1_volatility_forecast` 需要（`pip install arch`）
- `ProcssFunc`：外部模块，不在 PyPI；仅 `calc_trade_days_2_maturity` 需要

- `arch`: only for `garch1_1_volatility_forecast` (`pip install arch`)
- `ProcssFunc`: external module, not on PyPI; only for `calc_trade_days_2_maturity`

#### 第三步：构建 C++ 扩展模块 / Step 3: Build the C++ Extension Module

C++ 扩展模块位于 `cpp_source` 目录中，使用 pybind11 将 C++ 代码编译为 Python 可调用的 `.pyd` (Windows) 或 `.so` (Linux/macOS) 文件。

The C++ extension module is located in the `cpp_source` directory and uses pybind11 to compile C++ code into Python-callable `.pyd` (Windows) or `.so` (Linux/macOS) files.

**配置 CMakeLists.txt / Configure CMakeLists.txt**

在构建之前，需要修改 `cpp_source/CMakeLists.txt` 文件，设置您的 Python 环境路径：

Before building, modify the `cpp_source/CMakeLists.txt` file to set your Python environment paths:

```cmake
# 示例：根据您的环境修改这些路径
set(Python3_ROOT_DIR "/path/to/your/python/env")
set(CMAKE_PREFIX_PATH "/path/to/your/python/env/lib/site-packages/pybind11/share/cmake/pybind11")
set(Python3_INCLUDE_DIR "/path/to/your/python/env/include")
set(Python3_LIBRARY "/path/to/your/python/env/libs/python39.lib")  # Windows (python310.lib for 3.10, python311.lib for 3.11, etc.)
# set(Python3_LIBRARY "/path/to/your/python/env/lib/libpython3.9.so")  # Linux (adjust version number as needed)
set(Python3_EXECUTABLE "/path/to/your/python/env/python.exe")  # Windows
# set(Python3_EXECUTABLE "/path/to/your/python/env/bin/python")  # Linux/macOS
```

> **注意 / Note:** 如果您使用的是 Python 3.10、3.11 或其他版本，请相应地调整库文件名（例如 `python310.lib`、`libpython3.10.so` 等）。
> 
> If you're using Python 3.10, 3.11, or another version, adjust the library filenames accordingly (e.g., `python310.lib`, `libpython3.10.so`, etc.).

**使用 CMake 构建 / Build with CMake**

```bash
# 进入 cpp_source 目录
cd cpp_source

# 创建构建目录
mkdir build
cd build

# 配置 CMake（使用 Ninja 生成器，推荐）
cmake .. -G Ninja

# 或者使用默认生成器
cmake ..

# 编译
cmake --build .

# 或者使用 ninja 直接编译
ninja
```

**Windows (MSVC) / Visual Studio generator**

在 **x64 Native Tools / Developer PowerShell for VS** 中构建，并匹配 Python 位数（通常 x64）：

Build inside an **x64 Native Tools / Developer PowerShell for VS** shell, matching your Python bitness (usually x64):

```bash
cd cpp_source
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

构建产物位置 / Output locations:
- Ninja / MinGW: 通常在 `cpp_source/build/cmb_structured_valuation.pyd`（或 `.so`）
- Visual Studio: 通常在 `cpp_source/build/Release/cmb_structured_valuation.pyd`

Ninja/MinGW usually writes `cmb_structured_valuation.pyd` (or `.so`) under `cpp_source/build/`. Visual Studio usually writes it under `cpp_source/build/Release/`.

#### 第四步：复制生成的文件 / Step 4: Copy the Generated File

将生成的 `.pyd` 或 `.so` 文件复制到 `structured_simulation` 目录中：

Copy the generated `.pyd` or `.so` file to the `structured_simulation` directory:

```bash
# Windows (Ninja/MinGW output in build/)
copy cmb_structured_valuation.pyd ../../structured_simulation/

# Windows (MSVC / Visual Studio Release output)
copy Release\cmb_structured_valuation.pyd ..\..\structured_simulation\

# Linux/macOS
cp cmb_structured_valuation.so ../../structured_simulation/
```

#### 第五步：安装包（可选）/ Step 5: Install the Package (Optional)

> **重要 / Important:** 根目录 `setup.py` **不会**编译 C++ 扩展；它只打包已经存在的 `*.pyd`（目前未声明 `*.so`）。请先完成上面的构建与复制步骤，再安装包。
>
> Root `setup.py` does **not** build the C++ extension; it only packages an existing `*.pyd` (and currently does not declare `*.so`). Build and copy the extension first, then install the package.

```bash
# 返回项目根目录
cd ../..

# 以开发模式安装（推荐）— 仅安装 Python 包装层，不触发 pybind11 构建
# Editable install (recommended) — installs the Python wrapper only; does not trigger a pybind11 build
pip install -e .

# 或者直接安装
pip install .
```

## 快速开始 / Quick Start

### 使用生成的 .pyd 文件 / Using the Generated .pyd Files

`.pyd` (Windows) 或 `.so` (Linux/macOS) 文件是 Python 扩展模块，可以像普通 Python 模块一样导入使用。这些文件通过 pybind11 将 C++ 代码封装，提供高性能的计算能力。

`.pyd` (Windows) or `.so` (Linux/macOS) files are Python extension modules that can be imported like regular Python modules. These files wrap C++ code through pybind11 to provide high-performance computation.

> **重要提示 / Important Note:** 
> 
> `structured_simulation/wraps.py` 含硬编码路径（用于寻找运行时 DLL / `.pyd`）。若 `import structured_simulation` 失败，请检查该路径，或把扩展文件放到包目录 / `sys.path` 中，也可直接 `import cmb_structured_valuation`。
> 
> `structured_simulation/wraps.py` contains a hardcoded path used to locate runtime DLLs / the `.pyd`. If `import structured_simulation` fails, adjust that path, place the extension on `sys.path` / in the package folder, or `import cmb_structured_valuation` directly.
> 
> `ProcssFunc` / `arch` 已改为惰性导入，不再挡住基础鲨鱼鳍 API。
> `ProcssFunc` / `arch` are lazy-imported and no longer block the core shark-fin APIs.

### 基本用法 / Basic Usage

#### 1. 导入模块 / Import the Module

```python
import structured_simulation as ss
import numpy as np
import pandas as pd
```

#### 2. 生成价格路径 / Generate Price Paths

使用蒙特卡洛模拟生成股票价格路径：

Generate stock price paths using Monte Carlo simulation:

```python
# 生成价格路径
# mu: 收益率均值, sigma: 波动率, n_steps: 模拟步数, T: 年化交易日, n_s: 模拟次数
price_path = ss.price_path_simulation(
    mu=0.0249,      # 年化收益率
    sigma=0.2,      # 年化波动率
    n_steps=125,    # 产品天数
    T=252,          # 年化交易日数
    n_s=10000       # 模拟次数
)
```

#### 3. 计算双向鲨鱼鳍收益 / Calculate Dual Shark Fin Returns

双向鲨鱼鳍结构化产品是一种常见的结构化产品类型，具有上下双向敲出机制。

Dual shark fin structured products are common with both upper and lower knock-out barriers.

```python
# 计算双向鲨鱼鳍结构化产品的期望收益
# 注意：C++ 实现的函数名为 two_way_shark_fin，Python 包装函数为 dual_shark_fin
results = ss.dual_shark_fin(
    price_path=price_path,
    high_price_trigger=1.15,   # 敲出上限（115%）
    low_price_threshold=0.85,  # 敲出下限（85%）
    k1=0.0185,                 # 敲出后固定收益率（默认值）
    k2=0.0165,                 # 未敲出基础收益率
    participate_rate=0.2612    # 参与率
)

# 输出统计结果
print(f"平均收益率: {np.mean(results):.4f}")
print(f"收益率标准差: {np.std(results):.4f}")
print(f"最小收益率: {np.min(results):.4f}")
print(f"最大收益率: {np.max(results):.4f}")
```

#### 4. 计算单向鲨鱼鳍收益 / Calculate One-Way Shark Fin Returns

单向鲨鱼鳍产品包括看涨（long）和看跌（short）两种类型。

One-way shark fin products include call (long) and put (short) variants.

```python
# 看涨鲨鱼鳍 / Call shark fin (long)
results_long = ss.py_one_way_shark_fin(
    price_path=price_path,
    direction='long',          # 方向：看涨
    high_price_trigger=1.15,   # 敲出上限
    low_price_threshold=0.85,  # 保护下限
    k1=0.02,                   # 基础收益率
    k3=0.01,                   # 敲出后收益率
    participate_rate=0.5       # 参与率
)

# 看跌鲨鱼鳍 / Put shark fin (short)
results_short = ss.py_one_way_shark_fin(
    price_path=price_path,
    direction='short',         # 方向：看跌
    high_price_trigger=1.15,   # 保护上限
    low_price_threshold=0.85,  # 敲出下限
    k1=0.02,                   # 基础收益率
    k3=0.01,                   # 敲出后收益率
    participate_rate=0.5       # 参与率
)

print(f"看涨平均收益: {np.mean(results_long):.4f}")
print(f"看跌平均收益: {np.mean(results_short):.4f}")
```

#### 5. 完整示例 / Complete Example

```python
import structured_simulation as ss
import numpy as np

# 生成价格路径
price_path = ss.price_path_simulation(
    mu=0.0249,      # 年化收益率
    sigma=0.2,      # 年化波动率
    n_steps=125,    # 产品天数
    T=252,          # 年化交易日数
    n_s=10000       # 模拟次数
)

# 双向鲨鱼鳍（最常用）
# k1 参数（敲出后固定收益率）默认为 0，在不需要敲出收益时可以省略
# Note: k1 parameter (knock-out fixed return) defaults to 0, can be omitted when knock-out return is not needed
results_dual = ss.dual_shark_fin(
    price_path, 
    high_price_trigger=1.15, 
    low_price_threshold=0.85,
    k2=0.0165,
    participate_rate=0.2612
)

# 输出结果
print(f"双向鲨鱼鳍期望收益 / Dual Shark Fin Expected Return: {np.mean(results_dual):.4%}")
print(f"收益率标准差 / Standard Deviation: {np.std(results_dual):.4%}")
```

### 可用函数列表 / Available Functions

本项目提供以下主要函数：

This project provides the following main functions:

1. **`price_path_simulation(mu, sigma, n_steps, T, n_s)`**
   - 生成蒙特卡洛价格路径 / Generate Monte Carlo price paths
   - 返回 numpy array，形状为 (n_steps+1, n_s)
   - Returns numpy array with shape (n_steps+1, n_s)

2. **`dual_shark_fin(price_path, high_price_trigger, low_price_threshold, k1=0, k2=0.0165, participate_rate=0.2612)`**
   - 计算双向鲨鱼鳍产品收益 / Calculate dual shark fin returns
   - 内部调用 C++ 实现的 `two_way_shark_fin` 函数
   - Internally calls C++ `two_way_shark_fin` function
   - **默认值注意 / Defaults differ from C++:** Python wrapper uses `k1=0`, `participate_rate=0.2612`; C++ `two_way_shark_fin` defaults are `k1=0.0185`, `participate_rate=0.1002`

3. **`py_one_way_shark_fin(price_path, direction, high_price_trigger, low_price_threshold, k1, k3, participate_rate=0.1002)`**
   - 计算单向鲨鱼鳍产品收益 / Calculate one-way shark fin returns
   - `direction`: 'long' (看涨) 或 'short' (看跌) / 'long' (call) or 'short' (put)
   - 内部调用 C++ 实现的 `one_way_shark_fin` 函数
   - Internally calls C++ `one_way_shark_fin` function

4. **`calc_trade_days_2_maturity(start_date, end_date)`** *(可选依赖 ProcssFunc / optional ProcssFunc)*
   - 计算交易日天数 / Calculate trading days
   - 仅调用此函数时才需要外部模块 `ProcssFunc`（不在 PyPI）
   - `ProcssFunc` is required only when calling this function (external, not on PyPI)

5. **`garch1_1_volatility_forecast(log_returns)`** *(可选依赖 arch / optional arch)*
   - GARCH(1,1) 波动率预测 / GARCH(1,1) volatility forecasting
   - 仅调用此函数时才需要 `pip install arch`
   - `arch` is required only when calling this function

### C++ 扩展模块函数 / C++ Extension Module Functions

如果您直接使用 C++ 扩展模块（不通过 Python 包装层），可以调用：

If you use the C++ extension module directly (without Python wrapper layer):

```python
import cmb_structured_valuation as cv

# 直接调用 C++ 函数 / Call C++ functions directly
results = cv.two_way_shark_fin(
    price_path, 
    high_price_trigger=1.15, 
    low_price_threshold=0.85,
    k1=0.0185,
    k2=0.0165,
    participate_rate=0.1002
)

results_one_way = cv.one_way_shark_fin(
    price_path,
    direction='long',
    high_price_trigger=1.15,
    low_price_threshold=0.85,
    k1=0.02,
    k3=0.01,
    participate_rate=0.1002
)
```

### 故障排除 / Troubleshooting

**问题 1：找不到 cmb_structured_valuation 模块**

**Problem 1: Cannot find cmb_structured_valuation module**

确保 `.pyd` 或 `.so` 文件位于 `structured_simulation` 目录中，或者在您的 Python 脚本中添加路径：

Make sure the `.pyd` or `.so` file is in the `structured_simulation` directory, or add the path in your Python script:

```python
import sys
sys.path.append('/path/to/cpp_source/build')  # 添加 .pyd/.so 文件所在路径
```

**问题 2：CMake 找不到 Python 或 pybind11**

**Problem 2: CMake cannot find Python or pybind11**

检查并修改 `CMakeLists.txt` 中的路径设置，确保指向正确的 Python 环境。

Check and modify the path settings in `CMakeLists.txt` to ensure they point to the correct Python environment.

**问题 3：编译时出现 C++17 错误**

**Problem 3: C++17 compilation errors**

确保您的编译器支持 C++17 标准。对于旧版本的 GCC，可能需要更新：

Make sure your compiler supports the C++17 standard. For older versions of GCC, you may need to upgrade:

```bash
# Ubuntu/Debian
sudo apt-get install gcc-9 g++-9
```

**问题 4：ImportError: cannot import name 'ProcssFunc' / No module named 'ProcssFunc'**

**Problem 4: ImportError: cannot import name 'ProcssFunc' / No module named 'ProcssFunc'**

`ProcssFunc` 是**外部模块**（通常不在 PyPI），仅被 `calc_trade_days_2_maturity` 使用（惰性导入）。导入 `structured_simulation` 以及使用 `dual_shark_fin` / `py_one_way_shark_fin` / `price_path_simulation` **不需要**它。只有调用交易日函数时才会报错。

`ProcssFunc` is an **external module** (typically not on PyPI), used only by `calc_trade_days_2_maturity` (lazy import). Importing `structured_simulation` and using `dual_shark_fin` / `py_one_way_shark_fin` / `price_path_simulation` does **not** require it. The error appears only when you call the trading-day helper.

**解决方案 / Solution:**
- 不需要交易日功能：忽略即可，继续用鲨鱼鳍相关函数
- If you do not need trading-day helpers: ignore it and keep using the shark-fin APIs
- 需要该功能：自行安装/配置 `ProcssFunc` 到 Python 路径
- If you need it: install/configure `ProcssFunc` on your Python path yourself

**问题 5：arch 包相关错误**

**Problem 5: arch package related errors**

`arch` 仅被 `garch1_1_volatility_forecast` 惰性导入。其他函数不依赖它。

`arch` is lazily imported only by `garch1_1_volatility_forecast`. Other functions do not depend on it.

```bash
# 需要 GARCH 功能时再安装 / Install only if you need GARCH
pip install arch
```


## 常见产品 Applicable Product
招商的结构化产品利率较高的主要集中在沪深300、中证1000、中证500等指数上。包括单项鲨鱼鳍、双向鲨鱼鳍、价差结构，且产品合同计算方式较为统一
CMB's has varieties of structured product, hooked with CSI300, CSI1000, CSI 500 etc, ranging from one way sharkfin to 

### 1. 沪深300鲨鱼鳍
#### 1.1 双向鲨鱼鳍
![dual_500](https://s3gw.cmbimg.com/mbwebpage-images/504b0828-c0ff-337a-ae2b-64a487a67873_559x800.jpg)
#### 1.2 单向看涨、看跌鲨鱼鳍

### 2.1 中证一千看涨价差结构
CSI1000 call
![1000](https://s3gw.cmbimg.com/mbwebpage-images/5746e7d1-80c9-3f39-b40e-264e4403632f_639x702.jpg)


## docs
### import
```python
import structured_simulation as ss
ss.
```
### 价格生成
生成价格序列

- **price_path**: `Union[np.array, pd.DataFrame]`
- **high_price_trigger**: `float`
  - Knock out price, higher 敲出高限
- **low_price_threshold**: `float`
  - Knock out price, lower 敲出底线
- **k1**: `float`
  - Returns after Knock out 敲出后收益率
- **k2**: `float`
  - Base returns when not Knock out 未敲出基础收益率
- **participate_rate**: `float`
  - 参与率

#### Returns
- **`pd.Dataframe`**
  - 个人习惯返回Dataframe，行数为模拟步数，列数为模拟次数

#### Examples
```python
res = dual_shark_fin(
    price_path, high_price_trigger, low_price_threshold, k2=0.0165,
    participate_rate=0.2612
)
print(res.mean(), res.std())
# Output: (0.021247633780875654, 0.003572758860287444)
```
![PE0516](https://s3gw.cmbimg.com/s/L2x2NjZfdXNlcnByZF9idWNrZXQwMS9zaEltYWdlLzIwMjYwMi9pbWcyNjAyMDQxNDQ5MTMzMzMxLnBuZz9BV1NBY2Nlc3NLZXlJZD1sdjY2X3VzZXJwcmQmRXhwaXJlcz0yNzE2ODcyNTU0JlNpZ25hdHVyZT1hZUQwYiUyRlJsOXRlYTd4cjhNR1hsUm12bUV2RSUzRCZyZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPWZpbGVuYW1lJTNEc2hJbWFnZSUyNTJGMjAyNjAyJTI1MkZpbWcyNjAyMDQxNDQ5MTMzMzMxLnBuZyZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmc=/VjwOYCyRkWkDUCJLSo2NqTi-qPA=/lv66_userprd/0)