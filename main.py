import logs
import member_data

def main() -> None:
    member_data.gen_tables()
    logs.gen_tables()

if __name__ == "__main__":
    main()