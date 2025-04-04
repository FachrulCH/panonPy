from panonpy.panonpy import PanonPy


def test_simple_test():
    comparer = PanonPy()
    result = comparer.compare_images(
        '/Users/fachrulch/py/panonpy/tests/visualtest/keduax.png',
        '/Users/fachrulch/py/panonpy/tests/visualtest/baseline/pertamax.png',
        diff_path='/Users/fachrulch/py/panonpy/tests/visualtest/diff.png',
        threshold=0.01
    )

    if result:
        print("Images are similar within the threshold.")
    else:
        print("Images are different beyond the threshold.")