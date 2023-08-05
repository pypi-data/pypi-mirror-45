# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019 mathsman5133

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


import pytz


from dateutil import parser
from datetime import datetime


def try_enum(_class, data):
    if data is None:
        return None
    return _class(data=data)


class Clan:
    """Represents the most stripped down version of clan info.
    All other clan classes inherit this.

    Attributes
    ------------
    tag:
        :class:`str` - The clan tag
    name:
        :class:`str` - The clan name
    badge:
        :class:`Badge` - The clan badges
    """
    __slots__ = ('tag', 'name', 'badge', '_data')

    def __init__(self, *, data):
        self._data = data
        self.tag = data.get('tag')
        self.name = data.get('name')
        self.badge = try_enum(Badge, data.get('badgeUrls'))

    def __str__(self):
        return self.name

class BasicClan(Clan):
    """Represents a Basic Clan that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits :class:`Clan`, and thus all attributes
    of :class:`Clan` can be expected to be present.

    Attributes
    -----------
    location:
        :class:`Location` - The clan location
    level:
        :class:`int` - The clan level.
    points:
        :class:`int` - The clan trophy points.
    versus_points:
        :class:`int` - The clan versus trophy points.
    member_count:
        :class:`int` - The member count of the clan
    rank:
        :class:`int` - The clan rank for it's location this season
    previous_rank:
        :class:`int` - The clan rank for it's location in the previous season
    """
    __slots__ = ('location', 'level', 'points', 'versus_points',
                 'member_count', 'rank', 'previous_rank')

    def __init__(self, *, data):
        super().__init__(data=data)

        self.location = try_enum(Location, data.get('location', None))
        self.level = data.get('clanLevel', None)
        self.points = data.get('clanPoints', None)
        self.versus_points = data.get('clanVersusPoints', None)
        self.member_count = data.get('members', None)
        self.rank = data.get('rank')
        self.previous_rank = data.get('previous_rank')


class SearchClan(BasicClan):
    """Represents a Searched Clan that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits both :class:`Clan` and :class:`BasicClan`,
    and thus all attributes of these classes can be expected to be present.

    Attributes
    -----------
    type:
        :class:`str` - The clan type: open, closed, invite-only etc.
    required_trophies:
        :class:`int` - The required trophies to join
    war_frequency:
        :class:`str` - The war frequency of the clan
    war_win_streak:
        :class:`int` - The current war win streak of the clan
    war_wins:
        :class:`int` - The total war wins of the clan
    war_ties:
        :class:`int` - The total war ties of the clan
    war_losses:
        :class:`int` - The total war losses of the clan
    public_war_log:
        :class:`bool` - Indicates whether the war log is public
    description:
        :class:`str` - The clan description
    members:
        :class:`list` of :class:`BasicMember` - List of clan members
    """
    __slots__ = ('type', 'required_trophies', 'war_frequency', 'war_win_streak',
                 'war_wins', 'war_ties', 'war_losses', 'public_war_log',
                 'description', '_members')

    def __init__(self, *, data):
        self._members = {}
        super().__init__(data=data)

        self.type = data.get('type', None)
        self.required_trophies = data.get('requiredTrophies', None)
        self.war_frequency = data.get('warFrequency', None)
        self.war_win_streak = data.get('warWinStreak', None)
        self.war_wins = data.get('warWins', None)
        self.war_ties = data.get('warTies', None)
        self.war_losses = data.get('warLosses', None)
        self.public_war_log = data.get('isWarLogPublic', None)
        self.description = data.get('description')

        for mdata in data.get('memberList', []):
            self._add_member(BasicPlayer(data=mdata))

    def _add_member(self, data):
        self._members[data.tag] = data

    def get_member(self, tag):
        return self._members.get(tag)

    @property
    def members(self):
        return list(self._members.values())


