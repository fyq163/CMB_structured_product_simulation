import numpy as np
import pandas as pd
import learning_structure_valuation as sv





def two_way_shark_fin(price_path, high_price_trigger, low_price_threshold, k1=0.0185,
                      k2=0.0165, participate_rate=0.1002
                      ):
    """
    计算双边鲨鱼鳍的期望收益率
    Parameters
    ----------
    price_path : Union[np. Array,pd.DataFrame]
    high_price_trigger : float
        敲出底线
    low_price_threshold : float
        敲出高限
    k1 : float
        敲出后收益率
    k2 : float
        未敲出基础收益率
    participate_rate : float
        参与率
    n_steps : int
        产品期限
    N : int
        模拟次数

    Returns
    -------


    Examples
    --------
    >>> res = two_way_shark_fin(mu=0.0249, sigma=0.2, high_price_trigger=1.15,
    ...                   low_price_threshold=0.85, k1=0.0185,
    ...                   k2=0.0165 / 100, participate_rate=0.1002,
    ...                   n_steps=125, N=100000)
    ... print(res.mean(),res.std())
    0.021247633780875654 0.003572758860287444
    """
    paths = price_path
    k3_yield = [k1  # 如果敲出：标底收益大于或小于
                if (paths[i] > high_price_trigger).any() or
                   (paths[i] < low_price_threshold).any() else
                k2 + participate_rate * abs(paths.iloc[-1, i] - 1)
                for i in paths]
    return np.array(k3_yield)


def one_way_shar_fin(price_path, direction, high_price_trigger, low_price_threshold, k1,
                     k3, participate_rate=0.1002
                     ):
    """
    生成股票价格路径
    mu: 漂移（平均收益率）
    sigma: 波动率
    T: 总时间（年）
    dt: 时间步长
    N: 模拟路径数量
    Parameters
    ----------
    direction : Union['short','long']
        Whether to long or short
    price_path : Union[np. Array,pd.DataFrame]
        Simulated price path
    high_price_trigger : float
        敲出底线
    low_price_threshold : float
        敲出高限
    k1 : float
        敲出后收益率
    k3 : float
        未敲出基础收益率
    participate_rate : float
        参与率


    """
    paths = price_path
    N = paths.shape[1]
    paths = pd.DataFrame(paths)
    final_yield = np.zeros(N)
    for i in range(len(final_yield)):
        lp = paths.iloc[-1, i]  #last price
        if direction == 'long':
            if paths[i].max() > high_price_trigger:
                # any greater than high_price_trigger
                # then k3 return
                final_yield[i] = k3
            elif lp < low_price_threshold:
                final_yield[i] = k1
            else:
                final_yield[i] = k1 + participate_rate * (
                    (lp - low_price_threshold
                     )
                )
        else:
            if paths[i].min() < low_price_threshold:  # lower bound knock out
                final_yield[i] = k3
            elif lp > high_price_trigger:  # higher bound knock out
                final_yield[i] = k1
            else:
                final_yield[i] = k1 + participate_rate * (
                    (high_price_trigger - lp))
    return final_yield


def one_way_shar_fin_sv(price_path, direction, high_price_trigger, low_price_threshold, k1,):
    """

    mu: 漂移（平均收益率）
    sigma: 波动率
    T: 总时间（年）
    dt: 时间步长
    N: 模拟路径数量
    Parameters
    ----------
    direction : Union['short','long']
        Whether to long or short
    price_path : Union[np. Array,pd.DataFrame]
        Simulated price path
    high_price_trigger : float
        敲出底线
    low_price_threshold : float
        敲出高限
    k1 : float
        敲出后收益率
    k3 : float
        未敲出基础收益率
    participate_rate : float
        参与率

    """
    if not isinstance(price_path,np.array()):
        try:
            price_path = price_path.to_numpy()
        except Exception as e:
            raise ValueError('price_path must be a numpy array')
    sv.one_way_shark_fin(price_path=price_path,
                         direction=direction,
                         high_price_trigger=1.15,)
