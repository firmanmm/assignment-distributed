import server as srv

if __name__ == "__main__":
    server = srv.FileServer("localhost", 7777, "ALPHA-", ["ZULU-FileServer", "TRACY-FileServer"])
    server.Start()