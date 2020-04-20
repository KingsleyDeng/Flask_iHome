# coding:utf-8
import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = "SFXFDKJdfsf092"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACE_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 对cookie中的session_id进行隐藏数理
    SESSION_USE_SIGNER = True
    # session 数据的有效期 单位：秒
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境 配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}
