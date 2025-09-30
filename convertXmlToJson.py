import json
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from xml.etree import ElementTree as ET

import fire
from loguru import logger


@dataclass
class AnimeTitle:
    lang: str
    type: str
    text: str


@dataclass
class Anime:
    aid: str
    titles: List[AnimeTitle]


class AnimeTitleConverter:
    def __init__(self, anime_title_url: str = "./anime-titles.xml"):
        self.anime_title_url = Path(anime_title_url)

    def convert_xml_to_json(self, output_file: str = "./animes-titles.json") -> None:
        """Convert anime titles XML to JSON format."""
        logger.info(f"Reading XML file: {self.anime_title_url}")

        try:
            tree = ET.parse(self.anime_title_url)
            root = tree.getroot()
        except FileNotFoundError:
            logger.error(f"File not found: {self.anime_title_url}")
            return
        except ET.ParseError as e:
            logger.error(f"Error parsing XML: {e}")
            return

        animes: List[Dict[str, Any]] = []

        for anime_elem in root.findall("anime"):
            aid = anime_elem.get("aid")
            if not aid:
                logger.warning("Found anime element without aid, skipping")
                continue

            titles: List[Dict[str, str]] = []

            for title_elem in anime_elem.findall("title"):
                lang = title_elem.get("{http://www.w3.org/XML/1998/namespace}lang", "")
                title_type = title_elem.get("type", "")
                text = title_elem.text or ""

                titles.append({
                    "lang": lang,
                    "type": title_type,
                    "text": text
                })

            animes.append({
                "aid": aid,
                "titles": titles
            })

        logger.info(f"Processed {len(animes)} anime entries")

        output_path = Path(output_file)
        try:
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(animes, f, indent=2, ensure_ascii=False)
            logger.success(f"Successfully wrote JSON to: {output_path}")
        except IOError as e:
            logger.error(f"Error writing to file {output_path}: {e}")


def main(anime_title_url: str = "./anime-titles.xml", output_file: str = "./animes-titles.json") -> None:
    """Convert anime titles XML to JSON format.

    Args:
        anime_title_url: Path to the input XML file
        output_file: Path to the output JSON file
    """
    converter = AnimeTitleConverter(anime_title_url)
    converter.convert_xml_to_json(output_file)


if __name__ == "__main__":
    fire.Fire(main)