import inspect
import sys


def _leading_spaces(l):
    return len(l) - len(l.lstrip(' '))


def _get_lines_in_block(filename, line_nb):

    lines = []
    with open(filename) as f:
        for _ in range(line_nb):
            next(f)

        line = f.readline()
        while line.strip().startswith("#"):
            line = f.readline()

        first_line = line
        first_leading_spaces = _leading_spaces(first_line)
        lines.append(first_line)

        for line in f:
            if line.strip().startswith("#"):
                continue
            if _leading_spaces(line) >= first_leading_spaces:
                lines.append(line)

    return lines


def _parse_commands(code):

    # parsing top-level commands
    level = 0
    starts = []
    dot_without_paren = False
    open_call = False
    lastchar = None
    for i, char in enumerate(code, 0):
        if char in (" ", "\n", "\t"): continue

        if char == "(":
            if lastchar == ")" and level == 0:
                starts.append((i, char))
                open_call = True
            dot_without_paren = False
            level += 1
        elif char == ")":
            if open_call and level == 0:
                open_call = False
            level -= 1
        elif level == 0 and char == "." and not dot_without_paren:
            dot_without_paren = True
            starts.append((i, char))
        lastchar = char

    commands = []
    last_i = None
    for (i, _) in starts:
        commands.append(code[last_i:i])
        last_i = i
    commands.append(code[last_i:])

    return commands


def _run_commands(commands, start_line, source_file):

    clean = " ".join(commands[0].split()).strip()
    if "=" in clean:
        clean = clean.split("=")[1]
    var_name = "__dbg"
    __dbg = eval(clean)
    print("Start data:", file=sys.stderr)
    print(__dbg, file=sys.stderr)
    print("", file=sys.stderr)

    for command in commands[1:]:
        clean = " ".join(command.split()).strip().\
            replace("( ", "(").replace(") ", ")")
        dirty = var_name + clean
        __dbg = eval(dirty)
        print(clean, file=sys.stderr)
        print(__dbg, file=sys.stderr)
        print("", file=sys.stderr)

    print("[{}:{}]".format(source_file, start_line), file=sys.stderr)


