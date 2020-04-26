from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store, db
from ihome import constants
from flask import current_app, jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User
from ihome.libs.yuntongxun.sms import CCP
import random


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


# GET /api/v1.0/sms_codes/<mobile>
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 进行校验
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
        # 判断图片验证码是否过期
    if real_image_code is None:
        # 图片验证码没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis图片验证码，防止用户使用同一个验证码
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)


    # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        print(real_image_code, "real_image_code--------------")
        print(image_code, "image_code--------------")
        # 用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在,则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码异常")
    # 发送短信
    try:
        ccp = CCP()
        result = ccp.send_Template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
    # 返回值
    if result == 0:
        # 发送成功
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        return jsonify(errno=RET.THIRDERR, errmsg="第三方系统出现问题")
