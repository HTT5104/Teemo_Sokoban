# Teemo_Sokoban
Sokoban with Teemo theme

I. Cách chạy và thống kê:
1. Mở folder từ GitHub trên VSC.
2. cd Sokoban_with_Teemo\Sources
3. pyinstrument main.py
4. Sau khi kết thúc chương trình sẽ xem đưọc dung lượng tiêu tốn và thời gian chạy.
5. Thống kê 2 thông tin trên chỉ của file chứa thuật toán (BFS_Search, AStar_Search, BestFS_Search).
6. Thống kê thêm 2 thông tin state visited và step.
7. Tổng hợp ra file excel

II. Đối chiếu level và map
1 = 1
2 = 10
3 = 11
4 = 12
5 = 13
6 = 14
7 = 15
8 = 16
9 = 17
10 = 18
11 = 19
12 = 2
13 = 20
14 = 3
15 = 4
16 = 5
17 = 6
18 = 7
19 = 8
20 = 9

III. Báo cáo:
1. Làm bằng Latex
2. Chia mục:
    1. Giới thiệu chung
        1.1. Bài toán
            1.1.1. Mục tiêu (Trạng thái đích)
            - Di chuyển nhân vật để đẩy thùng sao cho toàn bộ thùng được đẩy vào điểm đích.
            - Di chuyển nhân vật Teemo để đẩy cây nấm vào các vị trí bụi cây.
            1.1.2. Thành phần
            - Nhân vật (Teemo): Đối tượng được điều khiển.
            - Tường (Turret): Không thể đi lên trên hay dẩy thùng lên trên tường.
            - Thùng (Cây nấm): Đối tượng được nhân vật tác động.
            - Điểm đích (Bụi cây): Vị trí mà thùng cần được đẩy tới.
            1.1.3. Toán tử
            - Đi lên.
            - Đi xuống.
            - Đi sang trái.
            - Đi sang phải.
            1.1.4. Trạng thái thất bại
            Thùng có ít nhất hai cạnh liền kề bị chặn.
            - Thùng nằm trong góc tường.
            - Hai thùng đặt cạnh nhau sát tường.

        1.2. Thuật toán
            1.2.1. Tìm kiếm mù
            Breadth First Search.
            1.2.2. Tìm kiếm heuristic:
            - A Star.
            - Best First Search.

    2. Thiết kế chương trình
        2.1. Cấu trúc dữ liệu
        |STT|       Tên         | Dạng  |
        | 1 | state             | state |
        | 2 | heuristic_queue   | heap  |
        | 3 | list_can_move     | list  |

        2.2. Thuật toán
            2.2.1. Breadth First Search
            2.2.2. A Star
            2.2.3. Best First Search
        2.3. Mẫu thử
        2.4. Giao diện
    
    3. Thống kê
        3.1. Thời gian
        3.2. Bộ nhớ
        3.3. Số bước
            3.3.1. Số trạng thái đã duyệt
            3.3.2. Số trạng thái sử dụng