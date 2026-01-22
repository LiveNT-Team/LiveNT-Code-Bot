from typing import TypedDict


class Guild(TypedDict):
    id: int
    discord_gid: int
    developer_role_id: int
    main_admin_role_id: int
    admin_role_id: int
    major_admin_role_id: int
    minor_admin_role_id: int
    main_moder_role_id: int
    moder_role_id: int
    major_moder_role_id: int
    minor_moder_role_id: int
    greetings_enabled: bool
    greetings_channel_id: int
    ai_chat_enabled: bool
    ai_channel_id: int
