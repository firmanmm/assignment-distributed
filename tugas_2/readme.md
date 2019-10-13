# Assignment 2
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
6. Able to detect failure with Ping - ACK
7. Able to detect failure with Centralized Hearthbeat
8. Able to detect failure with All to All Hearthbeat


Client will connect to remote server using Pyro 4 library and perform remote execution. Heartbeat down detection is utilizing time since last beat instead of sequence number for better accuracy.

## Usage

### Running
Please run it from current directory since this python project utilitize python module.

#### Ping-ACK
1. Run `pyro4-ns -n localhost -p 7777`
2. Run `python -m ping_ack.server`
3. Run `python -m ping_ack.client`

#### Centralized
1. Run `pyro4-ns -n localhost -p 7777`
2. Run `python -m centralized.central`
3. Run `python -m centralized.server_1`
4. Run `python -m centralized.server_2`
5. Run `python -m centralized.client`

#### All to All
1. Run `pyro4-ns -n localhost -p 7777`
2. Run `python -m centralized.server_1`
3. Run `python -m centralized.server_2`
4. Run `python -m centralized.client`

### Commands

- `STORE` file to remote server, return error if file already exist
- `UPDATE` file content to remote server, return error if file not exist
- `APPEND` file content to existing remote file, return error if file not exist
- `GET` file from remote server, return error if file not exist
- `DELETE` file on remote server, return error if file not exist
- `LIST` list all files on remote server