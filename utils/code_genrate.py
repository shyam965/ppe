def generate_member_code(self, prefix: str, last_code: str) -> str:
        last_number = int(last_code[len(prefix):]) if last_code else 0
        return f"{prefix}{last_number + 1}"