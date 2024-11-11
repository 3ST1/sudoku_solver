# ./src/utils.py
import os


def read_input(file_path):
    """
    Reads the input Sudoku grid from a file and returns a linearized array.
    Empty cells are represented by -1.
    Args:
        file_path (str): Path to the input file.
    Returns:
        list[int]: A linearized array representing the input Sudoku grid.
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")

    grid = []

    try:
        with open(file_path, "r") as f:
            for line in f:
                # Ignore if it is a commented line or empty line
                if not line.strip() or line.startswith("#"):
                    continue

                # If the line is correctly formatted, it should contain 9 numbers separated by commas
                if not line.count(",") == 8 or not len(line.strip()) == 17:
                    raise ValueError(
                        "Each row in the file must contain exactly 9 numbers (each number must be  : 0<number<10) separated by commas."
                        + "\nPlease correct the file. \n\texample (replace 0 by numbers): \n"
                        + "\t0,0,0,0,0,0,0,0,0\n" * 9
                    )

                # Split the line by commas and convert each element to an integer
                row = [
                    int(num) if num != "0" else -1 for num in line.strip().split(",")
                ]

                # Check if the row has exactly 9 elements
                if len(row) != 9:
                    raise ValueError(
                        "Each row in the file must contain exactly 9 numbers."
                    )

                grid.extend(row)

        # Check if the total number of elements is 81
        if len(grid) != 81:
            raise ValueError(
                f"Invalid input file: Sudoku grid must contain exactly 81 numbers. Please correct the file '{file_path}'."
            )

    except ValueError as ve:
        raise ValueError(f"Error processing file '{file_path}': {ve}")

    return grid


def url_convert(url):
    # split from the bd parameter from the url
    if "bd=" not in url:
        raise ValueError("The URL does not contain a 'bd' parameter.")

    grid = url.split("bd=")[1]

    grid_to_return = []
    for i in range(9):
        grid_to_return.append(list(grid[i * 9 : (i + 1) * 9]))

    grid = ""
    for row in grid_to_return:
        grid += f"{','.join(row)}\n"

    return grid.strip()


def write_grid_to_file(grid, file_name):
    """
    Write the grid to a file.
    Args:
        grid (str): The grid to write to the file.
        file_name (str): The name of the file to write the grid to.
    Returns:
        None
    """
    with open(file_name, "w") as file:
        file.write(grid)


def convert_url_to_grid(url: str) -> str:
    """
    Function to convert a URL to the temporay test file.
    Args:
        url (str): The URL to convert.
    Returns:
        str: The path to the temporary test file.
    """
    output_file = "grids/temp_test.txt"
    write_grid_to_file(url_convert(url), output_file)
    return output_file


def delete_file(file_path: str):
    """
    Function to delete the temporary a file.
    Args:
        file_path (str): The path to the file to delete.
    Returns:
        None
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def validate_input(att_name, min_val, max_val, attempts=3):
    """
    Decorator to validate user input.
    Args:
        att_name (str): The name of the attribute.
        min_val (int): The minimum value for the attribute.
        max_val (int): The maximum value for the attribute.
        attempts (int): The number of attempts to allow the user to enter a valid value.
    Returns:
        function: The wrapper function.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            """
            Wrapper function to validate user input.
            """
            for _ in range(attempts):
                value = func(*args, **kwargs)
                try:
                    value = int(value)
                    if min_val <= value <= max_val:
                        return value
                    else:
                        raise ValueError
                except ValueError:
                    print(
                        f"{att_name} must be a number between {min_val} and {max_val}."
                    )
            print(
                f"3 consecutive failed attempts to enter a valid {att_name}. Exiting."
            )
            exit()

        return wrapper

    return decorator


def is_unique(values: list[int]) -> bool:
    """
    Check if a list of values contains only unique values.
    Args:
        values (list[int]): A list of integers.
    Returns:
        bool: True if all values are unique, False otherwise
    """
    seen = set()
    for value in values:
        if value != -1:  # Ignore empty cells
            if value in seen:
                return False
            seen.add(value)
    return True
