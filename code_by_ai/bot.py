import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
import json
import asyncio
from typing import Dict, List, Optional, Tuple, Any, Union

DISCORD_TOKEN = '-'
API_URL = "-"
API_KEY = "-"
SETTINGS_FILE = 'server_settings.json'
TEMPLATES_FILE = 'default_templates.json'
CUSTOM_RESPONSES_FILE = 'custom_responses.json'
OWNER_IDS = [-]

class DataManager:
    @staticmethod
    def load_json(file: str, default: Dict) -> Dict:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=4, ensure_ascii=False)
            return default

    @staticmethod
    def save_json(file: str, data: Dict) -> None:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

class TemplateManager:
    def __init__(self):
        self._templates = DataManager.load_json(TEMPLATES_FILE, self._create_default_templates())
    
    def _create_default_templates(self) -> Dict:
        return {
            "personalities": {
                "assistant": "Будь лаконичным и полезным. Только суть.",
                "warm": "Отвечай тепло и с пониманием. Кратко, но с заботой.",
                "ideas": "Думай нестандартно. Предлагай яркие и свежие идеи.",
                "consultant": "Будь точным. Отвечай как эксперт, без воды.",
                "programmer": "Отвечай как опытный разработчик. Четко, по делу, с примерами.",
                "explorer": "Исследуй тему глубоко. Задавай уточняющие вопросы. Отвечай с интересом и стремлением к пониманию."
            }
        }
    
    def get_template(self, key: str) -> str:
        return self._templates.get(key, "")
    
    def get_personality(self, personality: str) -> str:
        return self._templates["personalities"].get(personality, self._templates["personalities"]["assistant"])
    
    def get_personalities(self) -> Dict[str, str]:
        return self._templates["personalities"]

class ServerSettingsManager:
    def __init__(self):
        self._settings = DataManager.load_json(SETTINGS_FILE, {})
        self._custom_responses = DataManager.load_json(CUSTOM_RESPONSES_FILE, {})
    
    def get_server_settings(self, guild_id: str) -> Dict:
        return self._settings.get(guild_id, {})
    
    def update_server_setting(self, guild_id: str, key: str, value: Any) -> None:
        if guild_id not in self._settings:
            self._settings[guild_id] = {}
        self._settings[guild_id][key] = value
        DataManager.save_json(SETTINGS_FILE, self._settings)
    
    def check_custom_response(self, question: str) -> Tuple[bool, Optional[str]]:
        question_lower = question.lower().strip()
        for pattern, response in self._custom_responses.items():
            if pattern.lower() in question_lower:
                return True, response
        return False, None
    
    def get_user_message_count(self, guild_id: str, user_id: str) -> int:
        """Получить количество сообщений пользователя на сервере"""
        settings = self.get_server_settings(guild_id)
        message_counts = settings.get("message_counts", {})
        return message_counts.get(user_id, 0)

    def increment_message_count(self, guild_id: str, user_id: str) -> int:
        """Увеличить счетчик сообщений пользователя и вернуть новое значение"""
        settings = self.get_server_settings(guild_id)
        
        if "message_counts" not in settings:
            settings["message_counts"] = {}
        
        if user_id not in settings["message_counts"]:
            settings["message_counts"][user_id] = 0
        
        settings["message_counts"][user_id] += 1
        
        # Сохраняем обновленные настройки
        self.update_server_setting(guild_id, "message_counts", settings["message_counts"])
        
        return settings["message_counts"][user_id]

