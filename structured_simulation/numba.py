# -*- coding: utf-8 -*-
# this is experimental to see if numba can replace cpp accelerated code for structured product simulation
import numpy as np
from numba import njit


@njit
def two_way_shark_fin(price_path, high_price_trigger, low_price_threshold, k1=0.0185,
                      k2=0.0165, participate_rate=0.1002):
    """
    计算双边鲨鱼鳍的期望收益率
    Parameters
    ----------
    price_path : ndarray
        模拟价格路径
    high_price_trigger : float
        敲出高限
    low_price_threshold : float
        敲出低限
    k1 : float
        敲出后收益率
    k2 : float
        未敲出基础收益率
    participate_rate : float
        参与率

    Returns
    -------
    ndarray
        期望收益率
    """
    paths = price_path
    n_paths = paths.shape[1]
    k3_yield = np.zeros(n_paths)

    for i in range(n_paths):
        knocked_out = False
        for j in range(paths.shape[0]):
            if paths[j, i] > high_price_trigger or paths[j, i] < low_price_threshold:
                knocked_out = True
                break
        if knocked_out:
            k3_yield[i] = k1
        else:
            k3_yield[i] = k2 + participate_rate * np.abs(paths[-1, i] - 1)

    return k3_yield


@njit
def one_way_shark_fin(price_path, direction, high_price_trigger, low_price_threshold, k1,
                      k3, participate_rate=0.1002):
    """
    计算单边鲨鱼鳍的期望收益率
    Parameters
    ----------
    price_path : ndarray
        模拟价格路径
    direction : str
        多头或者空头，取值 'long' 或 'short'
    high_price_trigger : float
        敲出高限
    low_price_threshold : float
        敲出低限
    k1 : float
        敲出后收益率
    k3 : float
        未敲出基础收益率
    participate_rate : float
        参与率

    Returns
    -------
    ndarray
        期望收益率
    """
    paths = price_path
    n_paths = paths.shape[1]
    final_yield = np.zeros(n_paths)

    for i in range(n_paths):
        lp = paths[-1, i]  # 最后一个价格
        if direction == 'long':
            max_exceeds_trigger = False
            for j in range(paths.shape[0]):
                if paths[j, i] > high_price_trigger:
                    max_exceeds_trigger = True
                    break
            if max_exceeds_trigger:
                final_yield[i] = k3
            elif lp < low_price_threshold:
                final_yield[i] = k1
            else:
                final_yield[i] = k1 + participate_rate * (lp - low_price_threshold)
        else:
            min_exceeds_threshold = False
            for j in range(paths.shape[0]):
                if paths[j, i] < low_price_threshold:
                    min_exceeds_threshold = True
                    break
            if min_exceeds_threshold:
                final_yield[i] = k3
            elif lp > high_price_trigger:
                final_yield[i] = k1
            else:
                final_yield[i] = k1 + participate_rate * (high_price_trigger - lp)

    return final_yield


# Example usage
if __name__ == "__main__":
    price_path = np.array([[1.0, 1.1, 1.2], [1.3, 1.4, 1.5]])
    high_price_trigger = 1.4
    low_price_threshold = 1.0
    k1 = 0.0185
    k2 = 0.0165
    k3 = 0.02
    participate_rate = 0.1002

    two_way_result = two_way_shark_fin(price_path, high_price_trigger, low_price_threshold, k1, k2, participate_rate)
    one_way_result = one_way_shark_fin(price_path, "long", high_price_trigger, low_price_threshold, k1, k3,
                                       participate_rate)

    print("Two-way Shark Fin Result:", two_way_result)
    print("One-way Shark Fin Result:", one_way_result)