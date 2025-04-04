from pathlib import Path

import pytest

from panonpy.panonpy import PanonPy


@pytest.fixture
def sample_images():
    base_path = Path(__file__).parent / "resources"
    actual = base_path / "actual.png"
    baseline = base_path / "baseline.png"
    output_dir = Path(__file__).parent / "results"

    output_dir.mkdir(exist_ok=True)

    return actual, baseline, output_dir


def test_identical_images_soft_assertion(sample_images):
    actual, baseline, diff_target = sample_images

    tester = PanonPy(output_dir=diff_target, soft_assertion=True)
    result = tester.compare(
        actual_image_path=str(baseline),
        baseline_image_path=str(baseline),
        test_name='identical_test'
    )
    assert result == 'equal'


def test_different_images_soft_assertion(sample_images):
    actual, baseline, diff_target = sample_images
    tester = PanonPy(output_dir=diff_target, soft_assertion=True)
    result = tester.compare(
        actual_image_path=str(actual),
        baseline_image_path=str(baseline),
        test_name='different_test'
    )
    assert result == 'diff'


def test_different_images_hard_assertion(sample_images):
    actual, baseline, diff_target = sample_images
    tester = PanonPy(output_dir=diff_target, soft_assertion=False)

    with pytest.raises(AssertionError, match="Image comparison failed"):
        tester.compare(
            actual_image_path=str(actual),
            baseline_image_path=str(baseline),
            test_name='hard_fail_test'
        )


def test_auto_approve_baseline(sample_images):
    actual, baseline, diff_target = sample_images

    # Modify actual image
    from PIL import Image, ImageDraw
    img = Image.open(actual)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 30, 30], fill='green')
    img.save(actual)

    tester = PanonPy(output_dir=diff_target, soft_assertion=True, auto_approve=True)
    result = tester.compare(
        actual_image_path=str(actual),
        baseline_image_path=str(baseline),
        test_name='auto_approve_test'
    )
    assert result == 'equal'

def test_different_images_type():
    actual = Path(__file__).parent / "resources" / "baseline.png"
    baseline = Path(__file__).parent / "resources" / "baseline.jpg"
    output_dir = Path(__file__).parent / "results"

    tester = PanonPy(output_dir=output_dir, soft_assertion=True)
    result = tester.compare(
        actual_image_path=str(actual),
        baseline_image_path=str(baseline),
        test_name='different_img_type'
    )
    assert result == 'diff'

def test_different_images_size():
    actual = Path(__file__).parent / "resources" / "actually_smaller.png"
    baseline = Path(__file__).parent / "resources" / "baseline.png"
    output_dir = Path(__file__).parent / "results"

    tester = PanonPy(output_dir=output_dir, soft_assertion=True)
    result = tester.compare(
        actual_image_path=str(actual),
        baseline_image_path=str(baseline),
        test_name='different_img_size'
    )
    assert result == 'diff'