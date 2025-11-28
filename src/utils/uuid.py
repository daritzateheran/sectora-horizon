import uuid

def generate_deterministic_id_name_based(obj: str) -> uuid.UUID:
    """
    Genera un UUID determinista basada en name.
    """
    return uuid.uuid5(uuid.NAMESPACE_DNS, obj.lower())