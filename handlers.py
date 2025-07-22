import re
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram import types
from config import DEFAULT_TIMEZONES
from db import set_timezone, get_timezone, get_all_timezones

TIME_REGEX = re.compile(r'\b([01]?\d|2[0-3]):([0-5]\d)\b')

async def cmd_settz(msg: types.Message):
    args = msg.text.split()
    if len(args) != 2:
        return await msg.reply("Usage: /settz Europe/Kyiv")

    tz = args[1]
    # try:
    ZoneInfo(tz)
    # except:
    #     return await msg.reply("Invalid timezone. Use `/listtzones` to see valid ones.")

    await set_timezone(msg.from_user.id, msg.from_user.username or "", tz)
    await msg.reply(f"Timezone set to {tz}")

async def cmd_settz_for(msg: types.Message):
    args = msg.text.split()
    if len(args) != 3:
        return await msg.reply("Usage: /settz_for @username Europe/Kyiv")

    username = args[1].lstrip("@")
    tz = args[2]

    try:
        ZoneInfo(tz)
    except:
        return await msg.reply("Invalid timezone name.")

    users = await get_all_timezones()
    matched = [(uid, name) for uid, name, _ in users if name == username]

    if not matched:
        return await msg.reply(f"User @{username} not found in DB yet.")

    user_id, _ = matched[0]
    await set_timezone(user_id, username, tz)
    await msg.reply(f"Timezone for @{username} updated to {tz}")

async def cmd_listtz(msg: types.Message):
    users = await get_all_timezones()
    if not users:
        return await msg.reply("No users have set their timezone yet.")

    lines = ["🌐 User timezones:"]
    for uid, name, tz in users:
        user_str = f"@{name}" if name else f"id:{uid}"
        lines.append(f"• {user_str}: {tz}")

    await msg.reply("\n".join(lines))

async def handle_time_mentions(msg: types.Message):
    if msg.text is None:
        return
    match = TIME_REGEX.search(msg.text)
    if not match:
        return

    hour, minute = int(match.group(1)), int(match.group(2))
    user_id = msg.from_user.id
    username = msg.from_user.username or ""

    tz_name = await get_timezone(user_id)
    if not tz_name:
        return await msg.reply("Please set your timezone first using /settz")

    try:
        base_tz = ZoneInfo(tz_name)
        now = datetime.now()
        base_dt = datetime(now.year, now.month, now.day, hour, minute, tzinfo=base_tz)
    except Exception as e:
        return await msg.reply("Error parsing time.")

    lines = ["🕒 Converted time:"]
    for tz in DEFAULT_TIMEZONES:
        try:
            converted = base_dt.astimezone(ZoneInfo(tz))
            lines.append(f"{tz}: {converted.strftime('%H:%M')}")
        except:
            continue

    await msg.reply("\n".join(lines), reply_to_message_id=msg.message_id)
