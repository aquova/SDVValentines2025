import asyncio
import functools
from typing import Callable, Coroutine, Sequence

import discord

from config import EVENT_ROLES

async def award_roles(user: discord.Member, guild_roles: Sequence[discord.Role]):
    for role_id in EVENT_ROLES:
        if not user.get_role(role_id):
            role = discord.utils.get(guild_roles, id=role_id)
            if role is not None:
                await user.add_roles(role)

def check_roles(user: discord.Member, valid_roles: list[int]) -> bool:
    for role in valid_roles:
        if user.get_role(role):
            return True
    return False

def to_thread(func: Callable) -> Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper
