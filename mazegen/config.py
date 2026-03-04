from dataclasses import dataclass


@dataclass
class MazeConf:
    """
    Data class representing the maze configuration.

    Attributes:
        width: Width of the maze.
        height: Height of the maze.
        entry: Entry coordinates (row, column).
        exit1: Exit coordinates (row, column).
        output_file: Output file path.
        perfect: Whether the maze should be perfect.
        seed: Optional random seed.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit1: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def pars_config(filepath: str) -> MazeConf | None:
    """
    Parse a configuration file and return a MazeConf object.

    The configuration file must contain mandatory keys:
    WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
    Optional key: SEED.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A MazeConf object if parsing is successful,
        otherwise None if an error occurs.
    """
    data: dict[str, str] = {}
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY',
                 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    optional = ['SEED']
    allowed = mandatory + optional

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
                if key.strip() != key or value.strip() != value:
                    print(f"ERROR: valide format: KEY=VALUE: {line}")
                    return None

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key not in allowed:
                    print(f"WARNING: unknown key ignored: {key}")
                    continue

                if not value:
                    print(f"ERROR: empty value for key: {key}")
                    return None
                data[key] = value

        for key in mandatory:
            if key not in data:
                print(f"ERROR: missing key: {key}")
                return None

    except FileNotFoundError:
        print(f"ERROR: file not found {filepath}")
        return None

    try:
        width = int(data['WIDTH'])
        height = int(data['HEIGHT'])
    except ValueError:
        print("ERROR: WIDTH and HEIGHT must be integers")
        return None

    if width < 3 or height < 3:
        print("ERROR: WIDTH and HEIGHT must be at least 3")
        return None

    try:
        entry = data['ENTRY']
        if " " in entry:
            raise ValueError("ERROR: ENTRY: Format must be x,y")

        content = entry[0:3]
        ex, ey = content.split(",")

        if not ex.isdigit() or not ey.isdigit():
            raise ValueError("ERROR: x and y must be integers in (ENTRY)")

        entry = (int(ex), int(ey))

        exit1 = data['EXIT']
        if " " in exit1:
            raise ValueError("ERROR: EXIT: Format must be x,y")

        content = exit1[0:3]
        ex, ey = content.split(",")

        if not ex.isdigit() or not ey.isdigit():
            raise ValueError("ERROR: x and y must be integers in (EXIT)")

        exit1 = (int(ex), int(ey))
    except (ValueError, IndexError) as error:
        print(error)
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

    seed = None
    if 'SEED' in data:
        try:
            seed = int(data['SEED'])
        except ValueError:
            print("ERROR: SEED must be an integer")
            return None

    return MazeConf(
        width=width,
        height=height,
        entry=entry,
        exit1=exit1,
        output_file=data['OUTPUT_FILE'],
        perfect=data['PERFECT'] == 'True',
        seed=seed
    )
