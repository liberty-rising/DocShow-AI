def map_dtype(dtype):
    if "int" in dtype:
        return "INT"
    elif "float" in dtype:
        return "FLOAT"
    elif "object" in dtype:
        return "VARCHAR(255)"
    else:
        return "VARCHAR(255)"  # Default data type
    
