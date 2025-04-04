import os
import shutil
from PIL import Image, ImageChops
import datetime


class PanonPy:
    def __init__(self, output_dir='visual_output', report_name='VisualTestsResult.html', fail=False):
        self.output_dir = output_dir
        self.report_name = report_name
        self.fail = fail
        self.results = {'equal': 0, 'diff': 0, 'baseline': 0}

        os.makedirs(self.output_dir, exist_ok=True)
        self._create_report()

    def compare_images(self, actual_image_path, baseline_image_path, test_name, threshold=0.0):
        """Compare two images and generate output report and images.

        :param actual_image_path: Path to actual (new) image
        :param baseline_image_path: Path to baseline (expected) image
        :param test_name: Name of the test
        :param threshold: Allowed difference threshold (0-1)
        :return: Result ('equal', 'diff', or 'baseline')
        """

        # Create output paths
        output_actual_path = os.path.join(self.output_dir, f'{test_name}_actual.png')
        output_baseline_path = os.path.join(self.output_dir, f'{test_name}_baseline.png')
        output_diff_path = os.path.join(self.output_dir, f'{test_name}_diff.png')

        # Copy actual and baseline images to output folder
        shutil.copyfile(actual_image_path, output_actual_path)

        if not os.path.exists(baseline_image_path):
            # If baseline doesn't exist, copy actual as baseline
            shutil.copyfile(actual_image_path, output_baseline_path)
            self._add_result_to_report('baseline', test_name, output_actual_path, output_baseline_path, None,
                                       "Baseline created")
            print(f"Baseline created for {test_name}")
            return 'baseline'

        shutil.copyfile(baseline_image_path, output_baseline_path)

        # Load images
        with Image.open(actual_image_path) as img_actual, Image.open(baseline_image_path) as img_baseline:
            max_size = (max(img_actual.width, img_baseline.width), max(img_actual.height, img_baseline.height))
            img_actual_max = Image.new('RGB', max_size)
            img_actual_max.paste(img_actual)
            img_baseline_max = Image.new('RGB', max_size)
            img_baseline_max.paste(img_baseline)

            # Save diff image
            diff_pixels_percentage = self._save_differences_image(img_actual_max, img_baseline_max, output_diff_path)

            # Determine result
            if diff_pixels_percentage <= threshold:
                result = 'equal'
                diff_img = None
                message = f'Similar (diff {diff_pixels_percentage:.6f})'
            else:
                result = 'diff'
                diff_img = output_diff_path
                message = f'Different (diff {diff_pixels_percentage:.6f})'

            self._add_result_to_report(result, test_name, output_actual_path, output_baseline_path, diff_img, message)
            print(f"Comparison result for {test_name}: {message}")
            # Fail behavior
            if result == 'diff' and self.fail:
                raise AssertionError(f"Image comparison failed for {test_name}: {message}")

            return result

    def _save_differences_image(self, img1, img2, diff_path):
        """Save differences between two images."""
        diff = ImageChops.difference(img1, img2).convert('L')
        mask = diff.point(lambda x: 255 if x else 0)
        red = Image.new('RGB', img1.size, (255, 0, 0))
        diff_img = Image.composite(red, img1, mask)
        diff_img.save(diff_path)

        total_pixels = img1.width * img1.height
        diff_pixels = sum(1 for pixel in mask.getdata() if pixel != 0)
        return diff_pixels / total_pixels

    def _create_report(self):
        """Create basic HTML report with styles and modal popup for images."""
        report_path = os.path.join(self.output_dir, self.report_name)
        if not os.path.exists(report_path):
            with open(report_path, 'w') as f:
                f.write(f"""<html><head><title>PanonPy Visual Test Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        table {{ width: 100%; border-collapse: collapse; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                        tr.equal {{ background-color: #d4edda; }}
                        tr.diff {{ background-color: #f8d7da; }}
                        tr.baseline {{ background-color: #fff3cd; }}
                        img {{ max-width: 200px; cursor: pointer; transition: 0.3s; }}
                        img:hover {{ opacity: 0.7; }}
                        /* The Modal (background) */
                        .modal {{
                            display: none;
                            position: fixed;
                            z-index: 1;
                            padding-top: 60px;
                            left: 0;
                            top: 0;
                            width: 100%;
                            height: 100%;
                            overflow: auto;
                            background-color: rgba(0,0,0,0.9);
                        }}
                        /* Modal Content (Image) */
                        .modal-content {{
                            margin: auto;
                            display: block;
                            width: 80%;
                            max-width: 700px;
                        }}
                        /* Close Button */
                        .close {{
                            position: absolute;
                            top: 15px;
                            right: 35px;
                            color: #f1f1f1;
                            font-size: 40px;
                            font-weight: bold;
                            transition: 0.3s;
                        }}
                        .close:hover,
                        .close:focus {{
                            color: #bbb;
                            text-decoration: none;
                            cursor: pointer;
                        }}
                    </style>
                    </head><body>
                    <h1>PanonPy Visual Test Report</h1>
                    <p><b>Execution date:</b> {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <table>
                    <thead><tr><th>Test</th><th>Baseline</th><th>Actual</th><th>Diff</th><th>Result</th></tr></thead>
                    <tbody></tbody>
                    </table>

                    <!-- The Modal -->
                    <div id="imgModal" class="modal">
                      <span class="close" onclick="closeModal()">&times;</span>
                      <img class="modal-content" id="modalImage">
                    </div>

                    <script>
                    function openModal(src) {{
                        var modal = document.getElementById("imgModal");
                        var modalImg = document.getElementById("modalImage");
                        modal.style.display = "block";
                        modalImg.src = src;
                    }}
                    function closeModal() {{
                        var modal = document.getElementById("imgModal");
                        modal.style.display = "none";
                    }}
                    </script>
                    </body></html>""")

    def _add_result_to_report(self, result, test_name, actual_path, baseline_path, diff_path, message):
        """Add a result row to the HTML report."""
        report_path = os.path.join(self.output_dir, self.report_name)
        with open(report_path, 'r+') as f:
            content = f.read()
            index = content.find('</tbody>')

            def img_tag(image_path):
                if image_path and os.path.exists(image_path):
                    return f'<img src="{os.path.basename(image_path)}" onclick="openModal(this.src)" />'
                else:
                    return '-'

            new_row = f'<tr class="{result}">'
            new_row += f'<td>{test_name}</td>'
            new_row += f'<td>{img_tag(baseline_path)}</td>'
            new_row += f'<td>{img_tag(actual_path)}</td>'
            new_row += f'<td>{img_tag(diff_path)}</td>'
            new_row += f'<td>{message}</td>'
            new_row += '</tr>'
            content = content[:index] + new_row + content[index:]
            f.seek(0)
            f.write(content)
