from app.web import create_app


app = create_app()


def main():
    config = app.config["LRW_CONFIG"]
    app.run(host=config["host"], port=config["port"], debug=config["debug"])


if __name__ == "__main__":
    main()
