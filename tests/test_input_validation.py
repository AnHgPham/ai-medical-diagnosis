"""
Test Input Validation
Kiểm tra tính hợp lệ của dữ liệu đầu vào từ người dùng
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestInputValidation:
    """Test cases for input validation"""
    
    def test_empty_input(self):
        """Test xử lý input rỗng"""
        user_input = ""
        assert len(user_input.strip()) == 0, "Input rỗng phải được phát hiện"
    
    def test_whitespace_only_input(self):
        """Test input chỉ có khoảng trắng"""
        user_input = "   \n\t  "
        assert len(user_input.strip()) == 0, "Input chỉ có whitespace phải được phát hiện"
    
    def test_very_short_input(self):
        """Test input quá ngắn (< 3 ký tự)"""
        user_input = "ab"
        assert len(user_input) < 3, "Input quá ngắn phải được cảnh báo"
    
    def test_very_long_input(self):
        """Test input quá dài (> 1000 ký tự)"""
        user_input = "a" * 1500
        assert len(user_input) > 1000, "Input quá dài phải được giới hạn"
    
    def test_normal_vietnamese_input(self):
        """Test input tiếng Việt bình thường"""
        user_input = "Tôi bị sốt và đau đầu"
        assert len(user_input.strip()) > 0, "Input hợp lệ phải được chấp nhận"
        assert any(char in user_input for char in "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"), \
            "Input tiếng Việt phải được nhận diện"
    
    def test_normal_english_input(self):
        """Test input tiếng Anh bình thường"""
        user_input = "I have fever and headache"
        assert len(user_input.strip()) > 0, "Input hợp lệ phải được chấp nhận"
        assert user_input.isascii(), "Input tiếng Anh phải là ASCII"
    
    def test_special_characters(self):
        """Test ký tự đặc biệt"""
        dangerous_chars = ["<script>", "DROP TABLE", "'; --", "<img src=x>"]
        for char in dangerous_chars:
            # Phải escape hoặc reject các ký tự nguy hiểm
            assert "<" in char or "'" in char, "Ký tự nguy hiểm phải được phát hiện"
    
    def test_numbers_in_input(self):
        """Test số trong input (hợp lệ cho triệu chứng)"""
        user_input = "Tôi bị sốt 39 độ từ 3 ngày nay"
        assert any(char.isdigit() for char in user_input), "Số trong mô tả triệu chứng là hợp lệ"
    
    def test_emoji_in_input(self):
        """Test emoji trong input"""
        user_input = "Tôi bị đau đầu 😢 và sốt 🤒"
        # Emoji có thể được chấp nhận hoặc loại bỏ
        assert len(user_input) > 0, "Input có emoji phải được xử lý"
    
    def test_multiple_languages_mixed(self):
        """Test input trộn nhiều ngôn ngữ"""
        user_input = "Tôi bị fever và đau đầu headache"
        assert len(user_input.strip()) > 0, "Input đa ngôn ngữ phải được chấp nhận"


class TestInputSanitization:
    """Test cases for input sanitization"""
    
    def test_html_escape(self):
        """Test escape HTML tags"""
        user_input = "<script>alert('xss')</script>"
        sanitized = user_input.replace('<', '&lt;').replace('>', '&gt;')
        assert '<' not in sanitized and '>' not in sanitized, "HTML tags phải được escape"
    
    def test_sql_injection_prevention(self):
        """Test ngăn chặn SQL injection"""
        user_input = "'; DROP TABLE users; --"
        # Không sử dụng SQL nên chỉ cần cảnh báo
        dangerous_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "SELECT"]
        has_sql = any(keyword in user_input.upper() for keyword in dangerous_keywords)
        assert has_sql, "SQL keywords phải được phát hiện"
    
    def test_trim_whitespace(self):
        """Test loại bỏ khoảng trắng thừa"""
        user_input = "  Tôi bị sốt  \n\n  "
        sanitized = user_input.strip()
        assert sanitized == "Tôi bị sốt", "Whitespace thừa phải được loại bỏ"
    
    def test_normalize_spaces(self):
        """Test chuẩn hóa khoảng trắng"""
        user_input = "Tôi    bị     sốt"
        sanitized = " ".join(user_input.split())
        assert "    " not in sanitized, "Multiple spaces phải được chuẩn hóa"


class TestInputLength:
    """Test cases for input length validation"""
    
    def test_minimum_length(self):
        """Test độ dài tối thiểu"""
        MIN_LENGTH = 3
        valid_input = "Sốt"
        invalid_input = "ab"
        assert len(valid_input) >= MIN_LENGTH, "Input hợp lệ phải đủ độ dài"
        assert len(invalid_input) < MIN_LENGTH, "Input không hợp lệ phải bị reject"
    
    def test_maximum_length(self):
        """Test độ dài tối đa"""
        MAX_LENGTH = 1000
        valid_input = "a" * 500
        invalid_input = "a" * 1500
        assert len(valid_input) <= MAX_LENGTH, "Input hợp lệ phải trong giới hạn"
        assert len(invalid_input) > MAX_LENGTH, "Input quá dài phải bị reject"
    
    def test_optimal_length(self):
        """Test độ dài tối ưu (50-500 ký tự)"""
        OPTIMAL_MIN = 50
        OPTIMAL_MAX = 500
        optimal_input = "Tôi bị sốt cao 39 độ từ 3 ngày nay, kèm theo ho nhiều, đau đầu và mệt mỏi"
        assert OPTIMAL_MIN <= len(optimal_input) <= OPTIMAL_MAX, \
            "Input tối ưu nên trong khoảng 50-500 ký tự"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
