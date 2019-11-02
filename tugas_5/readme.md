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
6. Maintain Data Centric Consistency between operation
7. Maintain Data Centric Consistency even when there is downtime

Client will connect to remote server using Pyro 4 library and perform remote execution

## Usage

### Running

1. Run `pyro4-ns -n localhost -p 7777`
2. Run `python driver.server_zulu`
3. Run `python driver.server_alpha`
4. Run `python driver.server_tracy`
5. Run `python driver.client_zulu`
6. Run `python driver.client_alpha`
7. Run `python driver.client_tracy`


### Commands

- `STORE` file to remote server, return error if file already exist
- `UPDATE` file content to remote server, return error if file not exist
- `APPEND` file content to existing remote file, return error if file not exist
- `GET` file from remote server, return error if file not exist
- `DELETE` file on remote server, return error if file not exist
- `LIST` list all files on remote server

## How It Works

When there is a *modification* operation such as *upload*, *update*, *append*, *delete* it will trigger lock between server to prevent race condition when modifying files.
Read operation is not blocked. When there is a downtime, the server that recover will try to contact the server one by one until it found an online server.
When there is a response from an online server, the recovering server will synchronize all of it's file with the responding server.
When there is no response at all then it is safe to assume that there are no synchronization server and this server will act as an online server for other server's downtime recovery.