# Auto Vote Tool

Tool tự động bình chọn bàn thắng đẹp trên Vietfootball.vn

## Cài đặt

1. Cài đặt Python 3.7 trở lên
2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Chạy chương trình:
```bash
python auto_vote.py
```

2. Nhập số lượng bình chọn bạn muốn thực hiện
3. Chương trình sẽ tự động:
   - Tạo tên ngẫu nhiên
   - Tạo số điện thoại Việt Nam hợp lệ
   - Thực hiện bình chọn
   - Hiển thị kết quả và tiến độ

## Lưu ý

- Chương trình sẽ tự động delay ngẫu nhiên 1-3 giây giữa các lần bình chọn để tránh bị phát hiện
- Mỗi lần bình chọn sẽ sử dụng User-Agent khác nhau
- Số điện thoại được tạo theo đúng định dạng số điện thoại Việt Nam #   t o o l - b i n h - c h o n  
 