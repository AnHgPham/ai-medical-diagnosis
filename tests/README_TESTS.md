# Testing Documentation - AI Medical Diagnosis System

## Tổng Quan

Hệ thống testing được thiết kế để đảm bảo chất lượng và độ tin cậy của ứng dụng AI Medical Diagnosis. Testing bao gồm nhiều cấp độ từ unit tests đến integration tests.

## Cấu Trúc Tests

```
tests/
├── __init__.py                    # Package initialization
├── test_input_validation.py       # Kiểm tra validation dữ liệu đầu vào
├── test_medical_ai_handler.py     # Kiểm tra module AI handler
├── test_data_quality.py           # Kiểm tra chất lượng dữ liệu
├── test_integration.py            # Kiểm tra tích hợp các module
└── README_TESTS.md               # Tài liệu này
```

## Các Loại Tests

### 1. Input Validation Tests (`test_input_validation.py`)

Kiểm tra tính hợp lệ của dữ liệu đầu vào từ người dùng.

**Test Cases:**
- Empty input và whitespace-only input
- Input quá ngắn (< 3 ký tự) và quá dài (> 1000 ký tự)
- Input tiếng Việt và tiếng Anh
- Ký tự đặc biệt và HTML tags
- SQL injection prevention
- Emoji và mixed languages

**Chạy tests:**
```bash
pytest tests/test_input_validation.py -v
```

### 2. Medical AI Handler Tests (`test_medical_ai_handler.py`)

Kiểm tra chức năng của module xử lý AI chẩn đoán.

**Test Cases:**
- Emergency keyword detection
- AI handler initialization
- Normal diagnosis flow
- Emergency diagnosis flow
- Conversation reset
- Error handling
- Response quality

**Chạy tests:**
```bash
pytest tests/test_medical_ai_handler.py -v
```

### 3. Data Quality Tests (`test_data_quality.py`)

Kiểm tra chất lượng dữ liệu và cấu hình hệ thống.

**Test Cases:**
- Emergency keywords coverage và quality
- System prompt structure và content
- Response format consistency
- Conversation flow quality
- Safety checks (no definitive diagnosis, no prescription)
- Medical terminology consistency

**Chạy tests:**
```bash
pytest tests/test_data_quality.py -v
```

### 4. Integration Tests (`test_integration.py`)

Kiểm tra tích hợp giữa các module và luồng hoạt động tổng thể.

**Test Cases:**
- End-to-end diagnosis flow
- Emergency handling flow
- Multi-turn conversation flow
- Module integration
- Error recovery
- Performance benchmarks
- Data flow từ input đến output

**Chạy tests:**
```bash
pytest tests/test_integration.py -v
```

## Cài Đặt

### Yêu Cầu

```bash
pip install pytest pytest-cov
```

### Cài Đặt Dependencies

```bash
cd ai-medical-diagnosis
pip install -r requirements.txt
pip install pytest pytest-cov
```

## Chạy Tests

### Chạy Tất Cả Tests

```bash
pytest tests/ -v
```

### Chạy Tests Theo File

```bash
pytest tests/test_input_validation.py -v
pytest tests/test_medical_ai_handler.py -v
pytest tests/test_data_quality.py -v
pytest tests/test_integration.py -v
```

### Chạy Tests Theo Marker

```bash
# Chỉ chạy unit tests
pytest -m unit -v

# Chỉ chạy integration tests
pytest -m integration -v

# Chỉ chạy validation tests
pytest -m validation -v
```

### Chạy Tests Với Coverage

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

Kết quả coverage sẽ được lưu trong thư mục `htmlcov/`.

### Chạy Tests Cụ Thể

```bash
# Chạy một test class
pytest tests/test_input_validation.py::TestInputValidation -v

# Chạy một test method
pytest tests/test_input_validation.py::TestInputValidation::test_empty_input -v
```

## Kết Quả Mong Đợi

### Test Statistics

- **Total Tests**: ~80+ test cases
- **Coverage Target**: > 80%
- **Pass Rate**: 100% (với mocked API)

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| Input Validation | 20+ | Kiểm tra validation dữ liệu |
| AI Handler | 25+ | Kiểm tra logic AI |
| Data Quality | 20+ | Kiểm tra chất lượng dữ liệu |
| Integration | 15+ | Kiểm tra tích hợp |

## Mocking

Do ứng dụng sử dụng Google Gemini API, các tests sử dụng **mocking** để:

1. **Tránh gọi API thật** - Tiết kiệm quota và tăng tốc độ test
2. **Kiểm soát responses** - Test các trường hợp edge cases
3. **Offline testing** - Không cần internet connection

**Example:**
```python
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_diagnose(mock_model_class, mock_configure):
    # Setup mock
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Test response"
    mock_chat.send_message.return_value = mock_response
    mock_model.start_chat.return_value = mock_chat
    mock_model_class.return_value = mock_model
    
    # Test
    handler = MedicalAIHandler()
    result = handler.diagnose("Test input")
    assert result == "Test response"
```

## Best Practices

### 1. Test Naming

- Test files: `test_<module_name>.py`
- Test classes: `Test<Feature>`
- Test methods: `test_<what_is_being_tested>`

### 2. Test Structure (AAA Pattern)

```python
def test_something():
    # Arrange - Setup
    input_data = "test"
    
    # Act - Execute
    result = function(input_data)
    
    # Assert - Verify
    assert result == expected
```

### 3. Test Independence

Mỗi test phải độc lập, không phụ thuộc vào kết quả của test khác.

### 4. Clear Assertions

```python
# Good
assert len(result) > 0, "Result should not be empty"

# Bad
assert result
```

## Continuous Integration

### GitHub Actions (Future)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### Lỗi Import Module

```bash
# Đảm bảo PYTHONPATH đúng
export PYTHONPATH="${PYTHONPATH}:/path/to/ai-medical-diagnosis"
```

### Lỗi API Key

Tests sử dụng mocking nên không cần API key thật. Nếu gặp lỗi, đảm bảo:
```python
with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
    # Your test code
```

### Lỗi Import Config

Đảm bảo `src/` đã được thêm vào path:
```python
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
```

## Metrics

### Test Coverage Goals

- **Overall**: > 80%
- **Critical modules** (medical_ai_handler): > 90%
- **Config & Utils**: > 70%

### Performance Benchmarks

- **Initialization**: < 1 second
- **Emergency check**: < 0.1 second
- **Full test suite**: < 30 seconds

## Contributing

Khi thêm tính năng mới:

1. **Viết tests trước** (TDD approach)
2. **Đảm bảo coverage** không giảm
3. **Chạy toàn bộ test suite** trước khi commit
4. **Update documentation** nếu cần

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Contact

Nếu có vấn đề về testing, vui lòng tạo issue trên GitHub repository.
