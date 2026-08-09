from dao import SQLiteClient

if __name__ == "__main__":
    client = SQLiteClient(database="test.db", echo=False)
    client.add_user("alice", "vp001", 1)
    print(client.get_all_users())
