import os
import random
from typing import Optional

import discord
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID", "").strip()

if not DISCORD_TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN in your .env file.")


# -----------------------------
# CHOICES
# -----------------------------

ATTRIBUTE_CHOICES = [
    app_commands.Choice(name="Strength", value="Strength"),
    app_commands.Choice(name="Dexterity", value="Dexterity"),
    app_commands.Choice(name="Stamina", value="Stamina"),
    app_commands.Choice(name="Charisma", value="Charisma"),
    app_commands.Choice(name="Manipulation", value="Manipulation"),
    app_commands.Choice(name="Composure", value="Composure"),
    app_commands.Choice(name="Intelligence", value="Intelligence"),
    app_commands.Choice(name="Wits", value="Wits"),
    app_commands.Choice(name="Resolve", value="Resolve"),
]

PHYSICAL_SKILLS = [
    app_commands.Choice(name="Athletics", value="Athletics"),
    app_commands.Choice(name="Brawl", value="Brawl"),
    app_commands.Choice(name="Craft", value="Craft"),
    app_commands.Choice(name="Drive", value="Drive"),
    app_commands.Choice(name="Firearms", value="Firearms"),
    app_commands.Choice(name="Larceny", value="Larceny"),
    app_commands.Choice(name="Melee", value="Melee"),
    app_commands.Choice(name="Stealth", value="Stealth"),
    app_commands.Choice(name="Survival", value="Survival"),
]

SOCIAL_SKILLS = [
    app_commands.Choice(name="Animal Ken", value="Animal Ken"),
    app_commands.Choice(name="Etiquette", value="Etiquette"),
    app_commands.Choice(name="Insight", value="Insight"),
    app_commands.Choice(name="Intimidation", value="Intimidation"),
    app_commands.Choice(name="Leadership", value="Leadership"),
    app_commands.Choice(name="Performance", value="Performance"),
    app_commands.Choice(name="Persuasion", value="Persuasion"),
    app_commands.Choice(name="Streetwise", value="Streetwise"),
    app_commands.Choice(name="Subterfuge", value="Subterfuge"),
]

MENTAL_SKILLS = [
    app_commands.Choice(name="Academics", value="Academics"),
    app_commands.Choice(name="Awareness", value="Awareness"),
    app_commands.Choice(name="Finance", value="Finance"),
    app_commands.Choice(name="Investigation", value="Investigation"),
    app_commands.Choice(name="Medicine", value="Medicine"),
    app_commands.Choice(name="Occult", value="Occult"),
    app_commands.Choice(name="Politics", value="Politics"),
    app_commands.Choice(name="Science", value="Science"),
    app_commands.Choice(name="Technology", value="Technology"),
]

DISCIPLINE_CHOICES = [
    app_commands.Choice(name="Animalism", value="Animalism"),
    app_commands.Choice(name="Auspex", value="Auspex"),
    app_commands.Choice(name="Blood Sorcery", value="Blood Sorcery"),
    app_commands.Choice(name="Celerity", value="Celerity"),
    app_commands.Choice(name="Dominate", value="Dominate"),
    app_commands.Choice(name="Fortitude", value="Fortitude"),
    app_commands.Choice(name="Obfuscate", value="Obfuscate"),
    app_commands.Choice(name="Oblivion", value="Oblivion"),
    app_commands.Choice(name="Potence", value="Potence"),
    app_commands.Choice(name="Presence", value="Presence"),
    app_commands.Choice(name="Protean", value="Protean"),
    app_commands.Choice(name="Thin-Blood Alchemy", value="Thin-Blood Alchemy"),
]

ATTRIBUTE_DOTS = [
    app_commands.Choice(name="1 dot", value=1),
    app_commands.Choice(name="2 dots", value=2),
    app_commands.Choice(name="3 dots", value=3),
    app_commands.Choice(name="4 dots", value=4),
    app_commands.Choice(name="5 dots", value=5),
]