class WarClan(Clan):
    """Represents a War Clan that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits :class:`Clan`, and thus all attributes
    of :class:`Clan` can be expected to be present.

    Attributes
    -----------
    members:
        :class:`list` of :class:`WarMember` - List of all clan members in war
    attacks:
        :class:`list` of :class:`WarAttack` - List of all attacks used this war
    defenses:
        :class:`list` of :class:`WarAttack` - List of all defenses by clan members this war
    attack_count:
        :class:`int` - Number of attacks by clan this war
    stars:
        :class:`int` - Number of stars by clan this war
    destruction:
        :class:`float` - Destruction as a percentage
    exp_earned:
        :class:`int` - Total XP earned by clan this war
    attacks_used:
        :class:`int` - Total attacks used by clan this war
    max_stars:
        :class:`int` - Total possible stars achievable
    """
    __slots__ = ('_war', '_members', '_attacks', '_defenses', 'level',
                 'attack_count', 'stars', 'destruction', 'exp_earned',
                 'attacks_used', 'total_attacks', 'max_stars')

    def __init__(self, *, data, war):

        self._war = war

        self._members = {}
        self._attacks = {}
        self._defenses = {}

        super(WarClan, self).__init__(data=data)

        self.level = data.get('clanLevel', None)
        self.attack_count = data.get('attacks', None)
        self.stars = data.get('stars', None)
        self.destruction = data.get('destructionPercentage', None)
        self.exp_earned = data.get('expEarned', None)

        self.attacks_used = data.get('attacks')
        self.total_attacks = self._war.team_size * 2
        self.stars = data.get('stars')
        self.max_stars = self._war.team_size * 3

        for mdata in data.get('members', []):
            member = WarMember(data=mdata, war=self._war)
            self._add_member(member)

    def _add_member(self, data):
        self._members[data.tag] = data

    def _add_attack(self, data):
        if data.attacker_tag in self._attacks.keys():
            self._attacks[data.attacker_tag].append(data)
        else:
            self._attacks[data.attacker_tag] = [data]

    def _add_defense(self, data):
        if data.defender_tag in self._defenses.keys():
            self._defenses[data.defender_tag].append(data)
        else:
            self._defenses[data.defender_tag] = [data]

    def _find_add_defender(self, data):
        defender_tag = data.defender_tag
        member = self._war.get_member(defender_tag)
        member._add_defense(data)

    def _load_attacks(self):
        for member in self._members:
            for attack in member.attacks:
                self._add_attack(attack)
                self._find_add_defender(attack)

    @property
    def members(self):
        return list(self._members.values())

    @property
    def attacks(self):
        return list(self._attacks.values())

    @property
    def defenses(self):
        return list(self._defenses.values())


class Player:
    """Represents the most stripped down version of a player.
    All other player classes inherit this.


    Attributes
    ------------
    tag:
        :class:`str` - The clan tag
    name:
        :class:`str` - The clan name
    """
    __slots__ = ('name', 'tag', '_data')

    def __init__(self, data):
        self._data = data
        self.name = data['name']
        self.tag = data.get('tag')

    def __str__(self):
        return self.name


class BasicPlayer(Player):
    """Represents a Basic Player that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits :class:`Player`, and thus all attributes
    of :class:`Player` can be expected to be present.

    Attributes
    -----------
    clan:
        :class:`Basic Clan` - The clan the member belongs to. May be ``None``
    level:
        :class:`int` - The player level.
    trophies:
        :class:`int` - The player's trophy count.
    versus_trophies:
        :class:`int` - The player's versus trophy count.
    role:
        :class:`str` - The members role in the clan - member, elder, etc.
    clan_rank:
        :class:`int` - The members clan rank
    clan_previous_rank
        :class:`int` - The members clan rank last season
    league_rank:
        :class:`int` - The player's current rank in their league for this season
    donations:
        :class:`int` - The members current donation count
    received:
        :class:`int` - The member's current donation received count
    attack_wins:
        :class:`int` - The players current attack wins for this season
    defense_wins:
        :class:`int` - The players current defense wins for this season
    """
    __slots__ = ('clan', 'level', 'league', 'trophies', 'versus_trophies', 'role',
                 'clan_rank', 'clan_previous_rank', 'league_rank', 'donations',
                 'received', 'attack_wins', 'defense_wins')

    def __init__(self, *, data, clan=None):
        super(BasicPlayer, self).__init__(data)

        self.clan = clan
        self.level = data.get('expLevel', None)
        self.league = try_enum(League, data.get('league', None))
        self.trophies = data.get('trophies', None)
        self.versus_trophies = data.get('versusTrophies', None)
        self.role = data.get('role', None)
        self.clan_rank = data.get('clanRank', None)
        self.clan_previous_rank = data.get('clanRank', None)
        self.league_rank = data.get('rank', None)
        self.donations = data.get('donations', None)
        self.received = data.get('donationsReceived', None)
        self.attack_wins = data.get('attackWins', None)
        self.defense_wins = data.get('defenseWins', None)

        if not self.clan:
            cdata = data.get('clan')
            if cdata:
                self.clan = BasicClan(data=cdata)


