import sys,os,datetime
from typing import Union
# Add the directory containing the .pyd file to the system path
sys.path.append(
    r'C:\Users\Administrator\miniconda3\envs\py9\Library\bin'
)
import cmb_structured_valuation as sv

import numpy as np
import pandas as pd
from ProcssFunc import if_tradeday
import ProcssFunc as pf
from arch import arch_model


def dual_shark_fin(
        price_path: np.array, high_price_trigger: float,
        low_price_threshold, k1=0,
        k2=0.0165, participate_rate=0.2612
):
    """
    Simulate a dual shark-fin note returns. 双边鲨鱼鳍的期望收益率
    Parameters
    ----------
    price_path : Union[np. Array,pd.DataFrame]
    high_price_trigger : float
        Kncok out price, higher 敲出高限
    low_price_threshold : float
        Knock out price, lower 敲出底线
    k1 : float
        returns after Knock out 敲出后收益率
    k2 : float
        Base returns when not Knock out未敲出基础收益率
    participate_rate : float
        参与率

    Returns
    -------
    List[float]
        A list of simulated returns
    Examples
    --------
    >>> res = dual_shark_fin(
    ...     np.random.randn(1000,1000),
    ...     high_price_trigger=1.15, low_price_threshold=0.85,
    ...     k2=0.0165,
    ...     participate_rate=0.2612
    ... )
    >>> print(np.mean(res),np.std(res))
    (0.021247633780875654 0.003572758860287444)
        """
    if isinstance(price_path, np.ndarray):
        price_path = price_path
    elif isinstance(price_path, pd.DataFrame):
        price_path = price_path.to_numpy()
    else:
        raise ValueError("price_path should be np.array or pd.DataFrame")

    return sv.two_way_shark_fin(
        price_path, high_price_trigger, low_price_threshold, k1, k2, participate_rate)


def py_one_way_shark_fin(price_path, direction, high_price_trigger, low_price_threshold, k1,
                      k3, participate_rate=0.1002, **kwargs
                      ):
    """

    Parameters
    ----------
    direction : Union['short','long']
        Whether to long or short
    price_path : Union[np. Array,pd.DataFrame]
        Simulated price path
    high_price_trigger : float
        Knock out return in decimal, higher. 敲出高限
    low_price_threshold : float
        Knock out price, lower. 敲出底线
    k1 : float
        Knock out fixed returns. 敲出后收益率
    k3 : float
        Base returns. 未敲出基础收益率
    participate_rate : float
        参与率
    Returns
    -------
    List[float]
        A list of simulated returns

    """
    if isinstance(price_path, np.ndarray):
        price_path = price_path
    elif isinstance(price_path, pd.DataFrame):
        price_path = price_path.to_numpy()
    else:
        raise ValueError("price_path should be np.array or pd.DataFrame")

    return sv.one_way_shark_fin(
        price_path, direction, high_price_trigger, low_price_threshold, k1, k3, participate_rate
    )


def price_path_simulation(mu=0.0249, sigma=0.2, n_steps=125, T=252, n_s=999999):
    """
    Generate price path based on default_rng and normal distribution.
    生成股票价格路径
    Parameters
    ----------
    input_format :
    mu : float
        Mean of log return
    sigma : float
        sigma of log return
    n_steps : days of the product, steps to simulate
    N : int
        number of trading days
    n_s: int
        steps to simulate

    Returns
    -------
    pd.DataFrame
        A list of returns
    """
    price_paths = np.zeros((n_steps + 1, n_s))
    price_paths[0] = 1
    dt = T / n_steps
    for t_ in range(1, n_steps + 1):
        z_ = np.random.default_rng().normal(0, 1, n_s)  # normal distribution rng
        price_paths[t_] = price_paths[t_ - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z_)
    # price_paths = pd.DataFrame(price_paths)
    return price_paths


def calc_trade_days_2_maturity(start_date='20241126', end_date='20241129'):
    """
    Calculate days to maturity
    计算到期日
    Parameters
    ----------
    start_date : str
        Start date '%Y%m%d'
    end_date : str
        End date

    Returns
    -------
    int
        Days to maturity
    """
    dates = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    for date in (start_date + datetime.timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        if pf.if_tradeday(date):
            dates.append(date)
    return len(dates)


def garch1_1_volatility_forecast(log_returns):
    model = arch_model(log_returns, vol='GARCH', p=1, q=1)
    model_fit = model.fit(disp='off')
    forecast = model_fit.forecast(horizon=1, simulations=9999)
    return np.sqrt(forecast.variance.values[-1, :][0])


if __name__ == '__main__':
    print(
        calc_trade_days_2_maturity()
    )
