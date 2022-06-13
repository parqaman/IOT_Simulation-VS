namespace py MyDBService

service MyDBService{
    void create_table(1:string table_name)
     
    string read_data(1:string rows, 2:string table_name)

    void insert_data(1:string in_data)

    void delete_data(1:string table_name, 2:i32 id)
}