class WarMember(Player):
    """Represents a War Member that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits :class:`Player`, and thus all attributes
    of :class:`Player` can be expected to be present.


    Attributes
    -----------
    town_hall:
        :class:`int` - The members TH level
    map_position:
        :class:`int` - The members map position this war
    attacks:
        :class:`list` of :class:`WarAttack` - The member's attacks this war. Could be an empty list
    war:
        :class:`War` - The war this member belongs to
    """
    __slots__ = ('town_hall', 'map_position', 'attacks', 'war')

    def __init__(self, data, war):
        self.attacks = []

        super(WarMember, self).__init__(data)

        self.town_hall = data.get('townHallLevel', None)
        self.map_position = data.get('mapPosition', None)

        for adata in data.get('attacks', []):
            self.attacks.append(WarAttack(data=adata, war=war, member=self))


class SearchPlayer(BasicPlayer):
    """Represents a Searched Player that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.

    This class inherits both :class:`Player` and :class:`BasicPlayer`,
    and thus all attributes of these classes can be expected to be present

    Attributes
    -----------
    achievements:
        :class:`list` of :class:`Achievement` - List of the player's achievements
    troops:
        :class:`list` of :class:`Troop` - List of the player's troops
    heroes:
        :class:`list` of :class:`Hero` - List of the player's heroes
    spells:
        :class:`list` of :class:`Spell` - List of the player's spells
    best_trophies:
        :class:`int` - The players top trophy count
    best_versus_trophies:
        :class:`int` - The players top versus trophy count
    war_stars:
        :class:`int` - The players war star count
    town_hall:
        :class:`int` - The players TH level
    builder_hall:
        :class:`int` - The players BH level
    versus_attacks_wins:
        :class:`int` - The players total BH wins
    """
    __slots__ = ('_achievements', '_troops', '_heroes', '_spells',
                 'best_trophies', 'war_stars', 'town_hall',
                 'builder_hall', 'best_versus_trophies', 'versus_attacks_wins')

    def __init__(self, *, data):
        self._achievements = {}
        self._troops = {}
        self._heroes = {}
        self._spells = {}

        super(SearchPlayer, self).__init__(data=data)

        self._add_data(data)

    def _add_data(self, data):
        self.clan = try_enum(Clan, data.get('clan', None))
        self.best_trophies = data.get('bestTrophies', None)
        self.war_stars = data.get('warStars', None)
        self.town_hall = data.get('townHallLevel', None)
        self.builder_hall = data.get('builderHallLevel', None)
        self.best_versus_trophies = data.get('bestVersusTrophies', None)
        self.versus_attacks_wins = data.get('versusBattleWins', None)

        for adata in data.get('achievements', []):
            achievement = Achievement(data=adata, player=self)
            self._add_achievement(achievement)

        for tdata in data.get('troops', []):
            troop = Troop(data=tdata, player=self)
            self._add_troop(troop)

        for hdata in data.get('heroes', []):
            hero = Hero(data=hdata, player=self)
            self._add_hero(hero)

        for sdata in data.get('spells', []):
            spell = Spell(data=sdata, player=self)
            self._add_spell(spell)

    def _add_achievement(self, data):
        self._achievements[data.name] = data

    def _add_troop(self, data):
        self._troops[data.name] = data

    def _add_hero(self, data):
        self._heroes[data.name] = data

    def _add_spell(self, data):
        self._spells[data.name] = data

    @property
    def achievements(self):
        return list(self._achievements.values())

    @property
    def troops(self):
        return list(self._troops.values())

    @property
    def heroes(self):
        return list(self._heroes.values())

    @property
    def spells(self):
        return list(self._spells.values())


