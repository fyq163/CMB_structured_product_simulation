# CMB_structured_product_simulation
> This repository is a backup of my codes of a tool that simulates the return of structured products based on the CMB index. The tool is used to evaluate the performance of the structured products by CMB specifically.
> 
> 本repo仅用于备份我编写的一个基于CMB指数的结构化产品回报模拟工具的代码。该工具用于预测招商银行指数结构化产品的表现。
> 

## Quick Start
### Install 
write installation guide  here
```
Short steps to build a .pyd from your pybind11 C++ project on Windows (Miniconda env):

Prepare environment
Install pybind11 and CMake in the conda env: conda activate py9
pip install pybind11 cmake
Make sure Visual Studio Build Tools (MSVC) for your Python bitness (x64) are installed.
Use an MSVC developer shell (or Developer PowerShell for VS) so msbuild is available, then run:
Where the .pyd ends up
For the Visual Studio generator the produced file is typically at: build/Release/cmb_structured_valuation.pyd
Copy that .pyd into a folder on Python’s sys.path (e.g. your package folder or site-packages of the env), or add build/Release to PYTHONPATH for testing.
Quick import test:
Notes / gotchas

Match bitness: if your Python is 64-bit, build x64. Use the matching Visual Studio generator (-A x64).
Remove or avoid -static in CMake if you get link errors with Python runtime.
If CMake cannot find Python/pybind11, pass -DPython3_ROOT_DIR or use pip-installed pybind11 and ensure CMake can find it.
If you prefer a single-command alternative, use scikit-build / setuptools + pybind11 and run python setup.py build_ext --inplace.
If you want, I can give an adjusted CMake command line tuned to your enviroment
# 从 build 输出复制到包目录（项目根中运行）
copy .\sv_wrap\cpp_source\build\Release\cmb_structured_valuation.pyd .\sv_wrap\structured_simulation\

# 或复制到当前 conda env site-packages
copy .\sv_wrap\cpp_source\build\Release\cmb_structured_valuation.pyd "C:\Users\Administrator\miniconda3\envs\py9\Lib\site-packages\"
# 在激活的 py9 环境中测试导入
python -c "import sys; print(sys.version); import cmb_structured_valuation as m; print('loaded', m)"
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
