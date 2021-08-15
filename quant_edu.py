import numpy as np
import math


class Bond():
    def __init__(self,
                 mat_years,
                 coupon_rate,
                 coupon_freq,
                 principal=1):
        self.mat_years = mat_years
        self.coupon_rate = coupon_rate
        self.principal = principal
        if isinstance(coupon_freq, str):
            if coupon_freq.lower() == 'a':
                self.coupon_freq = 1
            elif coupon_freq.lower() == 's':
                self.coupon_freq = 0.5
            elif coupon_freq.lower() == 'q':
                self.coupon_freq = 0.25
            else:
                raise Exception(f'[{coupon_freq}] coupon_freq not recognized!')
        else:
            self.coupon_freq = coupon_freq
    
    def get_current_yield(self, quoted_price):
        return self.coupon_rate / quoted_price
    
    def pv_irr(self, x):
        # Used in the irr solver. x is the interest rate
        pv = 0
        t_sched = np.arange(0, self.mat_years + self.coupon_freq, self.coupon_freq)
        for i in t_sched:
            pv += self.principal * (self.coupon_rate * self.coupon_freq) * math.exp(-i * x)
        pv += self.principal * math.exp(-t_sched[-1] * x)
        return pv
    
    def solve_irr(self, x_min, x_max, target_y, rel_tol=1e-04):
        x_mid = x_min + ((x_max - x_min) / 2)
        max_res = self.pv_irr(x_min)
        min_res = self.pv_irr(x_max)
        mid_res = self.pv_irr(x_mid)
        if math.isclose(target_y,mid_res, rel_tol=rel_tol):
            return x_mid
        elif target_y > mid_res and target_y < max_res:
            res = self.solve_irr(x_min, x_mid, target_y)
        elif target_y < mid_res and target_y > min_res:
            res = self.solve_irr(x_mid, x_max, target_y)
        return res
    
    def get_ytm(self, quoted_price):
        return self.solve_irr(0, 1, quoted_price)

if __name__ == '__main__':
    b = Bond(10, 0.06, 'S')
    irr = b.get_ytm(0.96)
