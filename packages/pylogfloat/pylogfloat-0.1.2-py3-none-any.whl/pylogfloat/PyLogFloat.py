__author__ = 'bsennblad'
__all__ = ['pylogfloat', 'PyLogFloat']

import numpy as np
import warnings

@np.vectorize # vectorize is not high performance, but essentially a for loop
def pylogfloat(x):
    """
    Constructs a PyLogFloat from x, or vectorized (via np.vectorize) for each element of x.

    See also: `PyLogFloat`
    """
    return PyLogFloat(x)


class PyLogFloat(object):
    """
    Overloads operators for easy log-space computations.

    Note that complex numbers are NOT used, so negative numbers are unsupported. In other words, this class is
    optimized for probability calculations. Special symbol LOGZERO is used for log(0), as in:
        http://bozeman.genome.washington.edu/compbio/mbt599_2006/hmm_scaling_revised.pdf .
    """
    LOGZERO = float("-inf")
    #warnings.simplefilter("error")
    warnings.filterwarnings("error",message = 'Overflow', category=RuntimeWarning, module='pylogfloat')
    
    def __init__(self, linear=None, log_space=None, log_sign=None):
        """Turns a linear-space float into a log-space float.
           Also possible to give the log_space=log(abs(float)) together with sign of float."""
        self.p = None
        self.sign = None
        if linear is not None:
            if log_space is not None:
                raise ValueError("do not specify both")
            if linear==0:
                self.sign = 0
                self.p = np.float64(0.0) #dummy
            else:
                self.sign = +1 if linear > 0 else -1 if linear < 0 else 0
                self.p = np.log(abs(np.float64(linear)))
        elif log_space is not None:
            if log_sign == None:
                raise ValueError("You need to indicate the sign of the log_space argument")
            self.sign=log_sign
            self.p = np.float64(log_space)
        assert np.isfinite(self.p), "PyLogFloat: Argument to __init__ is not finite (i.e., it's nan or infinite)"

    def copy(self):
        return PyLogFloat(log_space=self.p, log_sign=self.sign)

    def __repr__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return "PyLogFloat(log_space = {:e}, log_sign = {}; linear_space = {:e})".format(self.p if self.sign != 0 else 0, self.sign, self.to_float())

    def __str__(self):
        return repr(self)

    def to_float(self):
        """Returns the linear-space equivalent value of this."""
        if self.sign == 0:
            return 0
        else:
            return np.exp(self.p) * self.sign  

    def __float__(self):
        return self.to_float()


    ## arithetic and assign operators
    def __iadd__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __iadd__ must be a PyLogFloat"
        s = self.sign * q.sign
        if s == 1:
            self.addaslogs(q)
            self.sign = self. sign
        elif s == 0:
            if self.sign == 0:
                self.p = q.p
                self.sign = q.sign
        elif s == -1:
            self.subaslogs(q)
        else:
            raise ValueError("sign product {}*{}={} not in {{-1,0,+1}}".format(self, q,self.sign, q.sign, s))
        return self

    def __isub__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __isub__ must be a PyLogFloat"
        s = self.sign * q.sign
        if s == 1:
            self.subaslogs(q)
        elif s == 0:
            if self.sign == 0:
                self.p = q.p
                self.sign = -q.sign
        elif s == -1:
            if self.sign == 1:
                self.addaslogs(q)
            else:
                self.addaslogs(q)
                self.sign = -1
        else:
            raise ValueError("sign product {}*{}={} not in {-1,0,+1}".format(self, q, self.sign, q.sign, s))
        return self

    def __imul__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __imul__ must be a PyLogFloat"
        self.sign *= q.sign
        if self.sign != 0:
            self.p += q.p
        assert (np.isfinite(self.p)), "PyLogFloat: __imul__ result is not finite (i.e., it's nan or infinite)"
        return self
            
    def __itruediv__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __itruediv__ must be a PyLogFloat"
        if q.sign != 0:
            self.sign *= q.sign
            if self.sign != 0:
                self.p -= q.p
        else:
            raise ValueError("PyLogeFloat: division by zero attempted: {}/{}".format(self, q))    
        assert (np.isfinite(self.p)), "PyLogFloat: __itruediv__ result is not finite (i.e., it's nan or infinite)"
        return self

    ## Pow, exp, log 
    def __ipow__(self, power):
        assert not isinstance(power, PyLogFloat), "PyLogFloat: Argument to __ipow__ must not be a PyLogFloat"
        if self.sign < 0 and power < 1.0:
            raise ValueError("PyLogFloat: {a}**{b} yields complex number -- not supported".format(a=self.to_float(), b=power))
        try:
            self.p *= power
        except RuntimeWarning:
            pass
        assert (np.isfinite(self.p)), "PyLogFloat: __ipow__ result is not finite (i.e., it's nan or infinite)"
        return self

    def __iexp__(self):
        assert np.isfinite(self.to_float())
        try:
            self.p = self.to_float()
        except RuntimeWarning:
            pass
        self.sign = 1
        return self

    
    def __ilog__(self):
        if self.sign <= 0:
            raise ValueError("Can't log a negative number or zero\n")
        else:
            self = PyLogFloat(self.p) 
        return self
        
    ## arithmetic operators
    def __add__(self, q):
        return self.copy().__iadd__(q)
    
    def __sub__(self, q):
        return self.copy().__isub__(q)

    def __mul__(self, q):
        return self.copy().__imul__(q)

    def __truediv__(self, q):
        return self.copy().__itruediv__(q)

    ## Pow, exp, log
    def __pow__(self, power):
        return self.copy().__ipow__(power)

    def exp(self):
        return self.copy().__iexp__()

    
    def log(self):
        return self.copy().__ilog__()


    ## Logial operators
    def __eq__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __eq__ must be a PyLogFloat"
        if self.sign == q.sign:
            return self.p == q.p
        else:
            return False
        
    def __ne__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __ne__ must be a PyLogFloat"
        if self.sign == q.sign:
            return self.p != q.p
        else:
            return True
        
    def __le__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __le__ must be a PyLogFloat"
        if self.sign == q.sign:
            if self.sign == 1:
                return self.p <= q.p
            elif self.sign == 0:
                return True
            else:
                return self.p >= q.p
        else:
            return self.sign <= q.sign

    def __ge__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __ge__ must be a PyLogFloat"
        if self.sign == q.sign:
            if self.sign == 1:
                return self.p >= q.p
            elif self.sign == 0:
                return True
            else:
                return self.p <= q.p
        else:
            return self.sign >= q.sign

    def __lt__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __lt__ must be a PyLogFloat"
        if self.sign == q.sign:
            if self.sign == 1:
                return self.p < q.p
            elif self.sign == 0:
                return False
            else:
                return self.p > q.p
        else:
            return self.sign < q.sign

    def __gt__(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to __gt__ with must be a PyLogFloat"
        if self.sign == q.sign:
            if self.sign == 1:
                return self.p > q.p
            elif self.sign == 0:
                return False
            else:
                return self.p < q.p
        else:
            return self.sign > q.sign

        
    ## std functions
    def abs(self):
        ret = self.copy()
        ret.sign = 1 if self.sign != 0 else 0
        return ret

        
    ## helpers
    def addaslogs(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to add must be a PyLogFloat"
        if self.p > q.p:
            self.p += np.log1p(np.exp(q.p-self.p))
        else:
            self.p = q.p + np.log1p(np.exp(self.p - q.p))
        assert np.isfinite(self.p), "PyLogFloat: addaslog result is not finite (i.e., it's nan or infinite) for\n\t{}\n\t{}".format(self, q)
        return
        
    def subaslogs(self, q):
        assert isinstance(q, PyLogFloat), "PyLogFloat: Argument to add must be a PyLogFloat"
        if self.p > q.p:
#            self.p += np.log1p(- np.exp(q.p-self.p))
            self.p += self.log1mexp(self.p - q.p)
        elif self.p == q.p:
            self.sign = 0
            self.p = np.float64(0.0)
        else:
#            self.p = q.p + np.log1p(- np.exp(self.p - q.p))
            self.p = q.p + self.log1mexp(q.p - self.p)
            self.sign *= -1 
        assert np.isfinite(self.p), "PyLogFloat: subaslog result is not finite (i.e., it's nan or infinite) for\n\t{}\n\t{}".format(self, q)
        return

    ## Conditional use of log1p or exp1m for log value additions and subtractions, following
    ## Martin, M. Accurately Computing log(1 − exp(− |a|)) Assessed by the Rmpfr package Cran, The Comprehensive R Archive Network.
    def log1mexp(self, a):
        if a > np.log(2):
            return np.log1p(-np.exp(-a))
        else:
            return np.log(-np.expm1(-a))
