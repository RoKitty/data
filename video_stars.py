import asyncio
import json

from roblox import Client
from roblox.members import Member
from roblox.utilities.iterators import SortOrder


async def main():
    client = Client()
    group = await client.get_group(4199740)  # Roblox Star Creators group
    target_role = None

    for role in await group.get_roles():
        if role.rank == 1:
            target_role = role
            break

    if not target_role:
        raise ValueError("couldn't find role")

    members: list[Member] = []

    async for page in target_role.get_members(
        page_size=100,
        sort_order=SortOrder.Descending
    ).pages():
        # use .pages() instead of .flatten() so we can give a progress indicator. maybe add this to ro.py one day?
        members.extend(page)
        percentage = 100 * (len(members) / target_role.member_count)
        print(f"{len(members)}/{target_role.member_count} ({percentage:.01f}%)")

    # export user info to CSV and IDs only to JSON. CSV for inspection, JSON for RoKitty ingest.
    with open("video_stars.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write("id,name,display_name\n")
        for member in members:
            csv_file.write(f"{member.id},{member.name},{member.display_name}\n")

    member_ids = [member.id for member in members]
    with open("video_star_ids.json", "w", encoding="utf-8") as json_file:
        json.dump(member_ids, json_file, indent=2)


if __name__ == '__main__':
    asyncio.run(main())
