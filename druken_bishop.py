import random
import StringIO
import textwrap

class RandomArt(object):

    WIDTH = 17
    HEIGHT = 9
    CENTER = (8, 4)

    ALL_STEP_DIRECTIONS = [
        ('N', 'W'),
        ('N', 'E'),
        ('S', 'W'),
        ('S', 'E'),
    ]

    START_GLYPH = 'S'
    END_GLYPH = 'E'
    GLYPHS = ' .o+=*BOX@%&#/^'

    def __init__(self, debug=False):
        self.field = self.new_field()
        self.cursor = self.CENTER
        self.start_cursor = self.cursor
        self.steps = 0
        self.debug = debug

    def new_field(self):
        return [
            [0 for k in range(self.WIDTH)] for i in range(self.HEIGHT)
        ]

    def clear_field(self):
        self.field = self.new_field()
        self.cursor = self.CENTER
        self.steps = 0

    def randomart_mapper(self, c):
        _c = min(c, len(self.GLYPHS) - 1)
        return RandomArt.GLYPHS[_c]

    def set_cell(self, v, c, r):
        self.field[r][c] = v

    def get_cell(self, c, r):
        return self.field[r][c]

    def map_field(self):
        mapped_field = []

        for r, row in enumerate(self.field):
            curr_row = []

            for c, col in enumerate(row):
                if (c, r) == self.cursor:
                    curr_row.append(self.END_GLYPH)
                elif (c, r) == self.start_cursor:
                    curr_row.append(self.START_GLYPH)
                else:
                    value = self.get_cell(c, r)
                    mapped_char = self.randomart_mapper(value)
                    curr_row.append(mapped_char)

            mapped_field.append(curr_row)

        return mapped_field

    def __str__(self):
        return self.field_to_str()

    def field_to_str(self):
        mapped_field = self.map_field()
        str_buff = StringIO.StringIO()

        str_buff.write('+')
        str_buff.write('-' * self.WIDTH)
        str_buff.write('+\n')

        for l in mapped_field:
            str_buff.write('|')
            for c in l:
                str_buff.write(c)
            str_buff.write('|\n')

        str_buff.write('+')
        str_buff.write('-' * self.WIDTH)
        str_buff.write('+')

        full_string = str_buff.getvalue()
        str_buff.close()

        return full_string

    def step(self, ns, ew):
        col, row = self.cursor

        if ns == 'N':
            row -= 1
        elif ns == 'S':
            row += 1

        if ew == 'E':
            col += 1
        elif ew == 'W':
            col -= 1

        # clamp steps from moving off the board
        col = max(col, 0)
        col = min(col, self.WIDTH-1)
        row = max(row, 0)
        row = min(row, self.HEIGHT-1)

        new_cursor = (col, row)
        self.set_cell(self.get_cell(*new_cursor) + 1, *new_cursor)

        if self.debug:
            print 'Step #{}: {} from {} to {}'.format(self.steps, (ns,ew), self.cursor, new_cursor)

        self.cursor = new_cursor
        self.steps += 1

    def random_step(self):
        next_dir = random.choice(RandomArt.ALL_STEP_DIRECTIONS)
        self.step(*next_dir)

class BitPath(object):

    BITS_TO_DIRECTION_MAP = {
        '00': RandomArt.ALL_STEP_DIRECTIONS[0],
        '01': RandomArt.ALL_STEP_DIRECTIONS[1],
        '10': RandomArt.ALL_STEP_DIRECTIONS[2],
        '11': RandomArt.ALL_STEP_DIRECTIONS[3],
    }

    @staticmethod
    def bin(s):
        ''' from: https://wiki.python.org/moin/BitManipulation '''
        return str(s) if s<=1 else BitPath.bin(s>>1) + str(s&1)

    @staticmethod
    def padded_bin(s, mod=8):
        bin_str = BitPath.bin(s)

        while len(bin_str) % mod:
            bin_str = '0' + bin_str

        return bin_str

    @staticmethod
    def generate_from(hex_digest):
        bit_path = []

        for h in hex_digest.split(':'):
            h_bits = BitPath.padded_bin(int(h, 16))
            bit_path.extend(reversed(textwrap.wrap(h_bits, 2)))

        return bit_path

randomart = RandomArt()

key_fingerprint_md5 = '2f:9c:12:98:79:20:01:df:b4:70:cc:ef:0c:94:b0:43'
for b in BitPath.generate_from(key_fingerprint_md5):
    randomart.step( *BitPath.BITS_TO_DIRECTION_MAP[b] )

print randomart
