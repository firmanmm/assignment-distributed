# Assignment 5
## Assignee
- Name : **Firman Maulana**
- NRP : **0511164000059**
- Course : **Distributed System**

## Requirements
Create a remote file server with capabilities of 
1. Saving file
2. Read file
3. Delete file
4. Update file
5. List file
6. Maintain Data Centric Consistency

Client will connect to remote server using Pyro 4 library and perform remote execution

## Usage

### Running

1. Run `pyro4-ns -n localhost -p 7777`
2. Run `python server.py`
3. Run `python client.py`

### Commands

- `STORE` file to remote server, return error if file already exist
- `UPDATE` file content to remote server, return error if file not exist
- `APPEND` file content to existing remote file, return error if file not exist
- `GET` file from remote server, return error if file not exist
- `DELETE` file on remote server, return error if file not exist
- `LIST` list all files on remote server