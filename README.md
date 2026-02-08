# CMB_structured_product_simulation
> This repository is a backup of my codes of a tool that simulates the return of structured products based on the CMB index. The tool is used to evaluate the performance of the structured products by CMB specifically.
> 
> 本repo仅用于备份我编写的一个基于CMB指数的结构化产品回报模拟工具的代码。该工具用于预测招商银行指数结构化产品的表现。
> 
 ## 常见产品
招商的结构化产品利率较高的主要集中在沪深300、中证1000、中证500等指数上。包括单项鲨鱼鳍、双向鲨鱼鳍、价差结构，且产品合同计算方式较为统一
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
[pep0516](https://s3gw.cmbimg.com/s/L2x2NjZfdXNlcnByZF9idWNrZXQwMS9zaEltYWdlLzIwMjYwMi9pbWcyNjAyMDQxNDQ5MTMzMzMxLnBuZz9BV1NBY2Nlc3NLZXlJZD1sdjY2X3VzZXJwcmQmRXhwaXJlcz0yNzE2ODcyNTU0JlNpZ25hdHVyZT1hZUQwYiUyRlJsOXRlYTd4cjhNR1hsUm12bUV2RSUzRCZyZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPWZpbGVuYW1lJTNEc2hJbWFnZSUyNTJGMjAyNjAyJTI1MkZpbWcyNjAyMDQxNDQ5MTMzMzMxLnBuZyZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmc=/VjwOYCyRkWkDUCJLSo2NqTi-qPA=/lv66_userprd/0)

