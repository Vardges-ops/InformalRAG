from services.pipeline import run

if __name__ == "__main__":
    while True:
        query = input(">> ")
        result = run(query)
        print(result)