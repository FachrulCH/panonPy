from PIL import Image, ImageChops

class VisualComparer:
    def __init__(self, actual_path, baseline_path, diff_path):
        self.actual_path = actual_path
        self.baseline_path = baseline_path
        self.diff_path = diff_path

        self.img_actual = None
        self.img_baseline = None
        self.mask = None

    def compare(self):
        """Compare actual and baseline images and return difference percentage"""
        with Image.open(self.actual_path) as img_actual, Image.open(self.baseline_path) as img_baseline:
            self.img_actual = img_actual.convert('RGB')
            self.img_baseline = img_baseline.convert('RGB')

            # Validate image sizes are identical
            if self.img_actual.size != self.img_baseline.size:
                raise ValueError(
                    f"Image sizes do not match: actual {self.img_actual.size} vs baseline {self.img_baseline.size}"
                )

            diff = ImageChops.difference(self.img_actual, self.img_baseline).convert('L')
            self.mask = diff.point(lambda x: 255 if x else 0)

            total_pixels = self.img_actual.width * self.img_actual.height
            diff_pixels = sum(1 for pixel in self.mask.getdata() if pixel != 0)

            return diff_pixels / total_pixels

    def save_diff_image(self):
        """Save a diff image highlighting differences"""
        if self.mask is None or self.img_actual is None:
            raise ValueError("You must call compare() before save_diff_image().")

        red = Image.new('RGB', self.img_actual.size, (255, 0, 0))
        diff_img = Image.composite(red, self.img_actual, self.mask)
        diff_img.save(self.diff_path)