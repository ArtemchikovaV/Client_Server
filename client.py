import socket
import time

# My the best Server

class ClientError(Exception):
    pass

class ClientSocketError(ClientError):
    pass

class ClientProtocolError(ClientError):
    pass

class Client:
    def __init__(self, addres, connect, timeout=None):
        self.addres = addres
        self.connect = connect
        try:
            self.sock = socket.create_connection((addres, connect), timeout)
        except socket.error as err:
            raise ClientSocketError("error create connection", err)

    def __reseived_data(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.sock.recv(1024)
            except socket.error as err:
                raise ClientSocketError("error recv data", err)

            print("reseived data: ", data)
        decoded_data = data.decode()

        status, server_answer = decoded_data.split("\n", 1)
        server_answer= server_answer.strip()

        # если получили ошибку - бросаем исключение ClientError
        if status == "error":
            raise ClientProtocolError(server_answer)

        return server_answer

    def put(self, metric_name='', metric_value=0, timestamp=None):
        if timestamp == None:
            timestamp = str(int(time.time()))

        s = "put {key} {value} {timestamp}\n".format(key=metric_name, value=metric_value, timestamp=timestamp)
        try:
            self.sock.sendall(s.encode())
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        self.__reseived_data()

    def __extract_data(self, data, key):
        extract_data = {}
        data_list = data.split("\n")
        for item in data_list:
            if item != None:
                metric_name, metric_value, timestamp = item.split(" ")
                if metric_name in extract_data:
                    extract_data[metric_name].append((int(timestamp), float(metric_value)))
                else:
                    extract_data[metric_name] = [(int(timestamp), float(metric_value))]
        #extract_data = {data_list[i]:data_list[i + 3: i + 1 : -1] for i in range(0, len(data_list), 3)}
        return extract_data

    def get(self, key=None):
        if key == None:
            key = "*"
        s = "get {key}\n".format(key=key)
        try:
            self.sock.sendall(s.encode())
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        reseived_data = self.__reseived_data()
        if reseived_data == "":
            return {}

        extract_data = self.__extract_data(reseived_data, key)
        return extract_data

    def close(self):
        try:
            self.sock.close()
        except socket.error as err:
            raise ClientSocketError("error close connection", err)

def _main():
    client = Client("127.0.0.1", 10001, timeout=5)
    client.put("test", 0.5, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 0.5, timestamp=3)
    client.put("load", 3, timestamp=4)
    client.put("load", 4, timestamp=5)
    client.put("load", 4, timestamp=5)
    #print(client.get("test"))
    print(client.get("*"))

if __name__ == "__main__":
    _main()