class BaseWar:
    """Represents the most basic Clash of Clans War

    Attributes
    -----------
    team_size:
        :class:`int` - The number of players per clan in war
    clan:
        :class:`WarClan` - The offensive clan
    opponent:
        :class:`WarClan` - The opposition clan
    """
    __slots__ = ('team_size', 'clan', 'opponent', '_data')

    def __init__(self, *, data):
        self._data = data
        self.team_size = data.get('teamSize', None)

        clan = data.get('clan', {})
        if clan and ('tag' in clan.keys()):
            # at the moment, if the clan is in notInWar, the API returns
            # 'clan' and 'opponent' as dicts containing only badge urls of
            # no specific clan. very strange

            self.clan = WarClan(data=clan, war=self)
        else:
            self.clan = None

        opponent = data.get('opponent', {})
        if opponent and ('tag' in opponent.keys()):
            # same problem as clan
            self.opponent = WarClan(data=opponent, war=self)
        else:
            self.opponent = None


class WarLog(BaseWar):
    """Represents a Clash of Clans War Log Entry

    This class inherits :class:`BaseWar`, and thus all attributes
    of :class:`BaseWar` can be expected to be present.

    Attributes
    -----------
    result:
        :class:`str` - The result of the war - `win` or `loss`
    end_time:
        :class:`Timestamp` - The end time of the war as a Timestamp object
    """
    __slots__ = ('result', 'end_time')

    def __init__(self, *, data):
        self.result = data.get('result')
        self.end_time = try_enum(Timestamp, data.get('endTime'))
        super(WarLog, self).__init__(data=data)


class CurrentWar(BaseWar):
    """Represents a Current Clash of Clans War

    This class inherits :class:`BaseWar`, and thus all attributes
    of :class:`BaseWar` can be expected to be present.

    Attributes
    -----------
    state:
        :class:`str` - The clan's current war state
    preparation_start_time:
        :class:`Timestamp` - The start time of preparation day as a Timestamp object
    start_time:
        :class:`Timestamp` - The start time of battle day as a Timestamp object
    end_time:
        :class:`Timestamp` - The end time of battle day day as a Timestamp object
    attacks: :class:`list` of :class:`WarAttack`
            A list of all attacks this war
    members: :class:`list` of :class:`WarMember`
            A list of all members this war
    """
    __slots__ = ('state', 'preparation_start_time',
                 'start_time', 'end_time')

    def __init__(self, *, data):
        self.state = data.get('state')
        self.preparation_start_time = try_enum(Timestamp, data.get('preparationStartTime'))
        self.start_time = try_enum(Timestamp, data.get('startTime'))
        self.end_time = try_enum(Timestamp, data.get('endTime'))

        super(CurrentWar, self).__init__(data=data)

    @property
    def attacks(self):
        a = [].extend(self.clan.attacks).extend(self.opponent.attacks)
        a.sort(key=lambda o: o.order)
        return a

    @property
    def members(self):
        m = [].extend(self.clan.members).extend(self.opponent.members)
        return m