class CustomAPI:
    def __init__(self, api_url: str, api_key: str, template_manager: TemplateManager):
        self.api_url = api_url
        self.api_key = api_key
        self.template_manager = template_manager
        self.explorer_conversations = {}
    
    async def ask(self, question: str, personality: str = "assistant", custom_prompt: Optional[str] = None) -> str:
        content_to_use = custom_prompt if custom_prompt else question
        instruction = self.template_manager.get_personality(personality)
        
        # Формируем сообщения для API
        messages = [
            {
                "role": "system",
                "content": instruction
            },
            {
                "role": "user", 
                "content": content_to_use
            }
        ]
        
        # Данные для отправки
        data = {
            "custom_key": self.api_key,
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=data, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        # Извлекаем текст из формата OpenAI
                        if isinstance(response_data, dict) and 'choices' in response_data:
                            if len(response_data['choices']) > 0:
                                return response_data['choices'][0]['message']['content']
                        return str(response_data)
                    else:
                        return f"Ошибка API: HTTP {response.status}"
        except Exception as e:
            print(f"API Error: {e}")
            return f"Ошибка соединения: {str(e)}"
    
    async def ask_explorer(self, question: str, user_id: int, channel_id: int, custom_prompt: Optional[str] = None) -> str:
        content_to_use = custom_prompt if custom_prompt else question
        conv_key = f"{user_id}_{channel_id}"
        if conv_key not in self.explorer_conversations:
            self.explorer_conversations[conv_key] = []
        
        # Формируем сообщения для контекста
        messages = [
            {
                "role": "system",
                "content": self.template_manager.get_personality("explorer")
            }
        ]
        
        # Добавляем историю разговора
        for exchange in self.explorer_conversations[conv_key]:
            messages.append({"role": "user", "content": exchange['question']})
            messages.append({"role": "assistant", "content": exchange['answer']})
        
        # Добавляем новый вопрос
        messages.append({"role": "user", "content": content_to_use})
        
        # Данные для отправки
        data = {
            "custom_key": self.api_key,
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=data, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        # Извлекаем текст из формата OpenAI
                        if isinstance(response_data, dict) and 'choices' in response_data:
                            if len(response_data['choices']) > 0:
                                response_text = response_data['choices'][0]['message']['content']
                            else:
                                response_text = str(response_data)
                        else:
                            response_text = str(response_data)
                        
                        # Сохраняем в историю
                        self.explorer_conversations[conv_key].append({
                            "question": content_to_use,
                            "answer": response_text
                        })
                        
                        # Оставляем только последние 5 сообщений
                        self.explorer_conversations[conv_key] = self.explorer_conversations[conv_key][-5:]
                        
                        return response_text
                    else:
                        return f"Ошибка API: HTTP {response.status}"
        except Exception as e:
            print(f"API Error: {e}")
            return f"Ошибка соединения: {str(e)}"

class Bot(commands.Bot):
    def __init__(self):
        # Убираем интент DIRECT_MESSAGES для защиты от DDoS через ЛС
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix='/', intents=intents)
        self.template_manager = TemplateManager()
        self.settings_manager = ServerSettingsManager()
        self.custom_api = CustomAPI(API_URL, API_KEY, self.template_manager)
    
    async def setup_hook(self):
        try:
            synced = await self.tree.sync()
            print(f"Синхронизировано {len(synced)} слеш-команд")
        except Exception as e:
            print(f"Ошибка синхронизации команд: {e}")
    
    async def on_ready(self):
        print(f'{self.user} подключен к Discord! ID: {self.user.id}')
        print(f'Интенты: {self.intents}')
        print(f'Бот работает только на серверах (без ЛС)')
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="-"
        ))
    
    async def process_message(self, message):
        if message.author.bot:
            return None
        
        # Проверяем, что сообщение с сервера (не из ЛС)
        if not message.guild:
            return None
        
        gid = str(message.guild.id)
        settings = self.settings_manager.get_server_settings(gid)
        personality = settings.get("personality", "assistant")

        content = message.content
        if self.user in message.mentions:
            content = content.replace(f'<@{self.user.id}>', '').strip()
        if not content:
            content = "Чем могу помочь?"

        has_custom, custom_prompt = self.settings_manager.check_custom_response(content)
        
        if personality == "explorer":
            response = await self.custom_api.ask_explorer(
                content, 
                message.author.id, 
                message.channel.id, 
                custom_prompt if has_custom else None
            )
        else:
            response = await self.custom_api.ask(
                content, 
                personality, 
                custom_prompt if has_custom else None
            )

        return response
    
    async def send_long_message(self, channel, content, reference=None):
        """Разбивает длинные сообщения на части и отправляет их"""
        if len(content) <= 1900:
            if reference:
                return await channel.send(content, reference=reference)
            else:
                return await channel.send(content)
        else:
            chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
            messages = []
            
            if reference:
                messages.append(await channel.send(chunks[0], reference=reference))
            else:
                messages.append(await channel.send(chunks[0]))
            
            for chunk in chunks[1:]:
                messages.append(await channel.send(chunk))
            
            return messages
    
    async def get_or_create_activist_role(self, guild):
        """Получает или создает роль Активист"""
        activist_role = discord.utils.get(guild.roles, name="Активист")
        
        if not activist_role:
            try:
                activist_role = await guild.create_role(
                    name="Активист",
                    color=discord.Color.gold(),
                    reason="Автоматически создана для активных участников"
                )
                print(f"Создана роль 'Активист' на сервере {guild.name}")
            except Exception as e:
                print(f"Ошибка при создании роли: {e}")
                return None
        
        return activist_role
    
    def has_no_server_role(self, member):
        """Проверяет, есть ли у пользователя роль 'Пиарится'"""
        no_server_role = discord.utils.get(member.guild.roles, name="Пиарится")
        if no_server_role:
            return no_server_role in member.roles
        return False
    
    async def check_and_assign_activist_role(self, message):
        """Проверяет и выдает роль Активист если нужно"""
        if not message.guild:
            return
        
        if self.has_no_server_role(message.author):
            return
        
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        message_count = self.settings_manager.increment_message_count(guild_id, user_id)
        
        if message_count >= 200:
            activist_role = await self.get_or_create_activist_role(message.guild)
            
            if activist_role and activist_role not in message.author.roles:
                try:
                    await message.author.add_roles(activist_role)
                    await message.channel.send(
                        f"🎉 Поздравляем, {message.author.mention}! Вы написали {message_count} сообщений "
                        f"и получаете роль **Активист**!"
                    )
                except discord.Forbidden:
                    print(f"Недостаточно прав для выдачи роли на сервере {message.guild.name}")
                except Exception as e:
                    print(f"Ошибка при выдаче роли: {e}")
    
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Игнорируем сообщения из ЛС
        if not message.guild:
            return
        
        await self.check_and_assign_activist_role(message)
            
        is_mentioned = self.user in message.mentions
        
        if not is_mentioned:
            settings = self.settings_manager.get_server_settings(str(message.guild.id))
            active_channels = settings.get("active_channels", [])
            if message.channel.id not in active_channels:
                return
        
        if is_mentioned or message.channel.id in self.settings_manager.get_server_settings(str(message.guild.id)).get("active_channels", []):
            async with message.channel.typing():
                response = await self.process_message(message)
                if response:
                    await self.send_long_message(message.channel, response, reference=message)
    
    async def on_member_join(self, member):
        try:
            settings = self.settings_manager.get_server_settings(str(member.guild.id))
            channel_id = settings.get('welcome_channel')
            if channel_id:
                channel = member.guild.get_channel(channel_id)
                if channel:
                    full_prompt = f"Перефразируй и не упоминай командную строку или shell: {member.name}, Привет! Добро пожаловать в LiveNT-Code! Очень рады, что ты с нами. Расскажи, что тебя здесь интересует больше всего? Чем увлекаешься, что хотел бы изучить?"
                    welcome_text = await self.custom_api.ask(full_prompt, "warm")
                    await channel.send(f'{member.mention}, {welcome_text}')
                    print(f"Отправлено приветствие для {member.name} в канале {channel.name}")
                else:
                    print(f"Канал приветствий {channel_id} не найден")
            else:
                print(f"Канал приветствий не настроен для сервера {member.guild.name}")
        except Exception as e:
            print(f"Ошибка при обработке нового участника: {e}")

