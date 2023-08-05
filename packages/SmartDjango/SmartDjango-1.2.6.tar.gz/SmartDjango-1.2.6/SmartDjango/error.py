class EInstance:
    def __init__(self, e, append_msg=None):
        self.e = e
        self.append_msg = append_msg
        if (e.ph == ETemplate.PH_FORMAT or e.ph == ETemplate.PH_S) and isinstance(append_msg, str):
            self.append_msg = (append_msg,)

    def __str__(self):
        return 'EInstance of %s, %s' % (self.e, self.append_msg)


class ETemplate:
    """
    错误类，基类
    """
    _id = 0  # 每个错误实例的唯一ID

    PH_NONE = 0
    PH_FORMAT = 1
    PH_S = 2

    def __init__(self, msg, ph=PH_NONE):
        """
        错误类构造函数
        :param msg: 错误的中文解释
        :param ph: placeholder格式
        """
        self.msg = msg
        self.ph = ph
        self.eid = ETemplate._id

        ETemplate._id += 1

    def __call__(self, append_msg=None):
        return EInstance(self, append_msg or [])

    def __str__(self):
        return 'Error %s: %s' % (self.eid, self.msg)

    def dictor(self):
        from SmartDjango import Param
        return Param.dictor(self, ['msg', 'eid'])


ET = ETemplate
E = ET


class ErrorCenter:
    d = dict()
    reversed_d = dict()

    @staticmethod
    def get(k):
        return ErrorCenter.d.get(k)

    @staticmethod
    def r_get(eid):
        return ErrorCenter.reversed_d.get(eid)

    @staticmethod
    def all():
        _dict = dict()
        for item in ErrorCenter.d:
            _dict[item] = ErrorCenter.d[item].dictor()
        return _dict

    @classmethod
    def register(cls):
        for k in cls.__dict__:
            if k[0] != '_':
                e = getattr(cls, k)
                if isinstance(e, ETemplate):
                    if k in ErrorCenter.d:
                        raise AttributeError('conflict error identifier %s' % k)
                    ErrorCenter.d[k] = e
                    ErrorCenter.reversed_d[e.eid] = k


class BaseError(ErrorCenter):
    OK = ETemplate("没有错误")
    FIELD_VALIDATOR = ETemplate("字段校验器错误")
    FIELD_PROCESSOR = ETemplate("字段处理器错误")
    FIELD_FORMAT = ETemplate("字段格式错误")
    RET_FORMAT = ETemplate("函数返回格式错误")
    MISS_PARAM = ETemplate("缺少参数{0}", ET.PH_FORMAT)


BaseError.register()
