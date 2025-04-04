# 📸 PanonPy
PanonPy is a simple, modular Python library for visual regression testing by comparing images differences and generating HTML report

✨ Features
- Compare two images (actual vs baseline)
- Auto-generate HTML report with images
- Fail the test if images differ (optional)
- Pytest integration ready
- CLI support (coming soon)

## 📦 Installation
```bash
pip install panonpy
```

## 🚀 How to Use

### Basic Usage
```python
from panonpy.panonpy import PanonPy

# Create a PanonPy instance
tester = PanonPy(output_dir='results', fail=True)

# Compare two images
tester.compare(
    actual_image_path='path/to/home_page_screenshot.png',
    baseline_image_path='path/to/baseline_home_page.png',
    test_name='home_page_test',
    threshold=0.01  # Allow 1% difference
)
```

### Install Development
Make sure you have Poetry installed.
Clone the repository:
```bash
git clone https://github.com/FachrulCH/panonPy.git
cd panonpy
poetry install --with test
```

### Result
- Copies actual, baseline, and diff images into output_dir (default: 'results')
- Generates a VisualTestsResult.html report with:
  - Green rows for identical images
  - Red rows for different images
  - Yellow rows for newly created baselines
  - Clicking an image in the report opens a full-size popup preview