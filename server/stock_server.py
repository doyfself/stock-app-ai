import http.server
import socketserver
import json
import urllib.parse
import stock_api as sa
import get_data_from_xueqiu as xq
import selection_api as sla
import stock_review_api as sra
import stock_line_api as slia
import market_analysis_api as maa

ROUTES = {
    "/search": sa.query_stock_by_word,
    "/kline": xq.get_stock_data,
    "/stock_details": xq.get_stock_details,
    "/get_selection_detail": xq.get_selection_details,
    "/get_selection": sla.get_selection,  # 获取自选列表
    "/get_selection_remark": sla.get_selection_remark,
    "/add_selection": sla.add_selection,  # 添加自选
    "/update_selection_sort": sla.update_selection_sort,  # 自选排序
    "/delete_selection": sla.delete_selection,  # 删除自选
    "/is_selection_exists": sla.is_selection_exists,  # 检查自选是否存在
    # 自选三省
    "/get_stock_review": sra.get_stock_review,  # 获取自选三省列表
    "/get_single_stock_review": sra.get_single_stock_review,  # 获取自选三省列表
    "/add_stock_review": sra.add_stock_review,  # 添加三省
    "/delete_stock_review": sra.delete_stock_review,  # 删除三省
    # 画线
    "/query_lines": slia.query_lines,
    "/add_line": slia.add_line,
    "/delete_line": slia.delete_line,
    # 大盘分析
    "/get_analysis_info": maa.get_analysis_info,
    "/add_analysis_info": maa.add_analysis_info,
}

# 配置
PORT = 8000  # 服务端口
HOST = "0.0.0.0"  # 允许所有网络接口访问，便于局域网测试


def handle_not_found(query_params):
    """处理未匹配的路径"""
    return {"success": False, "message": "接口不存在"}, 404


class StockHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """处理股票查询请求的HTTP处理器，支持跨域"""

    def _set_headers(self, status_code=200, content_type="application/json"):
        """设置响应头，包含跨域支持"""
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")  # 允许所有域名访问
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
        )
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
            response_data = {"success": False, "error": str(e)}
            status_code = 500
        # 处理可能没有状态码的情况
        if isinstance(response_data, tuple):
            response_data, status_code = response_data

        # 返回响应
        self._set_headers(status_code)
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        """处理POST请求"""
        # 解析URL
        parsed_url = urllib.parse.urlparse(self.path)

        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        request_body = {}
        if content_length > 0:
            body = self.rfile.read(content_length).decode("utf-8")
            # 尝试解析JSON格式
            try:
                request_body = json.loads(body)
            except json.JSONDecodeError:
                # 解析失败时尝试解析表单数据
                request_body = urllib.parse.parse_qs(body)
                # 转换为普通字典（去除列表包装）
                request_body = {k: v[0] for k, v in request_body.items()}

        # 解析查询参数
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 查找路由对应的处理函数
        handler = ROUTES.get(parsed_url.path, handle_not_found)

        # 执行处理函数并获取响应
        try:
            # 同时传递查询参数和请求体给处理器
            response_data, status_code = handler(query_params, request_body), 200
        except Exception as e:
            response_data = {"success": False, "error": str(e)}
            status_code = 500
        # 处理可能没有状态码的情况
        if isinstance(response_data, tuple):
            response_data, status_code = response_data

        # 返回响应
        self._set_headers(status_code)
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))


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
