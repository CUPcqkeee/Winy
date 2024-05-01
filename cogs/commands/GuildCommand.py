import asyncio
import json

import disnake
from disnake import ModalInteraction
from disnake.ext import commands
from disnake.ui import Button

from main import db as db
from datetime import datetime, timezone, timedelta

cursor = db.cursor()

with open('./cogs/utils.json', "r", encoding='utf-8') as util:
    utils = json.load(util)

data = utils["Guild"]


class clanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.embed = Embeds()
        self.db = BD()
        self.buttons = Buttons(bot=bot)
        self.modal_cash = Modal_addcash()

        self.dev_guild_id = 847415392485376050
        self.pandorum_guild_d = 387409949442965506

        self.cupcqkee_id = 589492162211610662

        self.original_message = None

    @commands.slash_command(name="clan", guild_ids=[847415392485376050])
    async def clan(self, inter):
        pass

    @clan.sub_command(name="create", description="Создать клан | Стоимость: 20000")
    async def create(self,
                     inter,
                     name=commands.Param(name="название", description="Введите название вашего клана"),
                     color=commands.Param(name="цвет", description="Введите цвет клановой роли в HEX формате с '#'")):
        await self.bot.wait_until_ready()
        await inter.response.defer()

        def create_color(hexcolor):
            if not (color.startswith("#") and len(color) == 7):
                return "Неверный HEX формат"
            else:
                hex_color = color.lstrip("#")
                rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            return rgb_color

        guild_name = name.lower()
        check_name_clan = self.db.select_with(what="*", froms="Guild", where=f"`guild_name` = '{guild_name}'")
        print(inter.author.id)
        check_user_name = self.db.select_with(what="*", froms="Guild_member", where=f"`user_id` = '{inter.author.id}'")
        check_inter_balance = self.db.select_with(what="user_balance",
                                                  froms="Economy",
                                                  where=f"`user_id` = '{inter.author.id}'")
        if check_user_name:
            embed = self.embed.error(desc="У вас уже имеется клан или вы состоите в чьём-то клане",
                                     inter=inter)
            await inter.send(embed=embed)
        else:
            if check_inter_balance[0] >= 20000:
                if check_name_clan:
                    embed = self.embed.error(desc="Клан с таким названием уже существует!", inter=inter)
                    await inter.send(embed=embed)
                    return
                else:
                    guild = inter.guild
                    now = datetime.now(timezone(timedelta(hours=+3)))
                    d_time = now.strftime("%H:%M %d:%m:%Y")
                    times = int(now.timestamp())
                    if guild.id == self.dev_guild_id or guild.id == self.pandorum_guild_d:
                        rgb = create_color(hexcolor=color)
                        try:
                            role = await guild.create_role(name=name, color=disnake.Color.from_rgb(*rgb))
                        except BaseException:
                            embed = self.embed.error(desc="Вы не верно указали цвет",
                                                     inter=inter)
                            await inter.send(embed=embed, ephemeral=True)
                            return
                        cursor.execute(f"""SELECT MAX(`guild_id`) FROM `Guild`""")
                        max_guild_id = cursor.fetchone()
                        if max_guild_id[0] is not None:
                            await self.bot.wait_until_ready()
                            #
                            try:
                                self.db.insert_guild(guild_name=f"{name}",
                                                     guild_bank="0",
                                                     guild_type="OPEN",
                                                     guild_id=f"{int(max_guild_id[0]) + 1}",
                                                     date_create=f"{now}",
                                                     guild_count="25",
                                                     guild_owner=f"{inter.author.id}",
                                                     user_role=f"{role.id}",
                                                     guild_members_count="1",
                                                     guild_avatar=inter.author.avatar.url)

                                self.db.insert_guild_rank(guild_id=f"{int(max_guild_id[0]) + 1}")
                                self.db.insert_guild_member(guild_id=f"{int(max_guild_id[0]) + 1}",
                                                            user_role="1",
                                                            user_id=f"{inter.author.id}")
                                await asyncio.sleep(2)

                                self.db.update_economy(user_id=f"{inter.author.id}",
                                                       user_balance="20000")
                                await asyncio.sleep(2)
                                #
                                await inter.author.add_roles(role, reason="Создание клана")
                                embed = self.embed.information(field_name=f"Поздравляю с приобритением клана",
                                                               field_desc=f"\nИнформация о клане:"
                                                                          f"\n**Название**: `{name}`"
                                                                          f"\n**Роль клана**: {role.mention}"
                                                                          f"\n**Дата создания**: <t:{times}:R>"
                                                                          f"\n**Доступно слотов**: `24/25`",
                                                               inter=inter)
                                await inter.send(embed=embed)
                            except BaseException:
                                self.db.insert_guild(guild_name=f"{name}",
                                                     guild_bank="0",
                                                     guild_type="OPEN",
                                                     guild_id=f"{int(max_guild_id[0]) + 1}",
                                                     date_create=f"{now}",
                                                     guild_count="25",
                                                     guild_owner=f"{inter.author.id}",
                                                     user_role=f"{role.id}",
                                                     guild_members_count="1",
                                                     guild_avatar="NONE")
                                self.db.insert_guild_rank(guild_id=f"{int(max_guild_id[0]) + 1}")
                                self.db.insert_guild_member(guild_id=f"{int(max_guild_id[0]) + 1}",
                                                            user_role="1",
                                                            user_id=f"{inter.author.id}")
                                await asyncio.sleep(2)

                                self.db.update_economy(user_id=f"{inter.author.id}",
                                                       user_balance="20000")
                                await asyncio.sleep(2)
                                #
                                await inter.author.add_roles(role, reason="Создание клана")
                                embed = self.embed.information(field_name=f"Поздравляю с приобритением клана",
                                                               field_desc=f"\nИнформация о клане:"
                                                                          f"\n**Название**: `{name}`"
                                                                          f"\n**Роль клана**: {role.mention}"
                                                                          f"\n**Дата создания**: <t:{times}:R>"
                                                                          f"\n**Доступно слотов**: `24/25`",
                                                               inter=inter)
                                await inter.send(embed=embed)
                        else:
                            await self.bot.wait_until_ready()
                            try:
                                self.db.insert_guild(guild_name=f"{name}",
                                                     guild_bank="0",
                                                     guild_type="OPEN",
                                                     guild_id="1",
                                                     date_create=f"{now}",
                                                     guild_count="25",
                                                     guild_owner=f"{inter.author.id}",
                                                     user_role=f"{role.id}",
                                                     guild_members_count="1",
                                                     guild_avatar=f"{inter.author.avatar.url}")

                                self.db.insert_guild_rank(guild_id="1")
                                self.db.insert_guild_member(guild_id="1", user_id=f"{inter.author.id}", user_role="1")
                                await asyncio.sleep(2)

                                self.db.update_economy(user_id=f"{inter.author.id}",
                                                       user_balance="20000")
                                await asyncio.sleep(2)
                                #
                                await inter.author.add_roles(role, reason="Создание клана")
                                embed = self.embed.information(field_name=f"Поздравляю с приобритением клана",
                                                               field_desc=f"\nИнформация о клане:"
                                                                          f"\n**Название**: `{name}`"
                                                                          f"\n**Роль клана**: {role.mention}"
                                                                          f"\n**Дата создания**: <t:{times}:R>"
                                                                          f"\n**Доступно слотов**: `24/25`",
                                                               inter=inter)
                                await inter.send(embed=embed)
                            except BaseException:
                                self.db.insert_guild(guild_name=f"{name}",
                                                     guild_bank="0",
                                                     guild_type="OPEN",
                                                     guild_id="1",
                                                     date_create=f"{now}",
                                                     guild_count="25",
                                                     guild_owner=f"{inter.author.id}",
                                                     user_role=f"{role.id}",
                                                     guild_members_count="1",
                                                     guild_avatar="NONE")

                                self.db.insert_guild_rank(guild_id="1")
                                self.db.insert_guild_member(guild_id="1", user_id=f"{inter.author.id}", user_role="1")
                                await asyncio.sleep(2)

                                self.db.update_economy(user_id=f"{inter.author.id}",
                                                       user_balance="20000")
                                await asyncio.sleep(2)
                                #
                                await inter.author.add_roles(role, reason="Создание клана")
                                embed = self.embed.information(field_name=f"Поздравляю с приобритением клана",
                                                               field_desc=f"\nИнформация о клане:"
                                                                          f"\n**Название**: `{name}`"
                                                                          f"\n**Роль клана**: {role.mention}"
                                                                          f"\n**Дата создания**: <t:{times}:R>"
                                                                          f"\n**Доступно слотов**: `24/25`",
                                                               inter=inter)
                                await inter.send(embed=embed)
                    else:
                        return
            else:
                embed = self.embed.error(desc="У вас недостаточно денег", inter=inter)
                await inter.send(embed=embed)

    @clan.sub_command(name="manage", description="Открыть меню управления кланом")
    async def manage(self, inter):
        clan_member = self.db.select_with(what="*",
                                          froms="Guild_member",
                                          where=f"`user_id` = '{inter.author.id}'")

        clan = self.db.select_with(what="*",
                                   froms="Guild",
                                   where=f"`guild_id` = '{clan_member[0]}'")
        if clan_member[2] == "1":
            clan_member = data["Ranks"]["1"]
        elif clan_member[2] == "2":
            clan_member = data["Ranks"]["2"]
        elif clan_member[2] == "3":
            clan_member = data["Ranks"]["3"]
        elif clan_member[2] == "4":
            clan_member = data["Ranks"]["4"]
        elif clan_member[2] == "5":
            clan_member = data["Ranks"]["5"]

        embed = self.embed.information_clan(
            title=f"Меню управления кланом — {clan[0]}",
            field_desc=f"Название: **{clan[0]}**\n"
                       f"Участников: **{clan[8]}**\n"
                       f"Ранг: **{clan_member}**")
        try:
            embed.set_thumbnail(url=clan[9])
        except BaseException:
            pass

        button = self.buttons.phase_1_buttons()
        message = await inter.send(embed=embed, components=[button])
        self.original_message = message

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        message = self.original_message
        custom_id = inter.component.custom_id
        author = inter.message.interaction.user
        if inter.author == author:

            if custom_id == "next_page_phase_1":
                await inter.response.defer()
                new_buttons = self.buttons.phase_2_button()
                await inter.message.edit(components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "next_page_phase_2":
                await inter.response.defer()
                new_buttons = self.buttons.phase_3_button()
                await inter.message.edit(components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "prev_page_phase_2":
                await inter.response.defer()
                new_buttons = self.buttons.phase_1_buttons()
                await inter.message.edit(components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "prev_page_phase_3":
                await inter.response.defer()
                new_buttons = self.buttons.phase_2_button()
                await inter.message.edit(components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "cazna":
                await inter.response.defer()
                member_eco = self.db.select_with(what="*", froms="Economy", where=f"`user_id` = {inter.author.id}")
                member = self.db.select_with(what="*", froms="Guild_member", where=f"`user_id` = '{inter.author.id}'")
                guild = self.db.select_with(what="*", froms="Guild", where=f"`guild_id` = '{member[0]}'")
                embed = self.embed.money_guild_embed(guild=guild, user_money=member_eco[1])

                new_buttons = self.buttons.cazna()
                await inter.message.edit(embed=embed, components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "back":
                await inter.response.defer()
                clan_member = self.db.select_with(what="*",
                                                  froms="Guild_member",
                                                  where=f"`user_id` = '{inter.author.id}'")

                clan = self.db.select_with(what="*",
                                           froms="Guild",
                                           where=f"`guild_id` = '{clan_member[0]}'")
                if clan_member[2] == "1":
                    clan_member = data["Ranks"]["1"]
                elif clan_member[2] == "2":
                    clan_member = data["Ranks"]["2"]
                elif clan_member[2] == "3":
                    clan_member = data["Ranks"]["3"]
                elif clan_member[2] == "4":
                    clan_member = data["Ranks"]["4"]
                elif clan_member[2] == "5":
                    clan_member = data["Ranks"]["5"]

                embed = self.embed.information_clan(
                    title=f"Меню управления кланом — {clan[0]}",
                    field_desc=f"Название: **{clan[0]}**\n"
                               f"Участников: **{clan[8]}**\n"
                               f"Ранг: **{clan_member}**")
                try:
                    embed.set_thumbnail(url=clan[9])
                except BaseException:
                    pass

                new_buttons = self.buttons.phase_1_buttons()
                await inter.message.edit(embed=embed, components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "addcash":
                await inter.response.defer()
                await inter.response.send_modal(modal=self.modal_cash)
                await inter.edit_original_response()

            if custom_id == "members":
                await inter.response.defer()

                clan_member = self.db.select_with(what="*",
                                                  froms="Guild_member",
                                                  where=f"`user_id` = '{inter.author.id}'")

                clan = self.db.select_with(what="*",
                                           froms="Guild",
                                           where=f"`guild_id` = '{clan_member[0]}'")
                if clan_member[2] == "1":
                    clan_member = data["Ranks"]["1"]
                elif clan_member[2] == "2":
                    clan_member = data["Ranks"]["2"]
                elif clan_member[2] == "3":
                    clan_member = data["Ranks"]["3"]
                elif clan_member[2] == "4":
                    clan_member = data["Ranks"]["4"]
                elif clan_member[2] == "5":
                    clan_member = data["Ranks"]["5"]

                embed = self.embed.information_clan(
                    title=f"Меню управления участниками — {clan[0]}",
                    field_desc=f"Название: **{clan[0]}**\n"
                               f"Участников: **{clan[8]}**\n"
                               f"Ранг: **{clan_member}**")
                try:
                    embed.set_thumbnail(url=clan[9])
                except BaseException:
                    pass

                new_buttons = self.buttons.members()
                await inter.message.edit(components=[new_buttons])
                await inter.edit_original_response()

            if custom_id == "invites":
                await inter.response.defer()
                member = self.db.select_with(what="*", froms="Guild_member", where=f"`user_id` = '{inter.author.id}'")
                guild = self.db.select_with(what="*", froms="Guild", where=f"`guild_id` = '{member[0]}'")

                if member[2] == "1":
                    member = data["Ranks"]["1"]
                elif member[2] == "2":
                    member = data["Ranks"]["2"]
                elif member[2] == "3":
                    member = data["Ranks"]["3"]
                elif member[2] == "4":
                    member = data["Ranks"]["4"]
                elif member[2] == "5":
                    member = data["Ranks"]["5"]
                embed = self.embed.information_clan(title=f"Меню приглашения участников — {guild[0]}",
                                                    field_desc=f"Название: **{guild[0]}**\n"
                                                               f"Участников: **{guild[8]}**\n"
                                                               f"Ранг: **{member}**")

                try:
                    embed.set_thumbnail(url=guild[9])
                except BaseException:
                    pass

                new_buttons = self.buttons.invtes()
                await inter.message.edit(embed=embed, components=[new_buttons])
                await inter.edit_original_response()

    @clan.sub_command(name="online", description="Просмотр кланового онлайна")
    async def online(self, inter):
        pass

    @clan.sub_command(name="pofile", description="Просмотр кланового профиля")
    async def profile(self, inter):
            pass


class InviteMemberView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(InviteMember())


class InviteMember(disnake.ui.StringSelect):
    def __init__(self):
        dot = "<:ddddd:1191556735433977976>"
        options = [
            disnake.SelectOption(label='Moderator', description="Ответственные за модерацию в войсе", value='mod',
                                 emoji=f"{dot}"),
            disnake.SelectOption(label='Control', description="Ответственные за модерацию в чате", value='ctrl',
                                 emoji=f"{dot}"),
            disnake.SelectOption(label='TribuneMod', description="Ответственные за проведение трибуны", value='tbm',
                                 emoji=f"{dot}"),
            disnake.SelectOption(label='EventMod', description="Ответственные за проведение мероприятий",
                                 value='evm',
                                 emoji=f"{dot}"),
            disnake.SelectOption(label='Support', description="Ответственный за помощь по вопросам сервера",
                                 value='sup',
                                 emoji=f"{dot}")
        ]
        super().__init__(
            placeholder="Выберите интересующую вас должность",
            custom_id="choose_role",
            min_values=1,
            max_values=1,
            options=options
        )

    @disnake.ui.select(custom_id="choose_role", reconnect=True)
    async def callback(self, inter: disnake.MessageInteraction):
        selected_option = self.values[0]

        # if selected_option == 'mod':
        #     await inter.response.send_modal(modal=RecruitementModal(arg="538725888276168735"))


class Buttons:
    def __init__(self, bot):
        self.bot = bot

    def cazna(self):
        button = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="back",
                   label="Вернуться"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="addcash",
                   label="Пополнить казну")
        ]
        return button

    def phase_1_buttons(self):
        buttons = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="cazna",
                   label="Казна"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="members",
                   label="Участники"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="invites",
                   label="Приглашения"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="next_page_phase_1",
                   emoji="▶️")
        ]
        return buttons

    def invtes(self):
        button = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="back",
                   label="Вернуться"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="menu_manage_members",
                   label="Зайти в меню правления участниками")
        ]
        return button

    def members(self):
        button = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="back",
                   label="Вернуться"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="all_members",
                   label="Все участники"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="manage_members",
                   label="Управление участниками")
        ]
        return button

    def phase_2_button(self):
        buttons = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="prev_page_phase_2",
                   emoji="◀️"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="castomize",
                   label="Кастомизация"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="upgrade",
                   label="Улучшения"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="next_page_phase_2",
                   label="▶️")
        ]
        return buttons

    def phase_3_button(self):
        buttons = [
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="prev_page_phase_3",
                   emoji="◀️"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="infromation",
                   label="Информация"),
            Button(style=disnake.ButtonStyle.grey,
                   custom_id="settngs",
                   label="Настройки"),
            Button(style=disnake.ButtonStyle.red,
                   custom_id="leave",
                   label="Покинуть клан")
        ]
        return buttons


