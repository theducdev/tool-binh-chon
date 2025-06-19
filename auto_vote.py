from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import random
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
import time
from datetime import datetime
import os
import sys
import glob

def get_chrome_version():
    """Lấy phiên bản Chrome đang cài đặt"""
    try:
        if sys.platform == 'win32':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            version, _ = winreg.QueryValueEx(key, 'version')
            return version
    except:
        pass
    return None

def find_chromedriver():
    """Tìm file chromedriver.exe trong thư mục .wdm"""
    try:
        wdm_dir = os.path.join(os.path.expanduser('~'), '.wdm')
        pattern = os.path.join(wdm_dir, 'drivers', 'chromedriver', 'win64', '*', 'chromedriver-win32', 'chromedriver.exe')
        drivers = glob.glob(pattern)
        if drivers:
            return drivers[0]
    except:
        pass
    return None

def generate_vietnamese_name():
    """Tạo tên người Việt Nam ngẫu nhiên"""
    ho = [
        "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
        "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Đoàn", "Vương", "Trịnh"
    ]
    
    dem = [
        "Văn", "Thị", "Đức", "Hữu", "Đình", "Công", "Quang", "Hoài", "Minh", "Thành",
        "Hồng", "Thanh", "Ngọc", "Hải", "Xuân", "Bá", "Thế", "Kim", "Đăng", "Như",
        "", "", ""  # Thêm tên đệm trống để tăng tỷ lệ tên không có tên đệm
    ]
    
    ten = [
        "An", "Anh", "Bình", "Chi", "Cường", "Dũng", "Dung", "Dương", "Đạt", "Đức",
        "Hà", "Hải", "Hạnh", "Hiếu", "Hoàng", "Hùng", "Hương", "Huệ", "Khánh", "Linh",
        "Long", "Mai", "Minh", "Nam", "Nga", "Nhung", "Phong", "Phương", "Quân", "Quang",
        "Quyên", "Tâm", "Thảo", "Thủy", "Trang", "Trinh", "Trung", "Tú", "Tuấn", "Việt",
        "Xuân", "Yến"
    ]
    
    # Chọn các phần của tên
    ho_selected = random.choice(ho)
    dem_selected = random.choice(dem)
    ten_selected = random.choice(ten)
    
    # Tạo tên đầy đủ, loại bỏ dấu cách thừa
    if dem_selected:  # Nếu có tên đệm
        full_name = f"{ho_selected} {dem_selected} {ten_selected}"
    else:  # Nếu không có tên đệm
        full_name = f"{ho_selected} {ten_selected}"
    
    # Loại bỏ dấu cách thừa và chuẩn hóa dấu cách
    full_name = " ".join(word for word in full_name.split() if word)
    
    return full_name

def generate_phone():
    """Tạo số điện thoại Việt Nam ngẫu nhiên"""
    prefixes = ['086', '096', '097', '098', '032', '033', '034', '035', '036', '037', '038', '039', '088', '091', '094', '083', '084', '085', '081', '082']
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    phone = random.choice(prefixes) + suffix
    try:
        parsed_number = phonenumbers.parse(phone, "VN")
        if phonenumbers.is_valid_number(parsed_number):
            return phone
    except NumberParseException:
        return generate_phone()
    return phone

def setup_driver():
    """Thiết lập trình duyệt Chrome"""
    try:
        # Kiểm tra phiên bản Chrome
        chrome_version = get_chrome_version()
        if chrome_version:
            print(f"Phiên bản Chrome hiện tại: {chrome_version}")
        
        chrome_options = Options()
        ua = UserAgent()
        chrome_options.add_argument(f'user-agent={ua.random}')
        # chrome_options.add_argument('--headless=new')  # Sử dụng headless mới
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        
        # Tìm ChromeDriver đã cài đặt
        existing_driver = find_chromedriver()
        if existing_driver and os.path.exists(existing_driver):
            print(f"Sử dụng ChromeDriver đã cài đặt tại: {existing_driver}")
            service = Service(existing_driver)
        else:
            print("Đang cài đặt ChromeDriver mới...")
            driver_path = ChromeDriverManager().install()
            print(f"ChromeDriver mới được cài đặt tại: {driver_path}")
            service = Service(driver_path)
        
        print("Khởi tạo WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Đã khởi tạo WebDriver thành công!")
        return driver
        
    except Exception as e:
        print(f"Lỗi khi thiết lập ChromeDriver: {str(e)}")
        if "This version of ChromeDriver only supports Chrome version" in str(e):
            print("Lỗi: Phiên bản ChromeDriver không tương thích với phiên bản Chrome.")
            print("Vui lòng cập nhật Chrome lên phiên bản mới nhất và thử lại.")
        return None