class Debug:
    def __init__(self):
        frames = inspect.stack()
        for frame in frames:
            line = frame.code_context[0]
            if "Debug" in line:
                break

        lines = _get_lines_in_block(frame.filename, frame.lineno)

        code = "".join(lines)

        commands = _parse_commands(code)

        _run_commands(commands, frame.lineno, frame.filename)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == "__main__":

    import pyranges as pr
    exons = pr.data.exons()
    cpg = pr.data.cpg()

    with Debug():

        f = cpg.join(exons.unstrand()).slack(500)(lambda df: df.CpG > 50)(
            lambda df: ~df.Name.str.startswith("NR"))

    # Start data:
    # +--------------+-----------+-----------+-----------+
    # | Chromosome   | Start     | End       | CpG       |
    # | (category)   | (int64)   | (int64)   | (int64)   |
    # |--------------+-----------+-----------+-----------|
    # | chrX         | 64181     | 64793     | 62        |
    # | chrX         | 69133     | 70029     | 100       |
    # | chrX         | 148685    | 149461    | 85        |
    # | ...          | ...       | ...       | ...       |
    # | chrY         | 28773315  | 28773544  | 25        |
    # | chrY         | 59213794  | 59214183  | 36        |
    # | chrY         | 59349266  | 59349574  | 29        |
    # +--------------+-----------+-----------+-----------+
    # PyRanges object has 1077 sequences from 2 chromosomes.
    #
    # .join(exons.unstrand())
    # +--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------+
    # | Chromosome   | Start     | End       | CpG       | Start_b   | End_b     | Name                                  | Score     |
    # | (category)   | (int64)   | (int64)   | (int64)   | (int64)   | (int64)   | (object)                              | (int64)   |
    # |--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------|
    # | chrX         | 584563    | 585326    | 66        | 585078    | 585337    | NM_000451_exon_0_0_chrX_585079_f      | 0         |
    # | chrX         | 1510501   | 1511838   | 173       | 1510791   | 1511039   | NM_001636_exon_3_0_chrX_1510792_r     | 0         |
    # | chrX         | 1553851   | 1554115   | 20        | 1553914   | 1553976   | NM_004192_exon_8_0_chrX_1553915_r     | 0         |
    # | ...          | ...       | ...       | ...       | ...       | ...       | ...                                   | ...       |
    # | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NR_047599_exon_28_0_chrY_15591394_r   | 0         |
    # | chrY         | 16941822  | 16942188  | 32        | 16941609  | 16942399  | NM_014893_exon_4_0_chrY_16941610_f    | 0         |
    # | chrY         | 26979889  | 26980116  | 21        | 26979966  | 26980276  | NM_001005375_exon_0_0_chrY_26979967_f | 0         |
    # +--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------+
    # PyRanges object has 79 sequences from 2 chromosomes.
    #
    # .slack(500)
    # +--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------+
    # | Chromosome   | Start     | End       | CpG       | Start_b   | End_b     | Name                                  | Score     |
    # | (category)   | (int64)   | (int64)   | (int64)   | (int64)   | (int64)   | (object)                              | (int64)   |
    # |--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------|
    # | chrX         | 584063    | 585826    | 66        | 585078    | 585337    | NM_000451_exon_0_0_chrX_585079_f      | 0         |
    # | chrX         | 1510001   | 1512338   | 173       | 1510791   | 1511039   | NM_001636_exon_3_0_chrX_1510792_r     | 0         |
    # | chrX         | 1553351   | 1554615   | 20        | 1553914   | 1553976   | NM_004192_exon_8_0_chrX_1553915_r     | 0         |
    # | ...          | ...       | ...       | ...       | ...       | ...       | ...                                   | ...       |
    # | chrY         | 15590759  | 15592220  | 33        | 15591393  | 15592550  | NR_047599_exon_28_0_chrY_15591394_r   | 0         |
    # | chrY         | 16941322  | 16942688  | 32        | 16941609  | 16942399  | NM_014893_exon_4_0_chrY_16941610_f    | 0         |
    # | chrY         | 26979389  | 26980616  | 21        | 26979966  | 26980276  | NM_001005375_exon_0_0_chrY_26979967_f | 0         |
    # +--------------+-----------+-----------+-----------+-----------+-----------+---------------------------------------+-----------+
    # PyRanges object has 79 sequences from 2 chromosomes.
    #
    # (lambda df: df.CpG > 50)
    # +--------------+-----------+-----------+-----------+-----------+-----------+------------------------------------+-----------+
    # | Chromosome   |     Start |       End |       CpG |   Start_b |     End_b | Name                               |     Score |
    # | (category)   |   (int64) |   (int64) |   (int64) |   (int64) |   (int64) | (object)                           |   (int64) |
    # |--------------+-----------+-----------+-----------+-----------+-----------+------------------------------------+-----------|
    # | chrX         |    584063 |    585826 |        66 |    585078 |    585337 | NM_000451_exon_0_0_chrX_585079_f   |         0 |
    # | chrX         |   1510001 |   1512338 |       173 |   1510791 |   1511039 | NM_001636_exon_3_0_chrX_1510792_r  |         0 |
    # | chrX         |   2845695 |   2848011 |        92 |   2847272 |   2847416 | NM_001669_exon_9_0_chrX_2847273_r  |         0 |
    # | chrY         |    240898 |    246468 |       310 |    244667 |    245252 | NM_013239_exon_0_0_chrY_244668_r   |         0 |
    # | chrY         |  14531615 |  14534100 |       126 |  14533348 |  14533389 | NR_033667_exon_4_0_chrY_14533349_r |         0 |
    # +--------------+-----------+-----------+-----------+-----------+-----------+------------------------------------+-----------+
    # PyRanges object has 47 sequences from 2 chromosomes.
    #
    # (lambda df: ~df.Name.str.startswith("NR"))
    # +--------------+-----------+-----------+-----------+-----------+-----------+-----------------------------------+-----------+
    # | Chromosome   |     Start |       End |       CpG |   Start_b |     End_b | Name                              |     Score |
    # | (category)   |   (int64) |   (int64) |   (int64) |   (int64) |   (int64) | (object)                          |   (int64) |
    # |--------------+-----------+-----------+-----------+-----------+-----------+-----------------------------------+-----------|
    # | chrX         |    584063 |    585826 |        66 |    585078 |    585337 | NM_000451_exon_0_0_chrX_585079_f  |         0 |
    # | chrX         |   1510001 |   1512338 |       173 |   1510791 |   1511039 | NM_001636_exon_3_0_chrX_1510792_r |         0 |
    # | chrX         |   2845695 |   2848011 |        92 |   2847272 |   2847416 | NM_001669_exon_9_0_chrX_2847273_r |         0 |
    # | chrY         |    240898 |    246468 |       310 |    244667 |    245252 | NM_013239_exon_0_0_chrY_244668_r  |         0 |
    # +--------------+-----------+-----------+-----------+-----------+-----------+-----------------------------------+-----------+
    # PyRanges object has 43 sequences from 2 chromosomes.
    #
    # [_inspect.py:121]