class Achievement:
    """Represents a Clash of Clans Achievement.


    Attributes
    -----------
    player:
        :class:`SearchPlayer` - The player this achievement is assosiated with
    name:
        :class:`str` - The name of the achievement
    stars:
        :class:`int` - The current stars achieved for the achievement
    value:
        :class:`int` - The number of X things attained for this achievement
    target:
        :class:`int` - The number of X things required to complete this achievement
    info:
        :class:`str` - Information regarding the achievement
    completion_info:
        :class:`str` - Information regarding completion of the achievement
    village:
        :class:`str` - Either `home` or `builderBase`
    is_completed:
        :class:`bool` - Indicates whether the achievement is completed (3 stars achieved)
    is_home_base:
        :class:`bool` - Helper property to tell you if the achievement belongs to the home base
    is_builder_base:
        :class:`bool` - Helper property to tell you if the achievement belongs to the builder base
    """

    __slots__ = ('player', 'name', 'stars', 'value', 'target',
                 'info', 'completion_info', 'village', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.name = data['name']
        self.stars = data.get('stars')
        self.value = data['value']
        self.target = data['target']
        self.info = data['info']
        self.completion_info = data.get('completionInfo')
        self.village = data['village']

    @property
    def is_builder_base(self):
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        return self.village == 'home'

    @property
    def is_completed(self):
        return self.stars == 3


class Troop:
    """Represents a Clash of Clans Troop.

    Attributes
    -----------
    player:
        :class:`SearchPlayer` - player this troop is assosiated with
    name:
        :class:`str` - The name of the troop
    level:
        :class:`int` - The level of the troop
    max_level:
        :class:`int` - The overall max level of the troop, excluding townhall limitations
    village:
        :class:`str` - Either `home` or `builderBase`
    is_max:
        :class:`bool` - Indicates whether the troop is maxed overall, excluding townhall limitations
    is_home_base:
        :class:`bool` - Helper property to tell you if the troop belongs to the home base
    is_builder_base:
        :class:`bool` - Helper property to tell you if the troop belongs to the builder base
    """
    __slots__ = ('player', 'name', 'level',
                 'max_level', 'village', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.name = data['name']
        self.level = data['level']
        self.max_level = data['maxLevel']
        self.village = data['village']

    @property
    def is_max(self):
        return self.max_level == self.level

    @property
    def is_builder_base(self):
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        return self.village == 'home'


class Hero:
    """Represents a Clash of Clans Hero.

    Attributes
    -----------
    player:
        :class:`SearchPlayer` - The player this hero is assosiated with
    name:
        :class:`str` - The name of the hero
    level:
        :class:`int` - The level of the hero
    max_level:
        :class:`int` - The overall max level of the hero, excluding townhall limitations
    village:
        :class:`str` - Either `home` or `builderBase`
    is_max:
        :class:`bool` - Indicates whether the hero is maxed overall, excluding townhall limitations
    is_home_base:
        :class:`bool` - Helper property to tell you if the hero belongs to the home base
    is_builder_base:
        :class:`bool` - Helper property to tell you if the hero belongs to the builder base
    """
    __slots__ = ('player', 'name', 'level',
                 'max_level', 'village', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.name = data['name']
        self.level = data['level']
        self.max_level = data['maxLevel']
        self.village = data['village']

    @property
    def is_max(self):
        return self.level == self.max_level

    @property
    def is_builder_base(self):
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        return self.village == 'home'


class Spell:
    """Represents a Clash of Clans Spell.

    Attributes
    -----------
    player:
        :class:`SearchPlayer` - The player this spell is assosiated with
    name:
        :class:`str` - The name of the spell
    level:
        :class:`int` - The level of the spell
    max_level:
        :class:`int` - The overall max level of the spell, excluding townhall limitations
    village:
        :class:`str` - Either `home` or `builderBase`
    is_max:
        :class:`bool` - Indicates whether the spell is maxed overall, excluding townhall limitations
    is_home_base:
        :class:`bool` - Helper property to tell you if the spell belongs to the home base
    is_builder_base:
        :class:`bool` - Helper property to tell you if the spell belongs to the builder base
    """
    __slots__ = ('player', 'name', 'level',
                 'max_level', 'village', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.name = data['name']
        self.level = data['level']
        self.max_level = data['maxLevel']
        self.village = data['village']

    @property
    def is_max(self):
        return self.max_level == self.level

    @property
    def is_builder_base(self):
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        return self.village == 'home'


class WarAttack:
    """
    Represents a Clash of Clans War Attack

    Attributes
    -----------
    war:
        :class:`War` - The war this attack belongs to
    stars:
        :class:`int` - The stars achieved
    destruction:
        :class:`float` - The destruction achieved as a percentage (of 100)
    order:
        :class:`int` - The attack order in this war
    attacker_tag:
        :class:`int` - The attacker tag
    defender_tag:
        :class:`int` - The defender tag
    attacker:
        :class:`WarMember` - The attacker
    defender:
        :class:`WarMember` - The defender

    """
    __slots__ = ('war', 'member', 'stars',
                 'destruction', 'order',
                 'attacker_tag', 'defender_tag', '_data')

    def __init__(self, *, data, war, member):
        self._data = data

        self.war = war
        self.member = member
        self.stars = data['stars']
        self.destruction = data['destructionPercentage']
        self.order = data['order']
        self.attacker_tag = data['attackerTag']
        self.defender_tag = data['defenderTag']

    @property
    def attacker(self):
        return self.war.get_member(self.attacker_tag)

    @property
    def defender(self):
        return self.war.get_member(self.defender_tag)


class Location:
    """Represents a Clash of Clans Location

    Attributes
    -----------
    id:
        :class:`str` - The location ID
    name:
        :class:`str` - The location name
    is_country:
        :class:`bool` - Indicates whether the location is a country
    country_code:
        :class:`str` - The shorthand country code, if the location is a country
    """
    __slots__ = ('id', 'name', 'is_country', 'country_code', '_data')

    def __init__(self, *, data):
        self._data = data

        self.id = data.get('id')
        self.name = data.get('name')
        self.is_country = data.get('isCountry')
        self.country_code = data.get('countryCode')

    def __str__(self):
        return self.name


class League:
    """Represents a Clash of Clans League

    Attributes
    -----------
    id:
        :class:`str` - The league ID
    name:
        :class:`str` - The league name
    badge:
        :class:`Badge` - The league badge
    """
    __slots__ = ('id', 'name', 'badge', '_data')

    def __init__(self, *, data):
        self._data = data

        self.id = data.get('id')
        self.name = data.get('name')
        self.badge = try_enum(Badge, data=data.get('iconUrls', None))

    def __str__(self):
        return self.name


class LeagueRankedPlayer(BasicPlayer):
    """Represents a Clash of Clans League Ranked Player.
    Note that league season information is available only for Legend League.

    This class inherits both :class:`Player` and :class:`BasicPlayer`,
    and thus all attributes of these classes can be expected to be present.


    Attributes
    -----------
    rank:
        :class:`int` - The players rank in their league for this season
    """
    def __init__(self, *, data):
        self.rank = data.get('rank', None)
        super(LeagueRankedPlayer, self).__init__(data=data)


class Season:
    """Represents a Clash of Clans Player's Season.

    rank: """
    __slots__ = ('rank', 'trophies', 'id')

    def __init__(self, *, data):
        self.rank = data['rank']
        self.trophies = data['trophies']
        self.id = data['id']


class LegendStatistics:
    """Represents the Legend Statistics for a player.

    Attributes
    -----------
    player:
        :class:`Player` - The player
    legend_trophies:
        :class:`int` - The player's legend trophies
    current_season:
        :class:`int` - Legend trophies for this season
    previous_season:
        :class:`int` - Legend trophies for the previous season
    best_season:
        :class:`int` - Legend trophies for the player's best season
    """
    __slots__ = ('player', 'legend_trophies', 'current_season',
                 'previous_season', 'best_season', '_data')

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.legend_trophies = data['legendTrophies']
        self.current_season = try_enum(Season, data=data.get('currentSeason', None))
        self.previous_season = try_enum(Season, data=data.get('previousSeason', None))
        self.best_season = try_enum(Season, data=data.get('bestSeason', None))


class Badge:
    """Represents a Clash Of Clans Badge.

    Attributes
    -----------
    small:
        :class:`str` - URL for a small sized badge
    medium:
        :class:`str` - URL for a medium sized badge
    large:
        :class:`str` - URL for a large sized badge
    url:
        :class:`str` - Medium, the default URL badge size
    """
    __slots__ = ('small', 'medium', 'large', 'url', '_data')

    def __init__(self, *, data):
        # self._http = http
        self._data = data

        self.small = data.get('small')
        self.medium = data.get('medium')
        self.large = data.get('large')

        self.url = self.medium

    async def save(self, fp, size=None):
        """This funtion is a coroutine. Save this badge as a file-like object.

        :param fp: :class:`os.PathLike`
                    The filename to save the badge to
        :param size: Optional[:class:`str`] Either `small`, `medium` or `large`. The default is `medium`

        :raise HTTPException: Saving the badge failed

        :raise NotFound: The url was not found

        :return: :class:`int` The number of bytes written
        """
        sizes = {'small': self.small,
                 'medium': self.medium,
                 'large': self.large}

        if size and size in sizes.keys():
            url = sizes[size]
        else:
            url = self.medium

        # data = self._http.get_data_from_url(url)
        #
        # with open(fp, 'wb') as f:
        #     return f.write(data)


class Timestamp:
    """Represents a Clash of Clans Timestamp

    Attributes
    -----------
    utc_timestamp:
        :class:`datetime` - The timestamp as a UTC datetime object
    now:
        :class:`datetime` - The time in UTC now as a datetime object
    seconds_until:
        :class:`int` - Number of seconds until the timestamp. This may be negative.
    """
    __slots__ = ('time', '_data')

    def __init__(self, *, data):
        self._data = data

        self.time = data

    @property
    def utc_timestamp(self):
        utc = pytz.UTC
        parse = parser.parse(self.time)

        in_utc = parse.replace(tzinfo=utc)

        return in_utc

    @property
    def now(self):
        utc = pytz.UTC
        parse = datetime.utcnow()

        in_utc = parse.replace(tzinfo=utc)

        return in_utc

    @property
    def seconds_until(self):
        delta = self.utc_timestamp - self.now
        return delta.total_seconds()


class LeaguePlayer:
    """Represents a Clash of Clans League Player

    Attributes
    -----------
    tag:
        :class:`str` - The player's tag
    name:
        :class:`str` - The player's name
    town_hall:
        :class:`int` - The player's town hall level"""

    __slots__ = ('tag', 'name', 'town_hall', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data):
        self._data = data

        self.tag = data.get('tag')
        self.name = data.get('name')
        self.town_hall = data.get('townHall')


class LeagueClan(BasicClan):
    """Represents a Clash of Clans League Clan

    This class inherits both :class:`Clan` and :class:`BasicClan`,
    and thus all attributes of these classes can be expected to be present.

    Attributes
    -----------
    members:
        :class:`list` of :class:`LeaguePlayer` A list of players participating in this league season
    """
    def __init__(self, *, data):
        self._members = {}

        super(LeagueClan, self).__init__(data=data)

        for mdata in data.get('members', []):
            self._add_member(LeaguePlayer(data=mdata))

    def _add_member(self, data):
        self._members[data.tag] = data

    @property
    def members(self):
        return list(self._members.values())


class LeagueGroup:
    """Represents a Clash of Clans League Group

    Attributes
    -----------
    state:
        :class:`str` - The current state of the league group (`inWar`, `preparation` etc.)
    season:
        :class:`str` - The current season of the league group
    clans:
        :class:`list` of :class:`LeagueClan` A list of participating clans
    rounds:
        :class:`list` of :class:`list` - A list of lists containing all war tags for each round
    """
    __slots__ = ('state', 'season', '_clans', '_rounds', '_data')

    def __init__(self, *, data):
        self._data = data

        self._clans = {}
        self._rounds = []
        self.state = data.get('state', None)
        self.season = data.get('season', None)

        for cdata in data.get('clans', []):
            self._add_clan(LeagueClan(data=cdata))

        for rdata in data.get('rounds', []):
            self._add_round(rdata)

    def _add_clan(self, data):
        self._clans[data.tag] = data

    def _add_round(self, data):
        self._rounds.append(data['warTags'])

    @property
    def clans(self):
        return list(self._clans.values())

    @property
    def rounds(self):
        return self._rounds


class LeagueWar(CurrentWar):
    """Represents a Clash of Clans LeagueWar

    This class inherits both :class:`BaseWar` and :class:`CurrentWar`,
    and thus all attributes of these classes can be expected to be present.

    Attributes
    -----------
    tag:
        :class:`str` - The war tag
    """
    def __init__(self, *, data):
        self.tag = data.get('tag', None)
        super(LeagueWar, self).__init__(data=data)


class LeagueWarLogEntry:
    """Represents a Clash of Clans War Log entry for a League Season

    Attributes
    -----------
    end_time:
        :class:`Timestamp` - The end time of the war as a Timestamp object
    team_size:
        :class:`int` - The number of players per clan in war
    clan:
        :class:`Clan` - The offensive clan. Note this is only a :class:`Clan`, unlike that of a :class:`WarLog`
    enemy_stars:
        :class:`int` - Total enemy stars for all wars
    attack_count:
        :class:`int` - The total attacks completed by your clan over all wars
    stars:
        :class:`int` The total stars by your clan over all wars
    destruction:
        :class:`float` - The total destruction by your clan over all wars
    clan_level:
        :class:`int` - Your clan level.
    """

    __slots__ = ('end_time', 'team_size', 'clan', 'enemy_stars',
                 'attack_count', 'stars', 'destruction', 'clan_level')

    def __init__(self, *, data):
        self.end_time = try_enum(Timestamp, data.get('endTime'))
        self.team_size = data.get('teamSize')
        self.clan = try_enum(Clan, data.get('clan'))
        try:
            self.enemy_stars = data['opponent']['stars']
        except KeyError:
            self.enemy_stars = None

        if self.clan:
            self.attack_count = self.clan._data.get('attacks')
            self.stars = self.clan._data.get('stars')
            self.destruction = self.clan._data.get('destructionPercentage')
            self.clan_level = self.clan._data.get('clanLevel')
