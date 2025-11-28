# src.adapter.entities.ciiu

class Ciiu:
    def __init__(self):
        self

    def impute_missing_ciiu(self, ciiu_code: str, valid_codes: set) -> str:
        if ciiu_code in valid_codes:
            return ciiu_code

        code = str(ciiu_code).strip()
        if not code.isdigit():
            return None
        
        group_prefix = code[:3]  # 1031 -> "103"
        group_matches = sorted([c for c in valid_codes if c.startswith(group_prefix)])
        if group_matches: return group_matches[0]  # 1030
        return None 

    ranges = [
        (100, 499, "AGROPECUARIO"),
        (500, 990, "MINERO"),
        (1000, 3330, "MANUFACTURA"),
        (3500, 3530, "ENERGETICO"),
        (3600, 3900, "AMBIENTALES"),
        (4100, 4390, "CONSTRUCCION"),
        (4500, 4799, "COMERCIO"),
        (4900, 5320, "TRANSPORTE"),
        (5500, 5630, "ALIMENTICIO"),
        (5800, 6399, "TIC"),
        (6400, 6630, "FINANCIERO"),
        (6800, 6820, "INMOBILIARIO"),
        (6900, 7500, "PROFESIONAL"),
        (7700, 8299, "SERVICIOS"),
        (8400, 8560, "EDUCATIVO"),
        (8600, 8890, "SALUD"),
        (9000, 9330, "CULTURAL"),
        (9400, 9999, "SERVICIOS"),
    ]