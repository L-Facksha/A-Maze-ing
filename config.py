from dataclasses import dataclass


@dataclass
class Mazeconf():
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def pars_config(filepath: str) -> Mazeconf | None:
    data = {}
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY',
                 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"ERROR: Invalid format: {line}")
                    return None

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # TODO -> had l if li teht kthandli gha keys maghankhdmoch bihom
                if key not in mandatory:
                    print(f"WARNING: unknown key ignored: {key}")
                    continue

                #TODO -> hadi ila 3titi key witout value
                if not value:
                    print(f"ERROR: empty value for key: {key}")
                    return None
                data[key] = value

        # TODO -> o hadi kathandli ila nsiti chi key li khessk tkhdem bih
        for key in mandatory:
            if key not in data:
                print(f"ERROR: missing key: {key}")
                return None

    except FileNotFoundError:
        print(f"ERROR: file not found {filepath}")
        return None

    #TODO -> hna kanhandli gha integer number
    try:
        width = int(data['WIDTH'])
        height = int(data['HEIGHT'])
    except ValueError:
        print("ERROR: WIDTH and HEIGHT must be integers")
        return None

    # TODO -> khesso ikon 3el 2a9al kber mn 3
    if width < 3 or height < 3:
        print("ERROR: WIDTH and HEIGHT must be at least 3")
        return None

    try:
        entry = (int(data['ENTRY'].split(',')[0]),
                 int(data['ENTRY'].split(',')[1]))
        exit1 = (int(data['EXIT'].split(',')[0]),
                 int(data['EXIT'].split(',')[1]))
    except (ValueError, IndexError):
        print("ERROR: ENTRY and EXIT must be in format x, y")
        return None

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        print("ERROR: ENTRY is outside maze bounds")
        return None

    if not (0 <= exit1[0] < width and 0 <= exit1[1] < height):
        print("ERROR: EXIT is outside maze bounds")
        return None

    if entry == exit1:
        print("ERROR: ENTRY and EXIT must be diffrent")
        return None

    if data['PERFECT'] not in ('True', 'False'):
        print("ERROR: PERFECT must be True or False")
        return None

    return Mazeconf(
        width=width,
        height=height,
        entry=entry,
        exit=exit1,
        output_file=data['OUTPUT_FILE'],
        perfect=data['PERFECT'] == 'True'
    )


tt = pars_config("test.txt")
print(tt)
