import server as srv

if __name__ == "__main__":
    server = srv.FileServer("localhost", 7777, "ZULU-", ["ALPHA-FileServer", "TRACY-FileServer"])
    server.Start()