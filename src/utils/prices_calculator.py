def get_prices(subtotal_sin_descuento: float, descuento: float, impuesto: float):
    subtotal_con_descuento = subtotal_sin_descuento * (1 - descuento)
    total = subtotal_con_descuento * (1 + impuesto)
    return subtotal_con_descuento, total