from get_all_stock import get_and_save_stock_data
from stock_server import run_server

if __name__ == "__main__":
    get_and_save_stock_data();
    run_server()