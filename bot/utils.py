import re
import socket
from urllib.parse import urlparse

import aiohttp
from telegram import Update

import messages as messages
from config import DATE_FORMAT, SCREENSHOT_DIR, URL_WHOIS, WHOIS_FIELDS


def get_screenshot_path(url: str, update: Update) -> tuple[str, str]:
    request_info = get_request_info(url, update)
    date = request_info['date'].strftime(DATE_FORMAT)
    domain_name = request_info['website'].split('.')[:-1]
    if 'www' in domain_name:
        domain_name.remove('www')
    return f'{SCREENSHOT_DIR}{date}_{request_info['user_id']}_{'_'.join(domain_name)}.png'


def get_request_info(url: str, update: Update) -> dict[str, str]:
    request_info = {}
    request_info['date'] = update.message.date.astimezone()
    request_info['user_id'] = update.effective_user.id
    request_info['website'] = urlparse(url).netloc
    request_info['username'] = update.effective_user.username
    request_info['first_name'] = update.effective_chat.first_name
    return request_info


def is_valid_url(url: str) -> tuple[str, bool]:
    regex = (
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$'
    )
    regex_http = re.compile(
        r'^(?:http|ftp)s?://' + regex,
        re.IGNORECASE
    )
    regex_not_http = re.compile(regex, re.IGNORECASE)

    if regex_not_http.match(url) is not None:
        return 'https://' + url, True
    elif regex_http.match(url) is not None:
        return url, True
    return url, False


def get_screenshot_message(
    title: str, url: str, execution_time: float, language: str
) -> str:
    return (
        f'<b>{title}</b>\n\n'
        f'<b>{messages.website[language]}</b> {url}\n'
        f'<b>{messages.processing_time[language]}</b> {execution_time}'
    )


async def get_whois(website: str, language: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_WHOIS + website + WHOIS_FIELDS) as response:
            whois_info = await response.json()
            ip = socket.gethostbyname(website)
            return _get_whois_info_message(ip, whois_info, language)


def _get_whois_info_message(ip: str, whois_info: dict[str, str], language: str) -> str:
    return (
        f'IP: {ip}\n\n'
        f'{messages.continent[language]}: {whois_info['continent']}\n'
        f'{messages.country[language]}: {whois_info['country']}\n'
        f'{messages.city[language]}: {whois_info['city']}\n\n'
        f'{messages.provider[language]}: {whois_info['isp']}\n'
        f'{messages.organization[language]}: {whois_info['org']}'
    )
