from panonpy.file_manager import FileManager
from panonpy.report_manager import ReportManager
from panonpy.visual_comparer import VisualComparer


class PanonPy:
    def __init__(self, output_dir='visual_output', soft_assertion=True, auto_approve=False):
        """
        :param output_dir: Folder to store comparison results
        :param soft_assertion: If True, log differences only. If False, raise AssertionError on differences.
        :param auto_approve: If True, automatically update baseline when images differ.
        """
        self.output_dir = output_dir
        self.soft_assertion = soft_assertion
        self.auto_approve = auto_approve

        FileManager.create_folder(output_dir)
        self.report_manager = ReportManager(output_dir)

    def compare(self, actual_image_path, baseline_image_path, test_name, threshold=0.0):
        """
        Compare two images and generate a report.

        :param actual_image_path: Path to the actual (new) image
        :param baseline_image_path: Path to the baseline (expected) image
        :param test_name: Name of the test case
        :param threshold: Allowed difference threshold (0 to 1)
        :return: result string ('equal', 'diff', or 'baseline')
        """
        # Prepare output file paths
        output_actual = f"{self.output_dir}/{test_name}_actual.png"
        output_baseline = f"{self.output_dir}/{test_name}_baseline.png"
        output_diff = f"{self.output_dir}/{test_name}_diff.png"

        # Copy actual image to output
        FileManager.copy_file(actual_image_path, output_actual)

        # Handle missing baseline
        if not FileManager.validate_image_path(baseline_image_path):
            FileManager.copy_file(actual_image_path, output_baseline)
            self.report_manager.add_result('baseline', test_name, output_actual, output_baseline, None, "Baseline created")
            return 'baseline'

        # Copy baseline image to output
        FileManager.copy_file(baseline_image_path, output_baseline)

        # Compare images
        try:
            comparer = VisualComparer(actual_image_path, baseline_image_path, output_diff)
            diff_percentage = comparer.compare()
            diff_percentage_display = f"{diff_percentage * 100:.2f}%"
        except ValueError as e:
            self.report_manager.add_result('diff', test_name, output_actual, output_baseline, None, f"Error: {str(e)}")
            if not self.soft_assertion:
                raise AssertionError(f"Image comparison failed for {test_name}: {e}")
            return 'diff'

        if diff_percentage <= threshold:
            result = 'equal'
            diff_img = None
            message = f"Similar (diff {diff_percentage_display})"
        else:
            result = 'diff'
            diff_img = output_diff
            message = f"Different (diff {diff_percentage_display})"

            # Save diff image
            comparer.save_diff_image()

            # Handle auto-approve if enabled
            if self.auto_approve:
                FileManager.copy_file(actual_image_path, baseline_image_path)
                result = 'equal'
                diff_img = None
                message += " (Auto approved)"

        # Add result to HTML report
        self.report_manager.add_result(result, test_name, output_actual, output_baseline, diff_img, message)

        # Raise failure if soft_assertion is False and there is a diff
        if result == 'diff' and not self.soft_assertion:
            raise AssertionError(f"Image comparison failed for {test_name}: {message}")

        return result