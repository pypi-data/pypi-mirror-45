#工程数学库
#共三大模块,基础数学/统计学/物理学
from ctypes import CDLL,string_at
#嵌入式数据库,存放数学模型,C语言配置数据和哈希转换函数
import sqlite3

from platform import system
os_=system()
#默认
dll = CDLL('math.dll')
if os_=="Linux":
    dll = CDLL('math.so')

class MATH:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        pass

    def define(self,x):
        define_c=dll.define_c()
        define_c=ctp(define_c)
        return eval(define_c)

    def sin(self,x):
        sin_c = ctp(dll.sin_c())
        return eval(sin_c)

    def cos(self,x):
        cos_c = ctp(dll.cos_c())
        return eval(cos_c)

    def tan(self,x):
        tan_c = ctp(dll.tan_c())
        return eval(tan_c)

    def get_solution(self,f,x):
        get_solution_c=ctp(dll.get_solution_c())
        return eval(get_solution_c)

    def get_limit(self,f,x,num):
        get_limit_c=ctp(dll.get_limit_c())
        return eval(get_limit_c)
    #求偏导数
    def get_derivative(self,f,x):
        get_derivative_c=ctp(dll.get_derivative_c())
        return eval(get_derivative_c)
    #定积分,不定积分
    def get_integration(self,f,x):
        get_integration_c=ctp(dll.get_integration_c())
        return eval(get_integration_c)
    #级数展开
    def get_series(self,f, x, point, order):
        get_series_c=ctp(dll.get_series_c())
        return eval(get_series_c)

    def e(self):
        e_c=ctp(dll.e_c())
        return eval(e_c)

    def i(self):
        i_c=ctp(dll.i_c())
        return eval(i_c)

    def pi(self):
        pi_c=ctp(dll.pi_c())
        return eval(pi_c)

class STATISTICS:
    def __init__(self):
        pass

class PHYSICS:
    def __init__(self):
        pass

db="math.db"
def ctp(c):
    p=string_at(c,-1).decode()
    return p
math=MATH(db)
exec(ctp(dll.header_c()))