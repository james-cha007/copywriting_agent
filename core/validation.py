import re
import unicodedata
from typing import List, Dict, Any, Tuple

MAX_LEN = 123
ASCII_LETTERS_RE = re.compile(r"[A-Za-z]")

REPLACEMENTS = {
    # Account
    "แอคเคาท์": "แอคเคานต์",
    # Action
    "แอคชั่น": "แอคชัน",
    # Application
    "แอพพลิเคชั่น": "แอปพลิเคชัน",
    "แอปพลิเคชั่น": "แอปพลิเคชัน",
    # Bank
    "แบงค์": "แบงก์",
    # Barcode
    "บาร์โค้ท": "บาร์โค้ด",
    # Blog
    "บล้อก": "บล็อก",
    "บล้อค": "บล็อก",
    # Browser
    "บราวเซอร์": "เบราว์เซอร์",
    # Calorie
    "แคลลอรี่": "แคลอรี",
    # Catalog
    "แคตตาล็อก": "แค็ตตาล็อก",
    # Chart
    "ชาร์ท": "ชาร์ต",
    # Classic
    "คลาสสิค": "คลาสสิก",
    # Clear
    "เคลียร": "เคลียร์",
    # Click
    "คลิ๊ก": "คลิก",
    # Clip
    "คลิ๊ป": "คลิป",
    # Cloud
    "คลาว": "คลาวด์",
    # Code
    "โค้ท": "โค้ด",
    # Comment
    "คอมเม้นต์": "คอมเมนต์",
    "คอมเมนท์": "คอมเมนต์",
    # Computer
    "คอมพิวท์เตอร์": "คอมพิวเตอร์",
    # Computing
    "คอมพิว้ติ้ง": "คอมพิวติง",
    # Cookie
    "คุ้กกี้": "คุกกี้",
    # Countdown
    "เคาท์ดาวน์": "เคานต์ดาวน์",
    # Digital
    "ดิจิตอล": "ดิจิทัล",
    # Directory
    "ไดเร็กทอรี่": "ไดเรกทอรี",
    # E-mail
    "อีเมล์": "อีเมล",
    # Facebook
    "เฟสบุ๊ค": "เฟซบุ๊ก",
    "เฟสบุ้ค": "เฟซบุ๊ก",
    # Footpath
    "ฟุทบาธ": "ฟุตปาธ",
    "ฟุทบาท": "ฟุตปาธ",
    # Function
    "ฟังก์ชั่น": "ฟังก์ชัน",
    # Full
    "ฟูลล์": "ฟูล",
    # Game
    "เกมส์": "เกม",
    # Graphic
    "กราฟฟิก": "กราฟิก",
    "กราฟฟิค": "กราฟิก",
    # Internet
    "อินเตอร์เน็ต": "อินเทอร์เน็ต",
    "อินเตอร์เน็ท": "อินเทอร์เน็ต",
    # Jacket
    "แจกเก็ต": "แจ็กเกต",
    # Lab
    "แล็ป": "แล็บ",
    # Like
    "ไลค์": "ไลก์",
    # Link
    "ลิงค์": "ลิงก์",
    # Lock/Log/Locker variations
    "ล้อค": "ล็อก",
    "ล็อค": "ล็อก",
    "ล็อคเกอร์": "ล็อกเกอร์",
    "ล้อก": "ล็อก",
    # Mobile
    "โมบาย": "โมไบล์",
    # Notebook
    "โน้ตบุ้ค": "โน้ตบุ๊ก",
    "โน้ตบุ๊ค": "โน้ตบุ๊ก",
    # Package/Packet
    "แพคเกจ": "แพ็กเกจ",
    "แพ็คเกจ": "แพ็กเกจ",
    "แพ็กเก็ท": "แพ็กเก็ต",
    "แพกเก็ต": "แพ็กเก็ต",
    # Pickup truck
    "รถปิคอัพ": "รถพิกอัป",
    "รถปิกอัพ": "รถพิกอัป",
    # Platform
    "แพลทฟอร์ม": "แพลตฟอร์ม",
    # Post
    "โพส": "โพสต์",
    # Promotion
    "โปรโมชั่น": "โปรโมชัน",
    # Quota
    "โควต้า": "โควตา",
    # Remote
    "รีโมท": "รีโมต",
    # Server
    "เซิฟเวอร์": "เซิร์ฟเวอร์",
    # Set
    "เซ็ต": "เซต",
    # Series
    "ซีรีย์ส์": "ซีรีส์",
    # Shirt
    "เช็ต": "เชิ้ต",
    "เชิร์ท": "เชิ้ต",
    # Shopping
    "ช้อปปิ้ง": "ช้อปปิง",
    # Smart
    "สมาร์ท": "สมาร์ต",
    # Software
    "ซอฟท์แวร์": "ซอฟต์แวร์",
    # Source code
    "ซอสโค๊ด": "ซอร์สโค้ด",
    "ซอร์สโค๊ด": "ซอร์สโค้ด",
    # Start
    "สตาร์ท": "สตาร์ต",
    # Stock
    "สต๊อก": "สต็อก",
    # Stuff
    "สตั๊ฟ": "สตัฟฟ์",
    # Super
    "ซุปเปอร์": "ซูเปอร์",
    # Tag
    "แท๊ก": "แท็ก",
    # Technic
    "เทกนิค": "เทคนิค",
    # Teflon
    "เทฟล่อน": "เทฟลอน",
    # Tent
    "เต๊นท์": "เต็นท์",
    # Topic
    "ท้อปปิค": "ทอปิก",
    # Top up
    "ท๊อปอัพ": "ท็อปอัพ",
    # Update/Upload
    "อัพเดท": "อัปเดต",
    "อัปเดท": "อัปเดต",
    "อัพโหลด": "อัปโหลด",
    # Ultraviolet
    "อุลตร้าไวโอเลต": "อัลตราไวโอเลต",
    # Version
    "เวอร์ชั่น": "เวอร์ชัน",
    # Video
    "วีดีโอ": "วิดีโอ",
    # Web/Website
    "เว็ป": "เว็บ",
    "เว็ปไซต์": "เว็บไซต์",
    # Wifi
    "ไวไฟ": "วายฟาย",
    # Workshop
    "เวิร์คช็อป": "เวิร์กชอป",
    # X-ray
    "เอ็กซเรย์": "เอกซเรย์",
}