def is_admin():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id in OWNER_IDS or interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)

bot = Bot()

@bot.tree.command(name="welcome", description="Установить канал приветствия")
@is_admin()
async def welcome(interaction: discord.Interaction, канал: discord.TextChannel):
    bot.settings_manager.update_server_setting(str(interaction.guild_id), "welcome_channel", канал.id)
    await interaction.response.send_message(f"Канал приветствий установлен: {канал.mention}")

@bot.tree.command(name="activate", description="Активировать бота в этом канале")
@is_admin()
async def activate(interaction: discord.Interaction):
    gid = str(interaction.guild_id)
    settings = bot.settings_manager.get_server_settings(gid)
    active_channels = settings.get("active_channels", [])
    if interaction.channel_id not in active_channels:
        active_channels.append(interaction.channel_id)
        bot.settings_manager.update_server_setting(gid, "active_channels", active_channels)
        await interaction.response.send_message(f"Бот активирован в канале: {interaction.channel.mention}")
    else:
        await interaction.response.send_message("Бот уже активирован в этом канале.")

@bot.tree.command(name="deactivate", description="Деактивировать бота в этом канале")
@is_admin()
async def deactivate(interaction: discord.Interaction):
    gid = str(interaction.guild_id)
    settings = bot.settings_manager.get_server_settings(gid)
    active_channels = settings.get("active_channels", [])
    if interaction.channel_id in active_channels:
        active_channels.remove(interaction.channel_id)
        bot.settings_manager.update_server_setting(gid, "active_channels", active_channels)
        await interaction.response.send_message(f"Бот деактивирован в канале: {interaction.channel.mention}")
    else:
        await interaction.response.send_message("Бот не активирован в этом канале.")

