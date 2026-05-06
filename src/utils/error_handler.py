"""
A股投资组合分析系统 - 错误处理模块
"""
from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger('investment_portfolio')


class APIError(Exception):
    """API自定义错误"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


def handle_api_error(f):
    """API错误处理装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            logger.warning(f"API Error: {e.message}")
            return jsonify({
                'success': False,
                'error': e.message,
                'code': e.code
            }), e.code
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            return jsonify({
                'success': False,
                'error': '数据文件不存在'
            }), 404
        except TimeoutError as e:
            logger.error(f"Timeout: {str(e)}")
            return jsonify({
                'success': False,
                'error': '请求超时，请稍后重试'
            }), 504
        except Exception as e:
            logger.exception(f"Unexpected error in {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': '服务器内部错误'
            }), 500
    return decorated_function
