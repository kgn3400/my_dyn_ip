""" ------------------------------------------------------------------
# File name : my_dyn_ip_api.py
# Copyright 2023 KGN Data. All rights reserved.
# ------------------------------------------------------------------"""

import asyncio
from dataclasses import dataclass

from aiohttp.client import ClientSession
import async_timeout

from homeassistant.core import ServiceCall

from datetime import datetime, timedelta


# ------------------------------------------------------------------
# ------------------------------------------------------------------
@dataclass
class MyDynIpApi:
    """My dyn ip interface"""

    def __init__(
        self,
        session: ClientSession | None,
    ) -> None:
        self.session: ClientSession | None = session
        self.request_timeout: int = 5
        self.close_session: bool = False
        self.changed: bool = False
        self.ip: str = ""
        self._clear_changed_at: datetime = datetime.now()

    # ------------------------------------------------------------------
    async def reset_service(self, call: ServiceCall) -> None:
        """My dyn ip service interface"""
        self.changed = False

    # ------------------------------------------------------------------
    async def update_service(self, call: ServiceCall) -> None:
        """My dyn ip service interface"""
        await self.update()

    # ------------------------------------------------------------------
    async def update(self) -> None:
        """My dyn ip interface"""

        if self.changed and self._clear_changed_at < datetime.now():
            self.changed = False

        if self.session is None:
            self.session = ClientSession()
            self.close_session = True

        tmp_ip: str = await self._get_ip()

        if self.ip == "":
            self.ip = tmp_ip

        elif tmp_ip != self.ip:
            self.ip = tmp_ip
            self._clear_changed_at = datetime.now() + timedelta(hours=24)
            self.changed = True

        if self.session and self.close_session:
            await self.session.close()

    # ------------------------------------------------------
    async def _get_ip(self) -> str:
        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request("GET", "https://ident.me")  # type: ignore
                return await response.text()

        except asyncio.TimeoutError:
            pass
        return ""
