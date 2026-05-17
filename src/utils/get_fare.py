import logging
from datetime import date

import httpx

from config import INVENTORY_SERVICE_URL
from error import RoomNotHavefee

logger = logging.getLogger(__name__)

class TarifaClient:
    def __init__(self):
        self.base_url = INVENTORY_SERVICE_URL

    def obtener_tarifa_vigente(
        self,
        habitacion_id: str,
        fecha: date,
    ) -> dict:
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(
                    f"{self.base_url}/api/v1/inventory/tarifas/vigente",
                    params={
                        "habitacion_id": habitacion_id,
                        "fecha": fecha.isoformat(),
                    },
                )

                response.raise_for_status()

                logger.info(
                    f"Tarifa vigente obtenida correctamente "
                    f"para habitacion_id={habitacion_id}, "
                    f"fecha={fecha.isoformat()}"
                )

                return response.json()

        except Exception as e:
            logger.warning(
                f"Error obteniendo tarifa vigente "
                f"(habitacion_id={habitacion_id}, "
                f"fecha={fecha.isoformat()}): {e}"
            )
            raise RoomNotHavefee()