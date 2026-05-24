import os
import sys
import time
import subprocess
import csv
from pathlib import Path

# Cấu hình encoding để in tiếng Việt chuẩn trên Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình timeout tương ứng cho từng kích thước (giây)
TIMEOUT_CONFIG = {
    "5x5": 5,
    "10x10": 10,
    "15x15": 20,
    "25x25": 60,
    "50x50": 180
}

def get_test_files(size_dir: Path) -> list[Path]:
    """Tìm toàn bộ file test input .txt hợp lệ trong thư mục kích thước."""
    # Kiểm tra xem có thư mục con 'inputs' hay không
    inputs_dir = size_dir / "inputs"
    if inputs_dir.exists() and inputs_dir.is_dir():
        test_files = list(inputs_dir.glob("*.txt"))
    else:
        # Nếu để trực tiếp, quét toàn bộ .txt và loại bỏ file kết quả/solution
        test_files = [
            f for f in size_dir.glob("*.txt")
            if "solution" not in f.name.lower() and "result_summary" not in f.name.lower()
        ]
    # Sắp xếp file theo tên để chạy theo thứ tự đẹp mắt
    test_files.sort(key=lambda x: x.name)
    return test_files

def run_single_test(main_script: Path, test_file: Path, timeout: int) -> tuple[bool, float, str]:
    """Chạy một test case bằng subprocess, đo thời gian và trả về kết quả."""
    cmd = [
        sys.executable,
        str(main_script),
        str(test_file),
        "--no-visualize",
        "--timeout",
        str(timeout)
    ]
    
    start_time = time.perf_counter()
    try:
        # Chạy subprocess và bắt cả stdout/stderr
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='ignore'
        )
        elapsed_time = time.perf_counter() - start_time
        
        # Kiểm tra điều kiện giải thành công
        # 1. Mã lỗi bằng 0 (không bị crash)
        # 2. Đầu ra chuẩn chứa chuỗi báo thành công "[+] Thành công!"
        is_solved = (result.returncode == 0) and ("[+] Thành công!" in result.stdout)
        
        status_msg = "Thành công" if is_solved else "Không giải được"
        if result.returncode != 0:
            status_msg += f" (Lỗi Runtime - Code {result.returncode})"
            
        return is_solved, elapsed_time, status_msg
        
    except subprocess.TimeoutExpired:
        elapsed_time = time.perf_counter() - start_time
        return False, elapsed_time, f"Timeout (Quá {timeout} giây)"
    except Exception as e:
        elapsed_time = time.perf_counter() - start_time
        return False, elapsed_time, f"Lỗi hệ thống: {e}"

def main():
    project_root = Path(__file__).resolve().parent
    test_txt_dir = project_root / "Test-txt"
    main_script = project_root / "src" / "solver" / "main_2.py"
    
    # Kiểm tra sự tồn tại của các thành phần chính
    if not test_txt_dir.exists():
        print(f"[!] Lỗi: Không tìm thấy thư mục test tại '{test_txt_dir}'")
        sys.exit(1)
        
    if not main_script.exists():
        print(f"[!] Lỗi: Không tìm thấy file chạy chính tại '{main_script}'")
        sys.exit(1)

    print("=" * 80)
    print(" BẮT ĐẦU CHƯƠNG TRÌNH ĐÁNH GIÁ HIỆU NĂNG NONOGRAM SOLVER")
    print("=" * 80)
    print(f"[*] Thư mục test: {test_txt_dir}")
    print(f"[*] File thực thi: {main_script}")
    print("-" * 80)

    # Các kích thước cần đánh giá theo thứ tự
    sizes = ["5x5", "10x10", "15x15", "25x25", "50x50"]
    summary_results = []

    for size in sizes:
        size_dir = test_txt_dir / size
        if not size_dir.exists():
            print(f"[!] Cảnh báo: Bỏ qua kích thước '{size}' vì không tìm thấy thư mục.")
            continue
            
        test_files = get_test_files(size_dir)
        total_tests = len(test_files)
        
        if total_tests == 0:
            print(f"[!] Cảnh báo: Không tìm thấy file test nào trong '{size_dir}'")
            continue
            
        timeout = TIMEOUT_CONFIG.get(size, 60)
        print(f"\n[*] Đang xử lý nhóm kích thước: {size} ({total_tests} tests, Timeout: {timeout}s/test)")
        print("-" * 60)
        
        solved_count = 0
        total_solved_time = 0.0
        
        for idx, test_file in enumerate(test_files, 1):
            print(f"  -> [{idx}/{total_tests}] Chạy test: {test_file.name}...", end="", flush=True)
            
            is_solved, elapsed_time, status_msg = run_single_test(main_script, test_file, timeout)
            
            if is_solved:
                solved_count += 1
                total_solved_time += elapsed_time
                print(f" [OK] - Thời gian: {elapsed_time:.3f} giây")
            else:
                print(f" [THẤT BẠI] - Lý do: {status_msg} - Thời gian: {elapsed_time:.3f} giây")
                
        # Tính toán các chỉ số
        success_rate = (solved_count / total_tests) * 100.0 if total_tests > 0 else 0.0
        if solved_count > 0:
            avg_time = total_solved_time / solved_count
            avg_time_str = f"{avg_time:.3f}s"
        else:
            avg_time = None
            avg_time_str = "N/A"
            
        # Gán Ghi chú tự động dựa trên kích thước và kết quả chạy thực tế
        if size == "5x5":
            note = "dễ, chạy ổn định"
        elif size == "10x10":
            note = "trung bình, một số test chậm" if (avg_time and avg_time > 1.5) else "dễ, chạy ổn định"
        elif size == "15x15":
            note = "khó, có test timeout" if success_rate < 100 else "trung bình, chạy ổn định"
        elif size == "25x25":
            note = "khó, có test timeout" if success_rate < 100 else "khó, thời gian chạy lớn"
        elif size == "50x50":
            note = "rất khó, thời gian chạy lớn" if (success_rate < 100 or (avg_time and avg_time > 10.0)) else "rất khó, chạy ổn định"
        else:
            note = "chưa xác định"
            
        summary_results.append({
            "Kích thước": size,
            "Số test": total_tests,
            "Tỉ lệ giải được": f"{success_rate:.1f}%",
            "Thời gian trung bình": avg_time_str,
            "Ghi chú": note
        })
        
    # Ghi kết quả vào file result_summary.csv
    csv_file_path = test_txt_dir / "result_summary.csv"
    headers = ["Kích thước", "Số test", "Tỉ lệ giải được", "Thời gian trung bình", "Ghi chú"]
    
    try:
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in summary_results:
                writer.writerow(row)
        print(f"\n[+] Đã lưu bảng thống kê thành công tại: {csv_file_path}")
    except Exception as e:
        print(f"\n[!] Lỗi khi lưu file CSV: {e}")

    # Hiển thị bảng kết quả đẹp mắt ra màn hình terminal
    print("\n" + "=" * 85)
    print(" BẢNG TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ HIỆU NĂNG SOLVER")
    print("=" * 85)
    print(f"{'Kích thước':<12} | {'Số test':<10} | {'Tỉ lệ giải được':<18} | {'Thời gian trung bình':<22} | {'Ghi chú':<20}")
    print("-" * 85)
    for row in summary_results:
        print(f"{row['Kích thước']:<12} | {row['Số test']:<10} | {row['Tỉ lệ giải được']:<18} | {row['Thời gian trung bình']:<22} | {row['Ghi chú']:<20}")
    print("=" * 85)

if __name__ == "__main__":
    main()
