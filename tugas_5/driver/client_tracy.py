import client as cld

if __name__ == '__main__':
    client = cld.FileManagerClient("localhost", 7777, "TRACY-")
    client.RunCLI()