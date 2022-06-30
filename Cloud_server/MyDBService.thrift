namespace py MyDBService

service MyDBService{
    void create(1:string in_data)
     
    list<string> read()

    void update(1:i32 index, 2:string new_entry)

    void delete(1:string table_name, 2:i32 id)

    bool status_check()
}