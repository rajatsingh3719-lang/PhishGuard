import math
import re
from collections import Counter
from urllib.parse import urlparse

FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "is_domain_ip",
    "tld_length",
    "subdomain_count",
    "obfuscation_char_count",
    "letter_count",
    "letter_ratio",
    "digit_count",
    "digit_ratio",
    "equals_count",
    "question_mark_count",
    "ampersand_count",
    "other_special_char_count",
    "special_char_ratio",
    "uses_https",
    "path_length",
    "query_length",
    "hostname_length",
    "url_entropy",
]


def calculate_entropy(text):
    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def extract_url_features(url):
    url = str(url).strip()

    # Add a scheme if the user enters something like google.com
    parsed = urlparse(url)

    if not parsed.scheme:
        parsed = urlparse("http://" + url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    url_length = len(url)

    letter_count = sum(char.isalpha() for char in url)
    digit_count = sum(char.isdigit() for char in url)

    special_chars = re.findall(r"[^a-zA-Z0-9]", url)

    # Characters commonly associated with URL obfuscation
    obfuscation_chars = re.findall(
        r"[%@]",
        url
    )

    # IP address detection
    is_domain_ip = int(
        bool(
            re.fullmatch(
                r"\d{1,3}(\.\d{1,3}){3}",
                hostname
            )
        )
    )

    # Extract TLD
    tld = ""

    if "." in hostname:
        tld = hostname.rsplit(".", 1)[-1]

    subdomain_count = max(
        hostname.count(".") - 1,
        0
    )

    other_special_chars = re.findall(
        r"[^a-zA-Z0-9./?=&_%@-]",
        url
    )

    features = {
        "url_length": url_length,

        "domain_length": len(hostname),

        "is_domain_ip": is_domain_ip,

        "tld_length": len(tld),

        "subdomain_count": subdomain_count,

        "obfuscation_char_count": len(obfuscation_chars),

        "letter_count": letter_count,

        "letter_ratio": (
            letter_count / url_length
            if url_length > 0
            else 0
        ),

        "digit_count": digit_count,

        "digit_ratio": (
            digit_count / url_length
            if url_length > 0
            else 0
        ),

        "equals_count": url.count("="),

        "question_mark_count": url.count("?"),

        "ampersand_count": url.count("&"),

        "other_special_char_count": len(
            other_special_chars
        ),

        "special_char_ratio": (
            len(special_chars) / url_length
            if url_length > 0
            else 0
        ),

        "uses_https": int(
            parsed.scheme.lower() == "https"
        ),

        "path_length": len(path),

        "query_length": len(query),

        "hostname_length": len(hostname),

        "url_entropy": calculate_entropy(url),
    }

    return features