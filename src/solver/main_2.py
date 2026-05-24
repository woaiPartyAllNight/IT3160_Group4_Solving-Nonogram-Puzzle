import sys
import io
from pathlib import Path

# Thêm thư mục gốc vào path để giải quyết vấn đề import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Cấu hình encoding để in được tiếng Việt trên console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from solver.nonogram_solver import NonogramSolver
from solver.utils import load_puzzle, visualizer

def print_board(board):
    """Hàm in bảng Nonogram ra màn hình terminal"""
    if not board:
        print("Không có dữ liệu bảng.")
        return
    for row in board:
        print("".join(['#' if cell == 1 else '.' if cell == -1 else ' ' for cell in row]))

def main():
    # Sử dụng đường dẫn tuyệt đối để tìm file input.txt cạnh file main.py hoặc nhận từ đối số dòng lệnh
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        input_file = Path(sys.argv[1]).resolve()
    else:
        input_file = Path(__file__).resolve().parent / "input.txt"

    # Cho phép ghi đè thời gian chạy (timeout) từ tham số dòng lệnh (nếu có)
    # Ví dụ: --timeout 20
    time_limit = 60
    if "--timeout" in sys.argv:
        try:
            idx = sys.argv.index("--timeout")
            time_limit = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            pass

    # Kiểm tra xem có tắt chế độ trực quan hóa (Pygame) hay không
    use_visualize = "--no-visualize" not in sys.argv

    print(f"[*] Đang tải dữ liệu bài toán từ: {input_file}")
    try:
        m, n, row_list, col_list = load_puzzle(input_file)
        print(f"[*] Kích thước bảng: {m}x{n}")
    except FileNotFoundError:
        print(f"[!] Lỗi: Không tìm thấy file '{input_file}'. Vui lòng tạo file này.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Lỗi khi đọc file: {e}")
        sys.exit(1)
            
    # Khởi tạo solver
    solver = NonogramSolver()
    
    try:
        solver.set_puzzle(m, n, row_list, col_list)
    except Exception as e:
        print(f"[!] Cấu hình bài toán không hợp lệ: {e}")
        sys.exit(1)
        
    # Khởi tạo cửa sổ trực quan hóa nếu được bật
    if use_visualize:
        visualizer.init_puzzle(m, n, row_list, col_list)
        visualizer.record_step(solver.board)

    print("[*] Bắt đầu giải mã...")
    success = solver.solve(time_limit=time_limit, visualize=use_visualize)
    
    # In kết quả
    if success:
        solutions = solver.get_all_solutions()
        print(f"\n[+] Thành công! Tìm thấy {len(solutions)} nghiệm.")
        print("[+] Kết quả nghiệm đầu tiên:")
        print_board(solver.get_solution())
    else:
        print("\n[-] Không tìm thấy nghiệm nào hoặc đã vượt quá thời gian giới hạn.")

    # Hiển thị cửa sổ mô phỏng ở bước cuối cùng
    if use_visualize:
        visualizer.show()

if __name__ == "__main__":
    main()
