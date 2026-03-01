def save_to_file(self, filename: str) -> bool:
        """Save maze as hexadecimal."""
        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    hex_row = "".join(format(cell, 'x') for cell in row)
                    f.write(hex_row + '\n')
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False