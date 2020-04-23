from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import constants
from flask import current_app, jsonify, make_response
from ihome.utils.response_code import RET


# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>


@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    前端去获取图片验证码
    :param image_code_id :图片验证码编号
    :return: 正常情况返回——验证码图片 异常——抛出错误信息JSON
    """
    # 提取参数
    # 检验参数
    # 业务逻辑处理
    # 生成验证码图片
    # 名字 真实文本 图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中， 设置有效期
    # redis: 字符串 列表 哈希 set
    # "key" : xxx
    # 使用哈希维护有效期的时候只能整体设置
    # image_codes: ["", "" , ""]

    # 单条维护记录，选用字符串
    # "image_code_编号" : "真实值"
    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    # 将两步融合成一步  设置值 设置有效期
    try:
        # redis_store.set("image_code_%s" % image_code_id, text)
        # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        print("-----------------------", text)
    except Exception as e:
        # 捕获异常 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码失败")

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
