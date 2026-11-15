import png
class PNGParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.width, self.height, self.pixels, self.meta = self.parse_png()

    def parse_png(self):
        with open(self.file_path, 'rb') as f:
            reader = png.Reader(file=f)
            width, height, pixels, meta = reader.read_flat()
        return width, height, pixels, meta

    def get_pixels(self):
        return self.pixels

    def save_as_png_with_new_pixels(self, outfile_path: str, pixels: list):
        greyscale = self.meta.get('greyscale', False)
        alpha = self.meta.get('alpha', False)
        bitdepth = self.meta.get('bitdepth', 8)
        palette = self.meta.get('palette', None)
        planes = self.meta.get('planes', 3 if not greyscale else 1)  # 1, 3 или 4 канала

        row_len = self.width * planes

        with open(outfile_path, 'wb') as f:
            writer = png.Writer(
                width=self.width,
                height=self.height,
                greyscale=greyscale,
                alpha=alpha,
                bitdepth=bitdepth,
                palette=palette
            )

            def iter_rows():
                for y in range(self.height):
                    start = y * row_len
                    end = start + row_len
                    yield pixels[start:end]

            writer.write(f, iter_rows())

