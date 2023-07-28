import re


def check_if_product_is_on_sale(product: dict) -> bool:
    pattern = r'\bSALE\b'
    if re.search(pattern, product['title'], re.IGNORECASE) or re.search(pattern, product['description'], re.IGNORECASE):
        return True
    return False