class Modal_addcash(disnake.ui.Modal):
    def __init__(self):
        self.db = BD()
        self.embed = Embeds()

        components = [
            disnake.ui.TextInput(
                label="Укажите сумму для пополнения казны",
                custom_id="amount",
                placeholder="Сумма должна быть целым числом",
                max_length=50,
                min_length=1
            )
        ]
        super().__init__(title=f"Пополнение казны", components=components, custom_id="addcash")

    async def callback(self, interaction: ModalInteraction, /) -> None:
        amount = interaction.text_values["amount"]
        if amount.isdigit():
            self.db.update_economy(user_id=interaction.author.id, user_balance=amount)
            cursor.execute(f"""UPDATE `Guild` SET `guild_bank` = `guild_bank` + '{amount}'""")
            db.commit()

            embed = self.embed.success(desc=f"Вы пополнили казну на {data['Economy']['currency']} ```{amount}```",
                                       inter=interaction)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = self.embed.error(desc="Вы указали не целое число!", inter=interaction)
            await interaction.send(embed=embed, ephemeral=True)
            return


class Embeds:
    def __init__(self):
        self.color = 0x2f3136

    def money_guild_embed(self, guild, user_money):
        embed = disnake.Embed(colour=self.color, title=f"Меню управления кланом — {guild[0]}")
        embed.add_field(name=f"{data['Economy']['currency']} В казне:",
                        value=f"```{guild[6]}```")
        embed.add_field(name=f"{data['Economy']['currency']} Ваш баланс:",
                        value=f"```{user_money}```")
        try:
            embed.set_thumbnail(url=f"{guild[9]}")
        except BaseException:
            pass
        print(guild[9])
        return embed

    def error(self, desc, inter):
        embed = disnake.Embed(colour=self.color)
        try:
            embed.set_author(name=f"Произошла ошибка!", url=inter.author.avatar.url)
            embed.add_field(name="",
                            value=desc)
        except BaseException:
            embed.set_author(name="Произошла ошибка")
            embed.add_field(name="",
                            value=desc)
        return embed

    def success(self, desc, inter):
        embed = disnake.Embed(colour=self.color)
        try:
            embed.set_author(name="Успех", url=inter.author.avatar.url)
            embed.add_field(name="",
                            value=desc)
        except BaseException:
            embed.set_author(name="Успех")
            embed.add_field(name="",
                            value=desc)
        return embed

    def information(self, field_name, field_desc, inter):
        embed = disnake.Embed(colour=self.color)
        try:
            embed.set_author(name=f"{inter.author.display_name}", icon_url=inter.author.avatar.url)
            embed.add_field(name=field_name, value=field_desc)
        except BaseException:
            embed.set_author(name=f"{inter.author.display_name}")
            embed.add_field(name=field_name, value=field_desc)

        return embed

    def information_clan(self, title, field_desc):
        embed = disnake.Embed(colour=self.color, title=title)
        embed.add_field(name="", value=field_desc)

        return embed