@bot.tree.command(name="personality", description="Изменить личность бота")
@is_admin()
@app_commands.choices(шаблон=[
    app_commands.Choice(name=key, value=key) 
    for key in ["assistant", "warm", "ideas", "consultant", "programmer", "explorer"]
])
async def personality_command(interaction: discord.Interaction, шаблон: app_commands.Choice[str]):
    bot.settings_manager.update_server_setting(str(interaction.guild_id), "personality", шаблон.value)
    await interaction.response.send_message(f"Личность бота установлена: {шаблон.name}")

@bot.tree.command(name="settings", description="Показать настройки сервера")
async def settings_command(interaction: discord.Interaction):
    settings = bot.settings_manager.get_server_settings(str(interaction.guild_id))
    embed = discord.Embed(title="Настройки сервера", color=discord.Color.green())
    
    welcome_channel_id = settings.get("welcome_channel", "Не установлен")
    if isinstance(welcome_channel_id, int):
        channel = interaction.guild.get_channel(welcome_channel_id)
        welcome_channel = channel.mention if channel else "Канал не найден"
    else:
        welcome_channel = "Не установлен"
    
    active_channels = settings.get("active_channels", [])
    if active_channels:
        active_channels_text = ", ".join([
            channel.mention if (channel := interaction.guild.get_channel(ch_id)) else str(ch_id) 
            for ch_id in active_channels
        ])
    else:
        active_channels_text = "Нет активных каналов"
    
    embed.add_field(name="Welcome канал", value=welcome_channel, inline=False)
    embed.add_field(name="Активные каналы", value=active_channels_text, inline=False)
    embed.add_field(name="Личность", value=settings.get("personality", "assistant"), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Список команд")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Команды бота", color=discord.Color.blue())
    embed.add_field(name="/welcome", value="Установить канал приветствий", inline=False)
    embed.add_field(name="/activate", value="Активировать бота в канале", inline=False)
    embed.add_field(name="/deactivate", value="Деактивировать бота", inline=False)
    embed.add_field(name="/personality", value="Изменить личность", inline=False)
    embed.add_field(name="/settings", value="Показать текущие настройки", inline=False)
    embed.add_field(name="/role", value="Показать количество сообщений участника", inline=False)
    embed.add_field(name="@Бот", value="Упомяните бота в сообщении, чтобы он ответил", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="role", description="Показать количество сообщений участника")
async def role_command(interaction: discord.Interaction, участник: Optional[discord.Member] = None):
    member = участник or interaction.user
    guild_id = str(interaction.guild_id)
    user_id = str(member.id)
    
    message_count = bot.settings_manager.get_user_message_count(guild_id, user_id)
    
    has_no_server_role = bot.has_no_server_role(member)
    
    activist_role = await bot.get_or_create_activist_role(interaction.guild)
    has_activist_role = activist_role in member.roles if activist_role else False
    
    if has_no_server_role:
        response = f"**{member.display_name}** написал(а) {message_count} сообщений, но имеет роль **Пиарится** и не может получить роль **Активист**."
    elif has_activist_role:
        response = f"**{member.display_name}** написал(а) {message_count} сообщений и имеет роль **Активист**."
    else:
        if message_count >= 200:
            if activist_role:
                try:
                    await member.add_roles(activist_role)
                    response = f"**{member.display_name}** написал(а) {message_count} сообщений и получает роль **Активист**!"
                except Exception as e:
                    print(f"Ошибка при выдаче роли: {e}")
                    response = f"**{member.display_name}** написал(а) {message_count} сообщений и может получить роль **Активист**, но произошла ошибка при выдаче."
            else:
                response = f"**{member.display_name}** написал(а) {message_count} сообщений, но не удалось создать роль **Активист**."
        else:
            remaining = 200 - message_count
            response = f"**{member.display_name}** написал(а) {message_count} сообщений. До роли **Активист** осталось {remaining} сообщений."
    
    await interaction.response.send_message(response)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)