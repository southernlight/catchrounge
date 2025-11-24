class TableService:

    def __init__(self,table_repository):
        self.table_repository = table_repository

    def get_tables_info(self):
        return self.table_repository.find_all_tables()

    def get_table_info(self, table_num: int):
        table = self.table_repository.find_by_table_num(table_num)
        if table is None:
            return None
        return table

