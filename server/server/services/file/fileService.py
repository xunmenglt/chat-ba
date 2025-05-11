from server.db.mapper.knowledge_file_mapper import select_file_by_id

def get_file_by_id(id):
    return select_file_by_id(id)