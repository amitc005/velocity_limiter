import os
from filecmp import cmp

from main import main


class TestApp:
    def test_expect_out_file(self):
        input = open(os.getcwd() + "/tests/integration/extra/input.txt")
        expected_output_file = open(os.getcwd() + "/tests/integration/extra/output.txt")
        actual_ouput_file = open(
            os.getcwd() + "/tests/integration/extra/actual_output.txt", "w+"
        )
        try:
            main(input, actual_ouput_file)

        finally:
            input.close()
            expected_output_file.close()
            actual_ouput_file.close()

        assert cmp(
            os.getcwd() + "/tests/integration/extra/output.txt",
            os.getcwd() + "/tests/integration/extra/actual_output.txt",
            shallow=False,
        )
