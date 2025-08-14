import http.server
import socketserver
import json
import urllib.parse
from local_api import query_stock_by_word
from online_api import get_kline_data

ROUTES = {
    '/search': query_stock_by_word,
    '/kline': get_kline_data
}

# 配置
PORT = 8000  # 服务端口
HOST = "0.0.0.0"  # 允许所有网络接口访问，便于局域网测试

def handle_not_found(query_params):
    """处理未匹配的路径"""
    return {'success': False, 'message': '接口不存在'}, 404
class StockHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """处理股票查询请求的HTTP处理器，支持跨域"""
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """设置响应头，包含跨域支持"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # 允许所有域名访问
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """处理跨域预检请求"""
        self._set_headers()
    
    def do_GET(self):
        # 解析URL和查询参数
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 查找路由对应的处理函数
        handler = ROUTES.get(parsed_url.path, handle_not_found)
        
        # 执行处理函数并获取响应
        try:
            response_data, status_code = handler(query_params), 200
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            status_code = 500
        # 处理可能没有状态码的情况
        if isinstance(response_data, tuple):
            response_data, status_code = response_data
        
        # 返回响应
        self._set_headers(status_code)
        self.wfile.write(json.dumps(
            response_data, 
            ensure_ascii=False
        ).encode('utf-8'))

def run_server():
    """启动HTTP服务器"""
    # 配置服务器
    with socketserver.TCPServer((HOST, PORT), StockHTTPRequestHandler) as httpd:
        print(f"服务器已启动，地址: http://{HOST}:{PORT}")
        print(f"可用接口:")
        print("按 Ctrl+C 停止服务器")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        
        httpd.server_close()
        print("服务器已停止")
