from __future__ import annotations

import csv
import io
import zipfile
from dataclasses import dataclass
from pathlib import Path

INTERESTING_FILES = ("diary.csv", "reviews.csv")
SKIP_DIR_NAMES = frozenset({"deleted", "likes", "orphaned"})
DIARY_COLUMNS = [
    "Date",
    "Name",
    "Year",
    "Letterboxd URI",
    "Rating",
    "Rewatch",
    "Tags",
    "Watched Date",
]


class ExportError(ValueError):
    pass


@dataclass(frozen=True)
class LetterboxdExport:
    diary_csv: Path
    reviews_csv: Path
    username: str


def materialize_export(source: bytes, dest_dir: Path) -> LetterboxdExport:
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        archive = zipfile.ZipFile(io.BytesIO(source))
    except zipfile.BadZipFile as exc:
        raise ExportError("Upload a Letterboxd .zip export") from exc

    names = _safe_names(archive)
    chosen: dict[str, str] = {}
    for filename in INTERESTING_FILES:
        member = _pick_member(names, filename)
        if member is None:
            raise ExportError(f"The zip is missing {filename}")
        chosen[filename] = member

    for filename, member in chosen.items():
        (dest_dir / filename).write_bytes(archive.read(member))

    diary_csv = dest_dir / "diary.csv"
    if not _has_data_rows(diary_csv):
        watched = _read_member(archive, names, "watched.csv")
        if watched is not None and _text_has_data_rows(watched):
            ratings = _read_member(archive, names, "ratings.csv")
            diary_csv.write_text(
                _diary_from_watched(watched, ratings),
                encoding="utf-8",
            )

    return LetterboxdExport(
        diary_csv=diary_csv,
        reviews_csv=dest_dir / "reviews.csv",
        username=_username_from_profile(archive, names),
    )


def _safe_names(archive: zipfile.ZipFile) -> list[str]:
    names: list[str] = []
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename.replace("\\", "/")
        parts = [part for part in name.split("/") if part]
        if not parts or name.startswith("/") or any(part == ".." for part in parts):
            raise ExportError("The zip contains an unsafe path")
        names.append("/".join(parts))
    return names


def _pick_member(names: list[str], filename: str) -> str | None:
    candidates: list[list[str]] = []
    for name in names:
        parts = name.split("/")
        if parts[-1] != filename:
            continue
        if any(part in SKIP_DIR_NAMES for part in parts[:-1]):
            continue
        candidates.append(parts)
    if not candidates:
        return None
    candidates.sort(key=lambda parts: (len(parts), "/".join(parts)))
    return "/".join(candidates[0])


def _read_member(archive: zipfile.ZipFile, names: list[str], filename: str) -> str | None:
    member = _pick_member(names, filename)
    if member is None:
        return None
    return archive.read(member).decode("utf-8")


def _has_data_rows(path: Path) -> bool:
    with path.open(encoding="utf-8") as handle:
        return next(csv.DictReader(handle), None) is not None


def _text_has_data_rows(text: str) -> bool:
    return next(csv.DictReader(io.StringIO(text)), None) is not None


def username_from_profile(text: str) -> str:
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ExportError("profile.csv has no user")
    name = (rows[0].get("Username") or "").strip()
    if not name:
        raise ExportError("profile.csv is missing Username")
    return name


def _username_from_profile(archive: zipfile.ZipFile, names: list[str]) -> str:
    text = _read_member(archive, names, "profile.csv")
    if text is None:
        raise ExportError("The zip is missing profile.csv")
    return username_from_profile(text)


def _diary_from_watched(watched_text: str, ratings_text: str | None) -> str:
    rating_by_uri: dict[str, str] = {}
    if ratings_text:
        for row in csv.DictReader(io.StringIO(ratings_text)):
            uri = (row.get("Letterboxd URI") or "").strip()
            if uri:
                rating_by_uri[uri] = row.get("Rating") or ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=DIARY_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in csv.DictReader(io.StringIO(watched_text)):
        uri = row.get("Letterboxd URI") or ""
        date = row.get("Date") or ""
        writer.writerow(
            {
                "Date": date,
                "Name": row.get("Name") or "",
                "Year": row.get("Year") or "",
                "Letterboxd URI": uri,
                "Rating": rating_by_uri.get(uri, ""),
                "Rewatch": "",
                "Tags": "",
                "Watched Date": date,
            }
        )
    return output.getvalue()