def vote():
    """Thực hiện bình chọn"""
    vote_url = "https://vietfootball.vn/danh-muc/detail/binh-chon-ban-thang-dep-nhat-vong-5-hpl-s12"
    
    try:
        driver = setup_driver()
        if driver is None:
            print("Không thể khởi tạo trình duyệt. Vui lòng kiểm tra lại Chrome và ChromeDriver")
            return False
            
        wait = WebDriverWait(driver, 10)
        
        # Tạo thông tin người dùng giả
        name = generate_vietnamese_name()
        phone = generate_phone()
        
        # Truy cập trang bình chọn
        print("Đang truy cập trang bình chọn...")
        driver.get(vote_url)
        time.sleep(random.uniform(2, 4))  # Đợi trang load
        
        try:
            # Đợi form load
            print("Đang đợi form load...")
            form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
            
            # Điền thông tin
            print("Đang điền thông tin...")
            name_input = form.find_element(By.NAME, "name")
            phone_input = form.find_element(By.NAME, "phone")
            
            # Điền từng ký tự với tốc độ ngẫu nhiên để mô phỏng người dùng thật
            for char in name:
                name_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            for char in phone:
                phone_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            print("Đang chọn bàn thắng...")
            # Chọn bàn thắng của Phan Nhật Thành
            goal_select = form.find_element(By.CSS_SELECTOR, "select")
            goal_options = goal_select.find_elements(By.TAG_NAME, "option")
            for option in goal_options:
                if "Phan Nhật Thành" in option.text:
                    option.click()
                    break
            time.sleep(random.uniform(1, 2))
            
            print("Đang gửi bình chọn...")
            # Click nút bình chọn
            submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Bình chọn']")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(random.uniform(0.5, 1))
            submit_button.click()
            
            # Đợi và kiểm tra alert thành công
            try:
                # Đợi alert xuất hiện
                alert = wait.until(EC.alert_is_present())
                alert_text = alert.text
                
                if "Gửi thành công" in alert_text:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] Bình chọn thành công với tên: {name} - SĐT: {phone}")
                    # Chấp nhận alert
                    alert.accept()
                    success = True
                else:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] Alert hiển thị nội dung khác: {alert_text}")
                    alert.accept()
                    success = False
                    
            except:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] Không tìm thấy thông báo thành công")
                success = False
            
        except TimeoutException as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] Không tìm thấy phần tử trên trang: {str(e)}")
            success = False
            
        except Exception as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] Lỗi khi thao tác với trang: {str(e)}")
            success = False
            
        finally:
            print("Đóng trình duyệt...")
            driver.quit()
            return success
            
    except Exception as e:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] Có lỗi xảy ra khi khởi tạo trình duyệt: {str(e)}")
        return False

def main():
    successful_votes = 0
    total_attempts = int(input("Nhập số lượng bình chọn bạn muốn thực hiện: "))
    
    print("\nBắt đầu quá trình bình chọn tự động...")
    print("Mỗi lần bình chọn sẽ cách nhau 1-3 phút để tránh bị phát hiện")
    print("Bạn có thể để chương trình chạy trong background\n")
    
    for i in range(total_attempts):
        if vote():
            successful_votes += 1
        
        if i < total_attempts - 1:  # Không delay sau lần cuối cùng
            delay_time = random.uniform(10, 20)  # Delay 1-3 phút
            minutes = int(delay_time // 60)
            seconds = int(delay_time % 60)
            print(f"Đợi {minutes} phút {seconds} giây cho lần bình chọn tiếp theo...")
            time.sleep(delay_time)
        
        print(f"Tiến độ: {i+1}/{total_attempts} ({successful_votes} thành công)")
    
    print(f"\nKết quả cuối cùng:")
    print(f"Tổng số lần thử: {total_attempts}")
    print(f"Số lần thành công: {successful_votes}")
    print(f"Tỷ lệ thành công: {(successful_votes/total_attempts)*100:.2f}%")

if __name__ == "__main__":
    main() 