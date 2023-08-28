import flask
import argparse
from web2rss import *
app = flask.Flask(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 增加说明
    parser.description = 'RSS-Full-Text-Generator'
    # 服务设置
    server_group = parser.add_argument_group('server')
    server_group.add_argument('--port', type=int, default=5000, help='server port')
    server_group.add_argument('--host', type=str, default='127.0.0.1')
    # 调试设置
    debug_group = parser.add_argument_group('debug')
    debug_group.add_argument('--debug', type=bool, default=False)
    # 解析参数
    args = parser.parse_args()
    # 启动服务
    app.run(host=args.host, port=args.port, debug=args.debug)