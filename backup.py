import sys
from pathlib import Path

import requests

TOKEN_FILE = Path(__file__).parent / ".token"
GITHUB_API = "https://api.github.com"


def load_token() -> str:
    if not TOKEN_FILE.exists():
        print(f"Error: no se encuentra el fichero de token '{TOKEN_FILE}'", file=sys.stderr)
        sys.exit(1)
    token = TOKEN_FILE.read_text().strip()
    if not token:
        print("Error: el fichero de token está vacío", file=sys.stderr)
        sys.exit(1)
    return token


def get_current_user(token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(f"{GITHUB_API}/user", headers=headers)
    if response.status_code == 401:
        print("Error: token no válido o sin permisos suficientes", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def list_organizations(token: str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    orgs = []
    url = f"{GITHUB_API}/user/orgs"
    while url:
        response = requests.get(url, headers=headers, params={"per_page": 100})
        if response.status_code == 401:
            print("Error: token no válido o sin permisos suficientes", file=sys.stderr)
            sys.exit(1)
        response.raise_for_status()
        orgs.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return orgs


def main():
    token = load_token()
    user = get_current_user(token)
    orgs = list_organizations(token)
    total = 1 + len(orgs)
    print(f"Cuentas accesibles ({total}):")
    print(f"  - {user['login']} (usuario)")
    for org in orgs:
        print(f"  - {org['login']}")


if __name__ == "__main__":
    main()
