from PIL import Image, ImageChops


class PanonPy:
    """Library sederhana untuk membandingkan dua gambar"""

    @staticmethod
    def compare_images(image_path, baseline_path, diff_path=None, threshold=0):
        """
        Bandingkan dua gambar dan simpan gambar perbedaan.

        :param image_path: path gambar baru
        :param baseline_path: path gambar baseline
        :param diff_path: path untuk menyimpan gambar perbedaan (optional)
        :param threshold: toleransi persentase perbedaan (0-1)
        :return: (bool) True kalau gambar dianggap sama (di bawah threshold), False kalau beda
        """
        with Image.open(image_path) as img1, Image.open(baseline_path) as img2:
            # Sesuaikan ukuran
            max_size = (max(img1.width, img2.width), max(img1.height, img2.height))
            img1_max = Image.new('RGB', max_size)
            img1_max.paste(img1)
            img2_max = Image.new('RGB', max_size)
            img2_max.paste(img2)

            # Hitung perbedaan
            diff = ImageChops.difference(img1_max, img2_max).convert('L')
            diff_mask = diff.point(lambda x: 255 if x else 0)

            # Hitung persentase perbedaan
            total_pixels = max_size[0] * max_size[1]
            diff_pixels = sum(1 for pixel in diff_mask.getdata() if pixel != 0)
            diff_percentage = diff_pixels / total_pixels

            # Simpan gambar diff kalau mau
            if diff_path:
                # Highlight perbedaan di warna merah
                red = Image.new('RGB', max_size, (255, 0, 0))
                diff_img = Image.composite(red, img1_max, diff_mask)
                diff_img.save(diff_path)

            # Return hasil apakah beda atau tidak
            return diff_percentage <= threshold
