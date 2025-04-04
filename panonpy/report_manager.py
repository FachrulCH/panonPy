import os
import datetime

class ReportManager:
    def __init__(self, output_dir, report_name='VisualTests.html'):
        self.output_dir = output_dir
        self.report_path = os.path.join(output_dir, report_name)
        if not os.path.exists(self.report_path):
            self._create_report()

    def _create_report(self):
        with open(self.report_path, 'w') as f:
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
                            .modal {{ display: none; position: fixed; z-index: 1; padding-top: 60px; left: 0; top: 0;
                                      width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9); }}
                            .modal-content {{ margin: auto; display: block; width: 80%; max-width: 700px; }}
                            .close {{ position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; 
                                      font-weight: bold; transition: 0.3s; }}
                            .close:hover, .close:focus {{ color: #bbb; text-decoration: none; cursor: pointer; }}
                        </style>
                        </head><body>
                        <h1>PanonPy Visual Test Report</h1>
                        <p><b>Execution date:</b> {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                        <table>
                        <thead><tr><th>Test</th><th>Baseline</th><th>Actual</th><th>Diff</th><th>Result</th></tr></thead>
                        <tbody></tbody>
                        </table>

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

    def add_result(self, result, test_name, actual_image, baseline_image, diff_image, message):
        with open(self.report_path, 'r+') as f:
            content = f.read()
            index = content.find('</tbody>')

            def img_tag(image_path):
                if image_path and os.path.exists(image_path):
                    return f'<img src="{os.path.basename(image_path)}" onclick="openModal(this.src)" />'
                else:
                    return '-'

            new_row = f'<tr class="{result}">'
            new_row += f'<td>{test_name}</td>'
            new_row += f'<td>{img_tag(baseline_image)}</td>'
            new_row += f'<td>{img_tag(actual_image)}</td>'
            new_row += f'<td>{img_tag(diff_image)}</td>'
            new_row += f'<td>{message}</td>'
            new_row += '</tr>'

            content = content[:index] + new_row + content[index:]
            f.seek(0)
            f.write(content)