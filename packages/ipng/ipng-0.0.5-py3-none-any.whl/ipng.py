import zlib

from filter import FILTER_TYPE_TO_FUNC


class PNG:
    """
    Reference: https://tools.ietf.org/html/rfc2083#section-3

    The first eight bytes of a PNG file always contain the following
    values:

        (decimal)              137  80  78  71  13  10  26  10
        (hexadecimal)           89  50  4e  47  0d  0a  1a  0a
        (ASCII C notation)    \211   P   N   G  \r  \n \032 \n

    This signature both identifies the file as a PNG file and provides
    for immediate detection of common file-transfer problems.  The
    first two bytes distinguish PNG files on systems that expect the
    first two bytes to identify the file type uniquely.  The first
    byte is chosen as a non-ASCII value to reduce the probability that
    a text file may be misrecognized as a PNG file; also, it catches
    bad file transfers that clear bit 7.  Bytes two through four name
    the format.  The CR-LF sequence catches bad file transfers that
    alter newline sequences.  The control-Z character stops file
    display under MS-DOS.  The final line feed checks for the inverse
    of the CR-LF translation problem.
    """

    # Default size for a IDAT chunk.
    IDAT_CHUNK_SIZE = 16384

    # Color type determines number samples for each pixel
    # Color    Allowed    Interpretation
    # Type     Bit Depths
    #
    # 0       1,2,4,8,16  Each pixel is a grayscale sample.
    #
    # 2       8,16        Each pixel is an R,G,B triple.
    #
    # 3       1,2,4,8     Each pixel is a palette index;
    #                     a PLTE chunk must appear.
    #
    # 4       8,16        Each pixel is a grayscale sample,
    #                     followed by an alpha sample.
    #
    # 6       8,16        Each pixel is an R,G,B triple,
    #                     followed by an alpha sample.
    COLOR_TYPE_TO_NUM_SAMPLE = {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4
    }

    # Bit depth restrictions for each color type are imposed to
    # simplify implementations and to prohibit combinations that do
    # not compress well.  Decoders must support all legal
    # combinations of bit depth and color type.  The allowed
    # combinations are:
    #
    #    Color    Allowed    Interpretation
    #    Type    Bit Depths
    #
    #    0       1,2,4,8,16  Each pixel is a grayscale sample.
    #
    #    2       8,16        Each pixel is an R,G,B triple.
    #
    #    3       1,2,4,8     Each pixel is a palette index;
    #                        a PLTE chunk must appear.
    #
    #    4       8,16        Each pixel is a grayscale sample,
    #                        followed by an alpha sample.
    #
    #    6       8,16        Each pixel is an R,G,B triple,
    #                        followed by an alpha sample.
    SAMPLE_NUM_LOOKUP = {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4
    }

    def __init__(self, file):
        self._heading = bytearray()
        self._file = file
        self._chunk_ordering_list = []
        self._chunk_hist = {}
        self._data = bytearray(b'')

        self.bitmap = []
        self.metadata = None

        self._validate()
        self._analyze()

    def render(self, output):
        """
        Renders the image including the processing function, save to the output file.
        :param output: path to the output file
        :return: None
        """

        # Handle scanlines
        # given each scanline is prepended with 1 byte of the filter
        # method before compressing, number of bytes each scanline for
        # the image itself is really:
        #
        # len(decompressed)/height - 1
        #
        # which is equal to:
        #
        # width * number of samples per pixel * bit depth / 8
        bpp = int(self.pixel_size_in_bit / 8)
        real_scanline_len = len(self.bitmap[0])

        filtered_image = self._filter_image(bpp, self.bitmap, real_scanline_len)

        # compress updated image, the compress method with default parameters seem to work well for PNG standard
        compressed = zlib.compress(filtered_image)

        self._rebuild_image(compressed, output)

    def _chunk_hist_str_ordered(self):
        result_list = []
        for chunk_name in self._chunk_ordering_list:
            result_list.append(f'{chunk_name}:{self._chunk_hist[chunk_name]["count"]}')
        return ','.join(result_list)

    def _walk_chunks(self, pic_f):
        # skipping the first 8 bytes for header
        self._heading = pic_f.read(8)

        while True:
            raw_data, length, chunk_type, chunk_data, crc = self._read_one_chunk(pic_f)

            if chunk_type == 'IHDR':
                self._analyze_header(chunk_data, length)
            elif chunk_type == 'IDAT':
                # print(f'reading chunk_length = {length}')
                self._data.extend(chunk_data)

            if chunk_type in self._chunk_hist:
                self._chunk_hist[chunk_type]['count'] += 1
            else:
                self._chunk_ordering_list.append(chunk_type)
                self._chunk_hist[chunk_type] = {'raw': raw_data, 'count': 1}

            if chunk_type == 'IEND':
                break

        self.metadata = f'{self.metadata}\n{"chunk histogram:":20}{self._chunk_hist_str_ordered()}'

        # Deflate-compressed datastreams within PNG are stored in the "zlib"
        # format, which has the structure:
        #
        # Compression method/flags code: 1 byte
        # Additional flags/check bits:   1 byte
        # Compressed data blocks:        n bytes
        # Check value:                   4 bytes
        method_flag = self._data[0]
        additional = self._data[1]
        check = self._data[-4]
        self.metadata = f'{self.metadata}\n' \
            f'{"compression spec:":20}' \
            f'method/flag:{method_flag},' \
            f'additional:{additional},' \
            f'check:{check}'

        decompressed = zlib.decompress(self._data)

        # Handle scanlines
        # given each scanline is prepended with 1 byte of the filter
        # method before compressing, number of bytes each scanline for
        # the image itself is really:
        #
        # len(decompressed)/height - 1
        #
        # which is equal to:
        #
        # width * number of samples per pixel * bit depth / 8
        bpp = int(self.pixel_size_in_bit / 8)
        scanline_len = int(len(decompressed) / self.height)

        self.bitmap = self._recover_image(bpp, decompressed, scanline_len)

    def _filter_image(self, bpp, bitmap, real_scanline_len):
        filtered_image = bytearray()
        previous_line = None
        for i in range(self.height):
            updated_scanline = bytearray(real_scanline_len + 1)
            updated_scanline[:] = bitmap[i]
            filter_type = b'\x01' # TODO: auto choose
            updated_scanline[0:0] = bytearray(filter_type)
            previous_line_cache = updated_scanline
            updated_scanline = FILTER_TYPE_TO_FUNC[filter_type[0]][0](updated_scanline, previous_line, bpp)
            filtered_image.extend(updated_scanline)
            previous_line = previous_line_cache
        return filtered_image

    def _recover_image(self, bpp, decompressed, scanline_len):
        recovered_image = []
        previous_line = None
        for i in range(self.height):
            scanline_copy = bytearray(scanline_len)
            scanline_copy[:] = decompressed[i * scanline_len:(i + 1) * scanline_len]
            filter_type = scanline_copy[0]
            scanline_copy = FILTER_TYPE_TO_FUNC[filter_type][1](scanline_copy, previous_line, bpp)
            recovered_scanline = bytearray()
            recovered_scanline[:] = scanline_copy[1:]
            recovered_image.append(recovered_scanline)
            previous_line = scanline_copy
        return recovered_image

    def _check_filter_result(self, filtered_image, decompressed, scanline_len):
        if filtered_image != decompressed:
            for i in range(self.height):
                beg = i * scanline_len
                end = (i + 1) * scanline_len
                current_decompressed_row = decompressed[beg:end]
                current_updated_row = filtered_image[beg:end]
                if current_decompressed_row != current_updated_row:
                    raise ArithmeticError(f'filtering error happened in row: {i} with filter type '
                                          f'{current_decompressed_row[0]}')

    def _rebuild_image(self, updated_data, output):
        if not output:
            return

        with open(output, 'wb') as of:
            of.write(self._heading)
            for chunk_name in self._chunk_ordering_list:
                chunk = self._chunk_hist[chunk_name]
                raw = chunk['raw']
                if chunk_name != 'IDAT':
                    of.write(raw)
                else:
                    PNG._write_idat(of, updated_data)

    def _validate(self):
        with open(self._file, 'rb') as pic_f:
            b = pic_f.read(8)
            if len(b) != 8 or b != b'\x89PNG\r\n\x1a\n':
                raise IOError(f'Input file: {self._file} does not conform to PNG heading.')

    def _analyze(self):
        with open(self._file, 'rb') as pic_f:
            self._walk_chunks(pic_f)

    def _analyze_header(self, header_bytes, length):
        # The IHDR chunk must appear FIRST.  It contains:
        #
        # Width:              4 bytes
        # Height:             4 bytes
        # Bit depth:          1 byte
        # Color type:         1 byte (1 is not a valid value)
        # Compression method: 1 byte (only 0 is a valid value)
        # Filter method:      1 byte (only 0 is a valid value)
        # Interlace method:   1 byte (0 or 1 are valid values)

        if length != 13:
            raise IOError(f'IHDR chunk must be 13 bytes, {length} found.')

        self.width = int.from_bytes(header_bytes[0:4], 'big')
        self.height = int.from_bytes(header_bytes[4:8], 'big')
        self.bit_depth = int.from_bytes(header_bytes[8:9], 'big')
        self.color_type = int.from_bytes(header_bytes[9:10], 'big')
        self.compression = int.from_bytes(header_bytes[10:11], 'big')
        self.filter = int.from_bytes(header_bytes[11:12], 'big')
        self.interlace = int.from_bytes(header_bytes[12:13], 'big')
        self.pixel_size_in_bit = self.COLOR_TYPE_TO_NUM_SAMPLE[self.color_type] * self.bit_depth
        self.metadata = f'{"basic spec:":20}' \
            f'width:{self.width},' \
            f'height:{self.height},' \
            f'bit_depth:{self.bit_depth},' \
            f'color_type:{self.color_type},' \
            f'pixel_size(bit):{self.pixel_size_in_bit},' \
            f'compression:{self.compression},' \
            f'filter:{self.filter},' \
            f'interlace:{self.interlace}'

    @staticmethod
    def _read_one_chunk(pic_f):
        raw_data = bytearray()
        # Length
        # A 4-byte unsigned integer giving the number of bytes in the
        # chunk's data field. The length counts only the data field, not
        # itself, the chunk type code, or the CRC.  Zero is a valid
        # length.  Although encoders and decoders should treat the length
        # as unsigned, its value must not exceed (2^31)-1 bytes.
        chunk_length = pic_f.read(4)
        raw_data.extend(chunk_length)
        length = int.from_bytes(chunk_length, 'big')
        # Chunk Type
        # A 4-byte chunk type code.  For convenience in description and
        # in examining PNG files, type codes are restricted to consist of
        # uppercase and lowercase ASCII letters (A-Z and a-z, or 65-90
        # and 97-122 decimal).  However, encoders and decoders must treat
        # the codes as fixed binary values, not character strings.  For
        # example, it would not be correct to represent the type code
        # IDAT by the EBCDIC equivalents of those letters.  Additional
        # naming conventions for chunk types are discussed in the next
        # section.
        chunk_type = pic_f.read(4)
        raw_data.extend(chunk_type)
        chunk_type_str = chunk_type.decode('utf-8')
        # Chunk Data
        # The data bytes appropriate to the chunk type, if any.  This
        # field can be of zero length.
        chunk_data = pic_f.read(length)
        raw_data.extend(chunk_data)
        # CRC
        # A 4-byte CRC (Cyclic Redundancy Check) calculated on the
        # preceding bytes in the chunk, including the chunk type code and
        # chunk data fields, but not including the length field. The CRC
        # is always present, even for chunks containing no data.  See CRC
        # algorithm (Section 3.4).
        crc = pic_f.read(4)
        raw_data.extend(crc)
        # print(f'chunk_type: {chunk_type} crc: {int.from_bytes(crc, "big")}, '
        #       f'calculated: {zlib.crc32(chunk_type + chunk_data)}')

        return raw_data, length, chunk_type_str, chunk_data, crc

    @staticmethod
    def _write_idat(of, updated_data):
        leftover_data = updated_data
        end = False
        # There can be multiple IDAT chunks; if so, they must appear
        # consecutively with no other intervening chunks.  The compressed
        # datastream is then the concatenation of the contents of all the
        # IDAT chunks.  The encoder can divide the compressed datastream
        # into IDAT chunks however it wishes.  (Multiple IDAT chunks are
        # allowed so that encoders can work in a fixed amount of memory;
        # typically the chunk size will correspond to the encoder's
        # buffer size.) It is important to emphasize that IDAT chunk
        # boundaries have no semantic significance and can occur at any
        # point in the compressed datastream.  A PNG file in which each
        # IDAT chunk contains only one data byte is legal, though
        # remarkably wasteful of space.  (For that matter, zero-length
        # IDAT chunks are legal, though even more wasteful.)
        while not end:
            if len(leftover_data) > PNG.IDAT_CHUNK_SIZE:
                current_chunk = leftover_data[0:PNG.IDAT_CHUNK_SIZE]
                leftover_data = leftover_data[PNG.IDAT_CHUNK_SIZE:]
            else:
                current_chunk = leftover_data
                end = True

            # print(binascii.hexlify(current_chunk)[0:100])

            chunk_length = len(current_chunk).to_bytes(4, 'big')
            # print(f'chunk_length: {len(current_chunk)}')
            # print(len(current_chunk))
            # print(f'chunk_length: {chunk_length}')
            chunk_type = bytearray('IDAT', 'utf-8')
            chunk_data = current_chunk
            crc = zlib.crc32(chunk_type + current_chunk).to_bytes(4, 'big')
            of.write(chunk_length + chunk_type + chunk_data + crc)
