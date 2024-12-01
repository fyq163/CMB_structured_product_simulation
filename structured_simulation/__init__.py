# my_package/__init__.py

from .wraps import *

if __name__ == '__main__':
    df = price_path_simulation()
    print(type(
        dual_shark_fin(
            df, high_price_trigger=1.15, low_price_threshold=0.85, k1=0.0185, k2=0.0165, participate_rate=0.1002
        )
    ))
