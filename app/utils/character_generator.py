import random
import json
from enum import Enum
from typing import List, Dict, Tuple, Optional

from utils import client
from utils.query import generate_image


class CharacterRace(Enum):
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"
    ORC = "orc"
    GOBLIN = "goblin"
    HALFLING = "halfling"
    GNOME = "gnome"
    DRAGONBORN = "dragonborn"
    TIEFLING = "tiefling"
    ANIMAL = "anthropomorphic animal"
    ROBOT = "robot"
    ALIEN = "alien"
    FAIRY = "fairy"
    ANGEL = "angel"
    DEMON = "demon"
    VAMPIRE = "vampire"
    WEREWOLF = "werewolf"
    MERMAID = "mermaid"
    CENTAUR = "centaur"
    SATYR = "satyr"


class CharacterClass(Enum):
    WIZARD = "wizard"
    WARRIOR = "warrior"
    ROGUE = "rogue"
    CLERIC = "cleric"
    PALADIN = "paladin"
    RANGER = "ranger"
    BARD = "bard"
    DRUID = "druid"
    MONK = "monk"
    NECROMANCER = "necromancer"
    HUNTER = "hunter"
    KNIGHT = "knight"
    SAMURAI = "samurai"
    NINJA = "ninja"
    PIRATE = "pirate"
    ASTRONAUT = "astronaut"
    SCIENTIST = "scientist"
    DETECTIVE = "detective"
    CHEF = "chef"
    MERCHANT = "merchant"


class HairColor(Enum):
    BLACK = "black"
    BROWN = "brown"
    BLONDE = "blonde"
    RED = "red"
    GINGER = "ginger"
    WHITE = "white"
    GRAY = "gray"
    SILVER = "silver"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    PINK = "pink"
    RAINBOW = "rainbow-colored"
    TEAL = "teal"
    AUBURN = "auburn"
    OMBRE = "ombre"
    GOLD = "golden"
    COPPER = "copper"
    PLATINUM = "platinum"
    BALD = "bald"


class HairStyle(Enum):
    SHORT = "short"
    LONG = "long"
    CURLY = "curly"
    STRAIGHT = "straight"
    WAVY = "wavy"
    BRAIDED = "braided"
    PONYTAIL = "ponytail"
    MOHAWK = "mohawk"
    AFRO = "afro"
    DREADLOCKS = "dreadlocks"
    BALD = "bald"
    UNDERCUT = "undercut"
    PIXIE = "pixie cut"
    BOB = "bob cut"
    BUN = "bun"
    PIGTAILS = "pigtails"
    MULLET = "mullet"
    SHAVED_SIDES = "shaved sides"
    BOWL_CUT = "bowl cut"
    SPIKY = "spiky"


class FacialFeature(Enum):
    STRONG_JAW = "strong jaw"
    ROUND_FACE = "round face"
    ANGULAR_FACE = "angular face"
    HIGH_CHEEKBONES = "high cheekbones"
    LARGE_EYES = "large eyes"
    SMALL_EYES = "small eyes"
    HOODED_EYES = "hooded eyes"
    MONOLID = "monolid eyes"
    FULL_LIPS = "full lips"
    THIN_LIPS = "thin lips"
    SHARP_NOSE = "sharp nose"
    BUTTON_NOSE = "button nose"
    BROAD_NOSE = "broad nose"
    STRONG_BROW = "strong brow"
    DIMPLES = "dimples"
    FRECKLES = "freckles"
    SCARS = "facial scars"
    BEARD = "beard"
    MUSTACHE = "mustache"
    CLEAN_SHAVEN = "clean-shaven"


class EyeColor(Enum):
    BROWN = "brown"
    BLUE = "blue"
    GREEN = "green"
    HAZEL = "hazel"
    GRAY = "gray"
    AMBER = "amber"
    BLACK = "black"
    RED = "red"
    PURPLE = "purple"
    GOLD = "gold"
    SILVER = "silver"
    HETEROCHROMIA = "heterochromia (two different colors)"
    VIOLET = "violet"
    TEAL = "teal"
    YELLOW = "yellow"
    WHITE = "white"
    PINK = "pink"
    ORANGE = "orange"
    NEON = "neon"
    GLOWING = "glowing"