SKILL_DOTS = [
    app_commands.Choice(name="0 dots", value=0),
    app_commands.Choice(name="1 dot", value=1),
    app_commands.Choice(name="2 dots", value=2),
    app_commands.Choice(name="3 dots", value=3),
    app_commands.Choice(name="4 dots", value=4),
    app_commands.Choice(name="5 dots", value=5),
]

HUNGER_CHOICES = [
    app_commands.Choice(name="0 Hunger", value=0),
    app_commands.Choice(name="1 Hunger", value=1),
    app_commands.Choice(name="2 Hunger", value=2),
    app_commands.Choice(name="3 Hunger", value=3),
    app_commands.Choice(name="4 Hunger", value=4),
    app_commands.Choice(name="5 Hunger", value=5),
]

DIFFICULTY_CHOICES = [
    app_commands.Choice(name="No difficulty / count successes", value=0),
    app_commands.Choice(name="Difficulty 1", value=1),
    app_commands.Choice(name="Difficulty 2", value=2),
    app_commands.Choice(name="Difficulty 3", value=3),
    app_commands.Choice(name="Difficulty 4", value=4),
    app_commands.Choice(name="Difficulty 5", value=5),
    app_commands.Choice(name="Difficulty 6", value=6),
    app_commands.Choice(name="Difficulty 7", value=7),
    app_commands.Choice(name="Difficulty 8", value=8),
]

MODIFIER_CHOICES = [
    app_commands.Choice(name="-3 penalty", value=-3),
    app_commands.Choice(name="-2 penalty", value=-2),
    app_commands.Choice(name="-1 penalty", value=-1),
    app_commands.Choice(name="0 modifier", value=0),
    app_commands.Choice(name="+1 bonus", value=1),
    app_commands.Choice(name="+2 bonus", value=2),
    app_commands.Choice(name="+3 bonus", value=3),
    app_commands.Choice(name="+4 bonus", value=4),
    app_commands.Choice(name="+5 bonus", value=5),
]


# -----------------------------
# BOT SETUP
# -----------------------------

class VTMClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if DISCORD_GUILD_ID and DISCORD_GUILD_ID.isdigit():
            guild = discord.Object(id=int(DISCORD_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Synced commands to guild {DISCORD_GUILD_ID}.")
        else:
            await self.tree.sync()
            print("Synced global commands.")
            print("Tip: Add DISCORD_GUILD_ID to .env if you want commands to show faster in one server.")


client = VTMClient()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")


# -----------------------------
# VTM DICE LOGIC
# -----------------------------

def roll_vtm(pool: int, hunger: int, difficulty: int) -> dict:
    pool = max(pool, 1)
    hunger = max(0, min(hunger, 5, pool))

    hunger_count = hunger
    normal_count = pool - hunger_count

    normal_dice = [random.randint(1, 10) for _ in range(normal_count)]
    hunger_dice = [random.randint(1, 10) for _ in range(hunger_count)]

    all_dice = normal_dice + hunger_dice

    base_successes = sum(1 for die in all_dice if die >= 6)

    normal_tens = sum(1 for die in normal_dice if die == 10)
    hunger_tens = sum(1 for die in hunger_dice if die == 10)
    hunger_ones = sum(1 for die in hunger_dice if die == 1)

    total_tens = normal_tens + hunger_tens
    critical_pairs = total_tens // 2

    # In VTM 5e, a pair of 10s is a critical.
    # The two 10s already count as 2 successes.
    # Each critical pair adds 2 more successes, making that pair worth 4 total.
    total_successes = base_successes + (critical_pairs * 2)

    has_difficulty = difficulty > 0
    is_win = total_successes >= difficulty if has_difficulty else None

    messy_critical = bool(
        has_difficulty
        and is_win
        and critical_pairs > 0
        and hunger_tens > 0
    )

    bestial_failure = bool(
        has_difficulty
        and not is_win
        and hunger_ones > 0
    )

    critical_win = bool(
        has_difficulty
        and is_win
        and critical_pairs > 0
        and not messy_critical
    )

    if has_difficulty:
        if messy_critical:
            outcome = "🩸 Messy Critical"
            outcome_note = (
                "The roll succeeds with a critical, but at least one 10 was on a Hunger die. "
                "The Beast stains the victory."
            )
            color = discord.Color.dark_red()
        elif bestial_failure:
            outcome = "🐺 Bestial Failure"
            outcome_note = (
                "The roll fails and at least one Hunger die came up 1. "
                "The Beast lashes out."
            )
            color = discord.Color.red()
        elif critical_win:
            outcome = "✨ Critical Win"
            outcome_note = "The roll succeeds with a clean critical."
            color = discord.Color.gold()
        elif is_win:
            outcome = "✅ Win"
            outcome_note = "The roll meets or beats the Difficulty."
            color = discord.Color.green()
        else:
            outcome = "❌ Failure"
            outcome_note = "The roll does not meet the Difficulty."
            color = discord.Color.dark_gray()
    else:
        if critical_pairs > 0 and hunger_tens > 0:
            outcome = "🩸 Possible Messy Critical"
            outcome_note = (
                "A critical was rolled with a 10 on a Hunger die. "
                "If this roll counts as a success, treat it as a Messy Critical."
            )
            color = discord.Color.dark_red()
        elif critical_pairs > 0:
            outcome = "✨ Critical Rolled"
            outcome_note = (
                "A critical was rolled. No Difficulty was set, so the bot is only counting successes."
            )
            color = discord.Color.gold()
        elif hunger_ones > 0:
            outcome = "🐺 Possible Bestial Failure"
            outcome_note = (
                "A Hunger die rolled a 1. If this roll fails, it becomes a Bestial Failure."
            )
            color = discord.Color.red()
        else:
            outcome = "Successes Counted"
            outcome_note = "No Difficulty was set, so the bot is only counting total successes."
            color = discord.Color.blurple()

    return {
        "pool": pool,
        "hunger": hunger,
        "normal_dice": normal_dice,
        "hunger_dice": hunger_dice,
        "base_successes": base_successes,
        "successes": total_successes,
        "normal_tens": normal_tens,
        "hunger_tens": hunger_tens,
        "hunger_ones": hunger_ones,
        "critical_pairs": critical_pairs,
        "outcome": outcome,
        "outcome_note": outcome_note,
        "messy_critical": messy_critical,
        "bestial_failure": bestial_failure,
        "critical_win": critical_win,
        "color": color,
    }


def format_dice(dice: list[int]) -> str:
    if not dice:
        return "None"

    formatted = []

    for die in dice:
        if die == 10:
            formatted.append(f"**{die}**")
        elif die == 1:
            formatted.append(f"*{die}*")
        else:
            formatted.append(str(die))

    return ", ".join(formatted)


async def send_roll_result(
    interaction: discord.Interaction,
    title: str,
    pool: int,
    hunger: int,
    difficulty: int,
    modifier: int,
    breakdown: str,
    private: bool,
):
    result = roll_vtm(pool, hunger, difficulty)

    embed = discord.Embed(
        title=f"🩸 {title}",
        color=result["color"],
    )

    embed.add_field(name="Dice Pool", value=str(result["pool"]), inline=True)
    embed.add_field(name="Hunger", value=str(result["hunger"]), inline=True)
    embed.add_field(
        name="Difficulty",
        value="None" if difficulty == 0 else str(difficulty),
        inline=True,
    )

    embed.add_field(name="Breakdown", value=breakdown, inline=False)

    embed.add_field(
        name="Normal Dice",
        value=format_dice(result["normal_dice"]),
        inline=False,
    )

    embed.add_field(
        name="Hunger Dice",
        value=format_dice(result["hunger_dice"]),
        inline=False,
    )

    embed.add_field(name="Successes", value=str(result["successes"]), inline=True)
    embed.add_field(name="Critical Pairs", value=str(result["critical_pairs"]), inline=True)

    embed.add_field(
        name="Hunger Signs",
        value=(
            f"Hunger 10s: **{result['hunger_tens']}**\n"
            f"Hunger 1s: **{result['hunger_ones']}**"
        ),
        inline=True,
    )

    embed.add_field(
        name="Outcome",
        value=f"**{result['outcome']}**\n{result['outcome_note']}",
        inline=False,
    )

    if modifier != 0:
        embed.set_footer(text=f"Modifier applied: {modifier:+}")

    await interaction.response.send_message(embed=embed, ephemeral=private)


# -----------------------------
# SLASH COMMANDS
# -----------------------------

@client.tree.command(name="vphysical", description="Roll a VTM 5e Physical Skill test.")
@app_commands.describe(
    attribute="Choose the Attribute.",
    attribute_dots="Choose Attribute dots.",
    skill="Choose the Physical Skill.",
    skill_dots="Choose Skill dots.",
    hunger="Choose Hunger dice.",
    difficulty="Choose Difficulty, or no difficulty to count successes.",
    modifier="Extra bonus or penalty dice.",
    private="Show result only to you.",
)
@app_commands.choices(
    attribute=ATTRIBUTE_CHOICES,
    attribute_dots=ATTRIBUTE_DOTS,
    skill=PHYSICAL_SKILLS,
    skill_dots=SKILL_DOTS,
    hunger=HUNGER_CHOICES,
    difficulty=DIFFICULTY_CHOICES,
    modifier=MODIFIER_CHOICES,
)
async def vphysical(
    interaction: discord.Interaction,
    attribute: str,
    attribute_dots: int,
    skill: str,
    skill_dots: int,
    hunger: int,
    difficulty: int = 0,
    modifier: int = 0,
    private: bool = False,
):
    pool = attribute_dots + skill_dots + modifier
    breakdown = f"{attribute} {attribute_dots} + {skill} {skill_dots} + modifier {modifier:+}"
    await send_roll_result(
        interaction,
        "VTM Physical Roll",
        pool,
        hunger,
        difficulty,
        modifier,
        breakdown,
        private,
    )


@client.tree.command(name="vsocial", description="Roll a VTM 5e Social Skill test.")
@app_commands.describe(
    attribute="Choose the Attribute.",
    attribute_dots="Choose Attribute dots.",
    skill="Choose the Social Skill.",
    skill_dots="Choose Skill dots.",
    hunger="Choose Hunger dice.",
    difficulty="Choose Difficulty, or no difficulty to count successes.",
    modifier="Extra bonus or penalty dice.",
    private="Show result only to you.",
)
@app_commands.choices(
    attribute=ATTRIBUTE_CHOICES,
    attribute_dots=ATTRIBUTE_DOTS,
    skill=SOCIAL_SKILLS,
    skill_dots=SKILL_DOTS,
    hunger=HUNGER_CHOICES,
    difficulty=DIFFICULTY_CHOICES,
    modifier=MODIFIER_CHOICES,
)
async def vsocial(
    interaction: discord.Interaction,
    attribute: str,
    attribute_dots: int,
    skill: str,
    skill_dots: int,
    hunger: int,
    difficulty: int = 0,
    modifier: int = 0,
    private: bool = False,
):
    pool = attribute_dots + skill_dots + modifier
    breakdown = f"{attribute} {attribute_dots} + {skill} {skill_dots} + modifier {modifier:+}"
    await send_roll_result(
        interaction,
        "VTM Social Roll",
        pool,
        hunger,
        difficulty,
        modifier,
        breakdown,
        private,
    )


@client.tree.command(name="vmental", description="Roll a VTM 5e Mental Skill test.")
@app_commands.describe(
    attribute="Choose the Attribute.",
    attribute_dots="Choose Attribute dots.",
    skill="Choose the Mental Skill.",
    skill_dots="Choose Skill dots.",
    hunger="Choose Hunger dice.",
    difficulty="Choose Difficulty, or no difficulty to count successes.",
    modifier="Extra bonus or penalty dice.",
    private="Show result only to you.",
)
@app_commands.choices(
    attribute=ATTRIBUTE_CHOICES,
    attribute_dots=ATTRIBUTE_DOTS,
    skill=MENTAL_SKILLS,
    skill_dots=SKILL_DOTS,
    hunger=HUNGER_CHOICES,
    difficulty=DIFFICULTY_CHOICES,
    modifier=MODIFIER_CHOICES,
)
async def vmental(
    interaction: discord.Interaction,
    attribute: str,
    attribute_dots: int,
    skill: str,
    skill_dots: int,
    hunger: int,
    difficulty: int = 0,
    modifier: int = 0,
    private: bool = False,
):
    pool = attribute_dots + skill_dots + modifier
    breakdown = f"{attribute} {attribute_dots} + {skill} {skill_dots} + modifier {modifier:+}"
    await send_roll_result(
        interaction,
        "VTM Mental Roll",
        pool,
        hunger,
        difficulty,
        modifier,
        breakdown,
        private,
    )


@client.tree.command(name="vdiscipline", description="Roll a VTM 5e Discipline test.")
@app_commands.describe(
    attribute="Choose the Attribute.",
    attribute_dots="Choose Attribute dots.",
    discipline="Choose the Discipline.",
    discipline_dots="Choose Discipline dots.",
    hunger="Choose Hunger dice.",
    difficulty="Choose Difficulty, or no difficulty to count successes.",
    modifier="Extra bonus or penalty dice.",
    private="Show result only to you.",
)
@app_commands.choices(
    attribute=ATTRIBUTE_CHOICES,
    attribute_dots=ATTRIBUTE_DOTS,
    discipline=DISCIPLINE_CHOICES,
    discipline_dots=SKILL_DOTS,
    hunger=HUNGER_CHOICES,
    difficulty=DIFFICULTY_CHOICES,
    modifier=MODIFIER_CHOICES,
)
async def vdiscipline(
    interaction: discord.Interaction,
    attribute: str,
    attribute_dots: int,
    discipline: str,
    discipline_dots: int,
    hunger: int,
    difficulty: int = 0,
    modifier: int = 0,
    private: bool = False,
):
    pool = attribute_dots + discipline_dots + modifier
    breakdown = f"{attribute} {attribute_dots} + {discipline} {discipline_dots} + modifier {modifier:+}"
    await send_roll_result(
        interaction,
        "VTM Discipline Roll",
        pool,
        hunger,
        difficulty,
        modifier,
        breakdown,
        private,
    )


@client.tree.command(name="vcustom", description="Roll a custom VTM 5e dice pool.")
@app_commands.describe(
    pool="Total dice pool.",
    hunger="Choose Hunger dice.",
    difficulty="Choose Difficulty, or no difficulty to count successes.",
    modifier="Extra bonus or penalty dice.",
    label="Optional roll label.",
    private="Show result only to you.",
)
@app_commands.choices(
    hunger=HUNGER_CHOICES,
    difficulty=DIFFICULTY_CHOICES,
    modifier=MODIFIER_CHOICES,
)
async def vcustom(
    interaction: discord.Interaction,
    pool: int,
    hunger: int,
    difficulty: int = 0,
    modifier: int = 0,
    label: Optional[str] = "Custom Roll",
    private: bool = False,
):
    final_pool = pool + modifier
    breakdown = f"Custom pool {pool} + modifier {modifier:+}"
    await send_roll_result(
        interaction,
        f"VTM {label}",
        final_pool,
        hunger,
        difficulty,
        modifier,
        breakdown,
        private,
    )


# -----------------------------
# START BOT
# -----------------------------

client.run(DISCORD_TOKEN)