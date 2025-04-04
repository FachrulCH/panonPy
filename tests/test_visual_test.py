from panonpy.panonpy import PanonPy


def test_simple_test():
    tester = PanonPy(output_dir='results')

    tester.compare_images(
        actual_image_path='/Users/fachrulch/py/panonpy/tests/resources/actual.png',
        baseline_image_path='/Users/fachrulch/py/panonpy/tests/resources/baseline.png',
        test_name='pertamax_test',
        threshold=0.01
    )