class Background(Enum):
    FOREST = "forest"
    MOUNTAINS = "mountains"
    DESERT = "desert"
    OCEAN = "ocean"
    CITY = "city"
    VILLAGE = "village"
    CASTLE = "castle"
    DUNGEON = "dungeon"
    TAVERN = "tavern"
    BATTLEFIELD = "battlefield"
    LIBRARY = "library"
    LABORATORY = "laboratory"
    SPACESHIP = "spaceship"
    VOID = "void"
    HEAVEN = "heavenly realm"
    HELL = "hellish realm"
    MARKET = "marketplace"
    GARDEN = "garden"
    RUINS = "ancient ruins"
    JUNGLE = "jungle"


class EmotionalState(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    THOUGHTFUL = "thoughtful"
    CONFUSED = "confused"
    EXCITED = "excited"
    FEARFUL = "fearful"
    PROUD = "proud"
    NEUTRAL = "neutral"
    SMUG = "smug"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    LOVING = "loving"
    DETERMINED = "determined"
    ANXIOUS = "anxious"
    CONFIDENT = "confident"
    EMBARRASSED = "embarrassed"
    BORED = "bored"
    CURIOUS = "curious"
    SUSPICIOUS = "suspicious"


class CharacterGenerator:
    def __init__(self):
        """Initialize the character generator with random attributes"""
        # Select random character attributes
        self.race = random.choice(list(CharacterRace))
        self.character_class = random.choice(list(CharacterClass))
        self.hair_color = random.choice(list(HairColor))
        self.hair_style = random.choice(list(HairStyle))
        self.facial_feature = random.choice(list(FacialFeature))
        self.eye_color = random.choice(list(EyeColor))
        self.background = random.choice(list(Background))

        # Default emotional state
        self.emotional_state = random.choice(list(EmotionalState))

        # Select 1-3 additional facial features
        all_facial_features = list(FacialFeature)
        self.additional_features = random.sample(
            all_facial_features,
            k=min(random.randint(1, 3), len(all_facial_features))
        )

        # If the main facial feature is in additional features, remove it
        if self.facial_feature in self.additional_features:
            self.additional_features.remove(self.facial_feature)

        # Store the character name (can be set later)
        self.name = None

        # Determine voice based on character attributes
        self.voice = self._select_voice()

        # Log character creation
        self._log_character_creation()

    def _log_character_creation(self):
        """Log the created character's attributes for debugging"""
        print(f"Created new character:")
        print(f"  Race: {self.race.value}")
        print(f"  Class: {self.character_class.value}")
        print(f"  Hair: {self.hair_color.value} and {self.hair_style.value}")
        print(f"  Face: {self.facial_feature.value} with {self.eye_color.value} eyes")
        print(f"  Additional features: {[feat.value for feat in self.additional_features]}")
        print(f"  Background: {self.background.value}")
        print(f"  Voice: {self.voice}")

    def set_name(self, name: str):
        """Set the character's name"""
        self.name = name
        return self

    def set_emotional_state(self, state: EmotionalState):
        """Update the character's emotional state"""
        self.emotional_state = state
        return self

    def _select_voice(self) -> str:
        """Select an appropriate voice based on character attributes"""
        # This is a placeholder - in real implementation, you might use LLM with structured output
        # to pick the most appropriate voice based on character attributes

        # For now, just use a simple mapping based on race and gender probability
        voices = [
            "helpful woman", "reading lady", "newsman", "child",
            "meditation lady", "newslady", "calm lady",
            "pilot over intercom", "reading man", "wise man",
            "laidback woman", "friendly man"
        ]

        # Simple selection logic - can be replaced with more sophisticated LLM-based selection
        if self.race in [CharacterRace.ELF, CharacterRace.FAIRY]:
            return random.choice(["meditation lady", "calm lady", "helpful woman"])
        elif self.race in [CharacterRace.DWARF, CharacterRace.ORC]:
            return random.choice(["newsman", "wise man"])
        elif self.race == CharacterRace.ROBOT:
            return "pilot over intercom"
        elif self.character_class in [CharacterClass.WIZARD, CharacterClass.NECROMANCER]:
            return "wise man"
        elif self.race == CharacterRace.ANIMAL:
            # Animals can have any voice
            return random.choice(voices)
        else:
            # Default: random selection
            return random.choice(voices)

    def _generate_prompt(self, additional_context: str = "") -> str:
        """Generate a detailed prompt for image generation based on character attributes"""
        name_prefix = f"{self.name}, " if self.name else ""

        # Build additional facial features string
        additional_features_str = ""
        if self.additional_features:
            features = [feat.value for feat in self.additional_features]
            additional_features_str = f" with {', '.join(features)}"

        # Build the base character description
        prompt = (
            f"A portrait of {name_prefix}a {self.race.value} {self.character_class.value}, "
            f"with {self.hair_color.value} {self.hair_style.value} hair, "
            f"{self.eye_color.value} eyes, {self.facial_feature.value}{additional_features_str}, "
            f"looking {self.emotional_state.value}. "
            f"Background: {self.background.value}. "
        )

        # Add any additional context if provided
        if additional_context:
            prompt += additional_context

        # Add style directive for consistency
        prompt += " High quality, detailed fantasy portrait, digital art."

        return prompt

    def generate_image(self, user_id: str, additional_context: str = "") -> Tuple[bool, str]:
        """Generate an image of the character with the current attributes"""
        prompt = self._generate_prompt(additional_context)

        print(f"Generating image with prompt: {prompt}")
        return generate_image(prompt, user_id)

    def generate_emotional_image(self, user_id: str, emotion: EmotionalState, context: str = "") -> Tuple[bool, str]:
        """Generate an image of the character with a specific emotion"""
        # Save the current emotion to restore later
        current_emotion = self.emotional_state

        # Set the new emotion temporarily
        self.emotional_state = emotion

        # Generate the image
        result = self.generate_image(user_id, additional_context=context)

        # Restore the original emotion
        self.emotional_state = current_emotion

        return result

    def generate_voice_message(self, text: str) -> str:
        """Placeholder for generating voice messages using a TTS API"""
        # This is a placeholder for the TTS implementation
        # In a real implementation, you would call a TTS API with the text and selected voice

        print(f"Would generate voice message with voice '{self.voice}' saying: {text}")
        return f"[Voice message using {self.voice} voice: {text}]"

    def to_dict(self) -> Dict:
        """Convert character to dictionary for storage"""
        return {
            "race": self.race.name,
            "class": self.character_class.name,
            "hair_color": self.hair_color.name,
            "hair_style": self.hair_style.name,
            "facial_feature": self.facial_feature.name,
            "eye_color": self.eye_color.name,
            "background": self.background.name,
            "emotional_state": self.emotional_state.name,
            "additional_features": [feat.name for feat in self.additional_features],
            "name": self.name,
            "voice": self.voice
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CharacterGenerator':
        """Create a character from a dictionary"""
        character = cls()
        character.race = CharacterRace[data["race"]]
        character.character_class = CharacterClass[data["class"]]
        character.hair_color = HairColor[data["hair_color"]]
        character.hair_style = HairStyle[data["hair_style"]]
        character.facial_feature = FacialFeature[data["facial_feature"]]
        character.eye_color = EyeColor[data["eye_color"]]
        character.background = Background[data["background"]]
        character.emotional_state = EmotionalState[data["emotional_state"]]
        character.additional_features = [FacialFeature[feat] for feat in data["additional_features"]]
        character.name = data["name"]
        character.voice = data["voice"]
        return character


# def generate_hangman_image() -> str:
#     """
#     Generate an image of a hangman game.
#     """
#     hangman = "Mr. Incredible"
#     current_number_guess = 5
#
#     prompt = f"I am playing a game of hangman. You need to draw the hangman" \
#     f" the parts of the hand are the pole, the beem the rope. Then the head, the body, left arm, right arm, left leg, right leg."\
#     f"The person to be hanged is {hangman}. The player has guessed {current_number_guess} number of times. You must " \
#     f" draw the hangman with the parts equal to the number fo guresses."
#
#     response = client.images.generate(
#         prompt=prompt,
#         model="black-forest-labs/FLUX.1-schnell",
#         steps=10,
#         n=4
#     )
#     print("\nimage url : ", response.data[0].url)
