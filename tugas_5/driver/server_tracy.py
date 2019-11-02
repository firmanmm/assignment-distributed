import server as srv

if __name__ == "__main__":
    server = srv.FileServer("localhost", 7777, "TRACY-", ["ZULU-FileServer", "ALPHA-FileServer"])
    server.Start()