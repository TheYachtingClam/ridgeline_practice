
import bisect


class Playground:

    def __init__(self, file: str):
        self.red_tiles = []
        with open(file, 'r') as data:
            for line in data.readlines():
                sp = line.strip().split(',')
                self.red_tiles.append((int(sp[0]), int(sp[1])))
        self._build_validity_structure()

    def __str__(self):
        ret_val = ''
        for tile in self.red_tiles:
            ret_val += f'{tile[0], tile[1]}\n'
        return ret_val

    # --- Part 1 ---

    def is_covered(self, tile_one, tile_two) -> bool:
        ''' I'm writing this as a BS version assuming that no one is coming back in and "filling in"
        the broken square with future passes.  It's a big edge case that I'm going to ignore'''
        initial_tile = None
        for tile in self.red_tiles:
            if initial_tile is None:
                initial_tile = tile
                continue

            if self.is_inside(tile_one=tile_one, tile_two=tile_two, tile=tile):
                return False
        return True

    def is_inside(self, tile_one, tile_two, tile) -> bool:
        tile_is_inside = False

        if tile[0] > min(tile_one[0], tile_two[0]) and tile[0] < max(tile_one[0], tile_two[0]) and tile[1] > min(tile_one[1], tile_two[1]) and tile[1] < max(tile_one[1], tile_two[1]):
            tile_is_inside = True

        return tile_is_inside

    def find_biggest(self) -> int:
        largest_size = 0
        for outsidetile_index, outsidetile in enumerate(self.red_tiles):
            if outsidetile_index + 1 == len(self.red_tiles):
                continue
            for _, insidetile in enumerate(self.red_tiles[outsidetile_index+1:]):

                size = (abs(outsidetile[0] - insidetile[0]) + 1) * \
                    (abs(outsidetile[1] - insidetile[1]) + 1)
                if size > largest_size and self.is_covered(outsidetile, insidetile):
                    print(
                        f'largest set to {size} with {outsidetile} and {insidetile}')
                    largest_size = size
        return largest_size

    # --- Part 2 ---

    def _build_validity_structure(self):
        """
        Coordinate-compressed validity check. The grid can be huge (96K×96K),
        so we never enumerate individual tiles. Instead:
          - Only the N unique x/y values from red tiles create "interesting" boundaries.
          - Between consecutive interesting values, all tiles have identical validity.
          - We build a small compressed grid (≤2N × 2N) and use 2D prefix sums
            so every rectangle query is O(1).
        """
        print('building border segments...', flush=True)
        n = len(self.red_tiles)
        segs_v = []  # vertical segments: (x, y_min, y_max)
        segs_h = []  # horizontal segments: (y, x_min, x_max)
        for i in range(n):
            a = self.red_tiles[i]
            b = self.red_tiles[(i + 1) % n]
            if a[0] == b[0]:
                segs_v.append((a[0], min(a[1], b[1]), max(a[1], b[1])))
            else:
                segs_h.append((a[1], min(a[0], b[0]), max(a[0], b[0])))

        # Fast border lookup
        segs_v_by_x = {}
        for vx, vy_min, vy_max in segs_v:
            segs_v_by_x.setdefault(vx, []).append((vy_min, vy_max))
        segs_h_by_y = {}
        for hy, hx_min, hx_max in segs_h:
            segs_h_by_y.setdefault(hy, []).append((hx_min, hx_max))

        def is_on_border(x, y):
            for vy_min, vy_max in segs_v_by_x.get(x, []):
                if vy_min <= y <= vy_max:
                    return True
            for hx_min, hx_max in segs_h_by_y.get(y, []):
                if hx_min <= x <= hx_max:
                    return True
            return False

        print('building compressed coordinates...', flush=True)
        xs = sorted(set(t[0] for t in self.red_tiles))
        ys = sorted(set(t[1] for t in self.red_tiles))

        # Interleave exact coords with gap representatives.
        # cx[k] = xs[i] for exact coords, xs[i]+1 for the gap (xs[i], xs[i+1]).
        # One gap representative covers ALL tiles strictly between two consecutive xs values
        # because validity is constant within that span.
        cx = []
        for i, x in enumerate(xs):
            cx.append(x)
            if i + 1 < len(xs) and xs[i + 1] > x + 1:
                cx.append(x + 1)
        cy = []
        for i, y in enumerate(ys):
            cy.append(y)
            if i + 1 < len(ys) and ys[i + 1] > y + 1:
                cy.append(y + 1)

        W, H = len(cx), len(cy)
        print(f'compressed grid: {W} x {H} = {W * H} cells', flush=True)

        # For each cy value, precompute sorted x-coords of vertical segments
        # that strictly straddle that y (used for ray-casting interior check).
        cy_cross = [
            sorted(vx for vx, vy_min, vy_max in segs_v if vy_min <= y < vy_max)
            for y in cy
        ]

        def is_valid(x, y, cross_xs):
            if is_on_border(x, y):
                return True
            # Ray cast rightward: odd crossings → inside polygon → valid
            idx = bisect.bisect_right(cross_xs, x)
            return (len(cross_xs) - idx) % 2 == 1

        print('computing cell validity...', flush=True)
        invalid = [[0] * H for _ in range(W)]
        for i, x in enumerate(cx):
            if i % max(1, W // 20) == 0:
                print(f'\r  {i * 100 // W}%', end='', flush=True)
            for j, y in enumerate(cy):
                if not is_valid(x, y, cy_cross[j]):
                    invalid[i][j] = 1
        print('\rcell validity done     ', flush=True)

        # 2D prefix sums over invalid counts
        prefix = [[0] * (H + 1) for _ in range(W + 1)]
        for i in range(W):
            for j in range(H):
                prefix[i + 1][j + 1] = (invalid[i][j]
                                        + prefix[i][j + 1]
                                        + prefix[i + 1][j]
                                        - prefix[i][j])

        self._cx_idx = {x: i for i, x in enumerate(cx)}
        self._cy_idx = {y: j for j, y in enumerate(cy)}
        self._prefix = prefix
        print('validity structure ready', flush=True)

    def _rectangle_is_valid(self, tile_one, tile_two) -> bool:
        x1 = min(tile_one[0], tile_two[0])
        x2 = max(tile_one[0], tile_two[0])
        y1 = min(tile_one[1], tile_two[1])
        y2 = max(tile_one[1], tile_two[1])
        ix1 = self._cx_idx.get(x1)
        ix2 = self._cx_idx.get(x2)
        iy1 = self._cy_idx.get(y1)
        iy2 = self._cy_idx.get(y2)
        if None in (ix1, ix2, iy1, iy2):
            return False
        p = self._prefix
        invalid_count = p[ix2+1][iy2+1] - \
            p[ix1][iy2+1] - p[ix2+1][iy1] + p[ix1][iy1]
        return invalid_count == 0

    def find_biggest_valid(self) -> int:
        largest_size = 0
        n = len(self.red_tiles)
        total_pairs = n * (n - 1) // 2
        completed = 0
        last_pct = -1
        for i in range(n):
            for j in range(i + 1, n):
                tile_one = self.red_tiles[i]
                tile_two = self.red_tiles[j]
                size = (abs(tile_one[0] - tile_two[0]) + 1) * \
                       (abs(tile_one[1] - tile_two[1]) + 1)
                if size > largest_size and self._rectangle_is_valid(tile_one, tile_two):
                    print(
                        f'largest set to {size} with {tile_one} and {tile_two}')
                    largest_size = size
                completed += 1
                pct = completed * 100 // total_pairs
                if pct != last_pct:
                    print(f'\r{pct}% ({completed}/{total_pairs})',
                          end='', flush=True)
                    last_pct = pct
        print()
        return largest_size


playground = Playground('day9/data.txt')
print(f'Part 1 biggest: {playground.find_biggest()}')
print(f'Part 2 biggest (valid tiles only): {playground.find_biggest_valid()}')