class BD:
    def select(self, what, froms):
        cursor.execute(f"""SELECT {what} FROM `{froms}`""")
        result = cursor.fetchall()
        return result

    def select_with(self, what, froms, where):
        cursor.execute(f"""SELECT {what} FROM `{froms}` WHERE {where}""")
        result = cursor.fetchone()
        return result

    def insert_guild(self, guild_name, guild_id, guild_owner, user_role, date_create, guild_count, guild_bank,
                     guild_type, guild_members_count, guild_avatar):
        cursor.execute(f"""INSERT INTO `Guild`(`guild_name`, `guild_id`, `guild_owner`, `user_role`, `date_create`, `guild_count`, `guild_bank`, `guild_type`, `guild_members_count`, `guild_avatar`)
     VALUES ('{guild_name}','{guild_id}','{guild_owner}','{user_role}','{date_create}','{guild_count}','{guild_bank}','{guild_type}', '{guild_members_count}', '{guild_avatar}')""")
        db.commit()

    def insert_guild_rank(self, guild_id):
        cursor.execute(
            f"""INSERT INTO `Guild_ranks`(`guild_id`, `guild_rank_1`, `guild_rank_2`, `guild_rank_3`, `guild_rank_4`, `guild_rank_5`) VALUES ('{guild_id}', '1', '2', '3', '4', '5')""")
        db.commit()

    def insert_guild_member(self, guild_id, user_id, user_role):
        cursor.execute(f"""INSERT INTO `Guild_member`(`guild_id`, `user_id`, `user_role`)
     VALUES ('{guild_id}','{user_id}','{user_role}')""")
        db.commit()

    def update_guild_member(self, user_role, user_id):
        cursor.execute(
            f"""UPDATE `Guild_member` SET `user_role`='{user_role}' WHERE `user_id` = '{user_id.author.id}'""")
        db.commit()

    def update_economy(self, user_id, user_balance):
        cursor.execute(
            f"""UPDATE `Economy` SET `user_balance`= `user_balance` - '{user_balance}' WHERE `user_id` = '{user_id}'""")
        db.commit()


def setup(bot):
    bot.add_cog(clanCommand(bot))