AMBIGUOUS_TOKENS = {
    "เช็ค": {"suggest": "เช็ก (ตรวจสอบ) หรือ เช็ค (เอกสารธนาคาร) — ตรวจทานบริบท"},
}


def _normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", s)
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _apply_replacements(text: str) -> Tuple[str, List[Dict[str, Any]]]:
    issues = []
    new_text = text
    for tok in AMBIGUOUS_TOKENS.keys():
        if tok in new_text:
            issues.append({"type": "ambiguous_token", "token": tok, "message": AMBIGUOUS_TOKENS[tok]["suggest"]})

    for wrong, correct in REPLACEMENTS.items():
        if wrong in new_text:
            new_text = new_text.replace(wrong, correct)
            issues.append({"type": "replaced_word", "from": wrong, "to": correct})

    return new_text, issues


def _verify_field(text: str, max_len: int = MAX_LEN, strict_thai: bool = False) -> Tuple[str, List[Dict[str, Any]]]:
    issues = []
    s = _normalize_text(text)

    if "!" in s:
        s = s.replace("!", "")
        issues.append({"type": "removed_exclamation", "message": "Removed '!'"})

    s, repl_issues = _apply_replacements(s)
    issues.extend(repl_issues)

    if ASCII_LETTERS_RE.search(s):
        if strict_thai:
            cleaned = ASCII_LETTERS_RE.sub("", s)
            if cleaned != s:
                s = cleaned
                issues.append({"type": "removed_ascii_letters"})
        else:
            issues.append({"type": "non_thai_letters_detected"})

    if len(s) > max_len:
        s = s[: max_len - 1] + "…"
        issues.append({"type": "length_trimmed", "max_len": max_len})

    return s, issues


def validate_and_fix(model_json: Any) -> List[Dict[str, Any]]:
    # Accept either {"items": [...]} or [...] from the LLM
    if isinstance(model_json, dict) and "items" in model_json:
        arr = model_json.get("items", [])
    elif isinstance(model_json, list):
        arr = model_json
    else:
        raise ValueError("Expected a JSON array or {'items': [...]} from the model.")

    cleaned: List[Dict[str, Any]] = []
    for idx, obj in enumerate(arr, start=1):
        if not isinstance(obj, dict):
            obj = {}
        o = {
            "card_id": idx,
            "title": _normalize_text(obj.get("title", "")),
            "subtitle": _normalize_text(obj.get("subtitle", "")),
        }
        cleaned.append(o)

    return cleaned


def verify_and_adjust_banners(payload: Dict[str, Any], max_len: int = MAX_LEN, strict_thai: bool = False) -> Dict[str, Any]:
    items = payload.get("items", []) or []
    cleaned_items = []
    report = []

    for idx, obj in enumerate(items, start=1):
        o = dict(obj or {})
        o["card_id"] = idx
        title, title_issues = _verify_field(o.get("title", ""), max_len=max_len, strict_thai=strict_thai)
        subtitle, subtitle_issues = _verify_field(o.get("subtitle", ""), max_len=max_len, strict_thai=strict_thai)

        cleaned_items.append({"card_id": idx, "title": title, "subtitle": subtitle})
        report.append({"card_id": idx, "field": "title", "issues": title_issues})
        report.append({"card_id": idx, "field": "subtitle", "issues": subtitle_issues})

    return {"items": cleaned_items, "report": report}