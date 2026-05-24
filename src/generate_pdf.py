from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "BAO CAO: HOAT DONG CUA THUAT TOAN NONOGRAM SOLVER", border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", '', 10)
        self.cell(0, 10, f"Trang {self.page_no()}", align='C')

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, border=0, align='L', fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", '', 12)
        self.multi_cell(0, 8, body)
        self.ln()
        
    def bullet_point(self, title, body=""):
        self.set_font("Arial", 'B', 12)
        self.cell(5, 8, chr(149)) # bullet char
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        if body:
            self.set_font("Arial", '', 12)
            self.set_x(15)
            self.multi_cell(0, 8, body)
        self.ln(2)

pdf = PDF()
pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")

pdf.add_page()

pdf.chapter_title("1. Tong quan thu vien 'src'")
pdf.chapter_body(
    "Thu vien 'src' chua ma nguon chinh yeu de giai quyet bai toan Nonogram (tim vi tri cac o den/trang dua tren goi y so). "
    "Luong thuc thi chinh bat dau tu 'main.py', ket noi voi 'nonogram_solver.py' dong vai tro la vo boc (wrapper) cho toan bo logic giai ma. "
    "Thuat toan giai ma cot loi nam o 'backtrack.py' (su dung de quy quay lui) va 'logical.py' (su dung ky thuat lan truyen rang buoc - Constraint Propagation de cat tia nhanh). "
    "Su ket hop giua tim kiem (Backtracking), thuat toan Heuristic va suy luan logic (Logic Rules) giup he thong giai bai toan mot cach toi uu va nhanh chong."
)

pdf.chapter_title("2. Cac bien cau truc du lieu quan trong")
pdf.chapter_body(
    "De phuc vu cho thuat toan giai ma, cac cau truc du lieu sau duoc khoi tao va su dung lien tuc trong vong doi cua solver:"
)
pdf.bullet_point("board (Mang 2 chieu M x N):", 
    "Dai dien cho luoi Nonogram. Cac gia tri trong luoi:\n"
    "  *  0: O chua xac dinh (unknown)\n"
    "  *  1: O duoc to den (filled)\n"
    "  * -1: O bi danh dau cheo/trang (cross)"
)
pdf.bullet_point("row_list va col_list:", 
    "Danh sach cac mang chua so luong o den lien tiep tuong ung voi cac goi y (clues) o moi hang va cot. "
    "Vi du: row_list[i] = [2, 3] nghia la hang i co 2 khoi den, khoi dau dai 2 o va khoi sau dai 3 o."
)
pdf.bullet_point("bound (Khong gian gioi han cua cac khoi):", 
    "Day la bien quan trong nhat cho suy luan logic. Mang bound la mang 4 chieu luu tru vi tri bat dau som nhat (start) va ket thuc muon nhat (end) cua moi khoi den.\n"
    "  * bound[0][i][k]: Luu [start, end] cua khoi thu k tren hang i.\n"
    "  * bound[1][j][k]: Luu [start, end] cua khoi thu k tren cot j.\n"
    "Khi thuat toan quet va phat hien cac o da duoc dien, mang bound nay se duoc thu hep lai (start tang len, end giam xuong)."
)
pdf.bullet_point("solutions:", 
    "Mang luu tru cac nghiem hop le (ma tran board hoan chinh) duoc tim thay."
)

pdf.chapter_title("3. Thu tu hoat dong khi chay file 'main.py'")
pdf.chapter_body("Khi khoi chay file 'main.py', luong chuong trinh dien ra tuan tu qua cac buoc sau:")

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 8, "Buoc 1: Nap du lieu va Khoi tao (main.py)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8, 
    "  * Chuong trinh goi utils.load_puzzle() de doc file 'input.txt'.\n"
    "  * Khoi tao doi tuong solver = NonogramSolver().\n"
    "  * Dua du lieu dau vao thong qua solver.set_puzzle(m, n, row_list, col_list)."
)
pdf.ln(3)

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 8, "Buoc 2: Chuan bi bang va gioi han (nonogram_solver.py -> base.py)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8, 
    "  * Trong ham set_puzzle(), ham base.init_board() duoc goi de tao mang toan so 0.\n"
    "  * Ham base.init_bound() duoc goi. No tinh toan vi tri som nhat va muon nhat co the "
    "cua moi khoi dua tren chieu dai cua chung va khoang cach 1 o trong xen giua. Dieu nay tao "
    "ra ranh gioi rang buoc ban dau cho tat ca cac khoi."
)
pdf.ln(3)

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 8, "Buoc 3: Thuat toan giai chinh (main.py -> nonogram_solver.solve -> backtrack.py)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8, 
    "Ham solver.solve() goi ham backtrack() voi trang thai board va bound ban dau. "
    "Tai moi buoc goi de quy trong backtrack, qua trinh sau dien ra:\n\n"
    "  A. Lan truyen Logic - Logical Inference (logical.py):\n"
    "     Thuat toan ap dung lien tiep cac luat logic vao tat ca hang va cot (Rule 1.1, 2.1, 2.2, 3.1, 3.2, 3.3). "
    "Cac luat nay (vi du nhu Overlap, Anchor Propagation) giup tim ra cac o chac chan den hoac trang de dien ngay "
    "va dong thoi thu hep khoang bound cua cac khoi.\n"
    "     Neu cac luat phat hien mau thuan (vi du khoi bi day ra ngoai bang), ham tra ve False, nhanh tim kiem nay bi huy (Cat tia - Pruning).\n\n"
    "  B. Lua chon Heuristic (get_mrv_cell trong backtrack.py):\n"
    "     Neu logic khong the tu giai quyet phan con lai, thuat toan can thu sai (guess). "
    "No dung ham get_mrv_cell (Minimum Remaining Values) de uu tien chon o trong "
    "nam tren hang va cot dang co it o trong (chua xac dinh) nhat. Chon o nay giup phat hien loi som nhat va thu hep khong gian tim kiem hieu qua.\n\n"
    "  C. Thu nghiem - Branching:\n"
    "     Thuat toan tao ra hai ban sao moi cua board va bound. Ban sao thu nhat thu dat o da chon la -1 (trang) va goi lai backtrack. "
    "Ban sao thu hai dat o do la 1 (den) va goi lai backtrack."
)
pdf.ln(3)

pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 8, "Buoc 4: Trich xuat va in ket qua (main.py)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 8, 
    "  * Neu backtrack dien day bang va kiem tra (check) thanh cong, ket qua duoc luu vao solutions.\n"
    "  * main.py kiem tra so luong solutions, in ma tran cua nghiem dau tien ra terminal qua print_board(), "
    "va neu duoc bat, se dung Pygame (visualizer.show) de mo phong hinh anh."
)

pdf.output("Bao_cao_Nonogram_Solver.pdf")
print("Bao_cao_Nonogram_Solver.pdf created successfully.")
