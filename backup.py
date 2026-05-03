import subprocess
import sys
from pathlib import Path

import questionary
import requests

TOKEN_FILE = Path(__file__).parent / ".token"
DATA_DIR = Path(__file__).parent / "data"
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


def make_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_current_user(token: str) -> dict:
    response = requests.get(f"{GITHUB_API}/user", headers=make_headers(token))
    if response.status_code == 401:
        print("Error: token no válido o sin permisos suficientes", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def list_organizations(token: str) -> list[dict]:
    orgs = []
    url = f"{GITHUB_API}/user/orgs"
    while url:
        response = requests.get(url, headers=make_headers(token), params={"per_page": 100})
        if response.status_code == 401:
            print("Error: token no válido o sin permisos suficientes", file=sys.stderr)
            sys.exit(1)
        response.raise_for_status()
        orgs.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return orgs


def list_repos(token: str, account: str, is_user: bool) -> list[dict]:
    repos = []
    if is_user:
        url = f"{GITHUB_API}/user/repos"
        params = {"per_page": 100, "type": "owner"}
    else:
        url = f"{GITHUB_API}/orgs/{account}/repos"
        params = {"per_page": 100, "type": "all"}
    while url:
        response = requests.get(url, headers=make_headers(token), params=params)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")
        params = {}
    return repos


def clone_or_pull(token: str, repo: dict, dest_dir: Path) -> None:
    repo_dir = dest_dir / repo["name"]
    clone_url = repo["clone_url"].replace("https://", f"https://x-access-token:{token}@")

    if repo_dir.exists():
        print(f"    Actualizando {repo['name']}...")
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "pull", "--quiet"],
            capture_output=True, text=True
        )
    else:
        print(f"    Clonando {repo['name']}...")
        result = subprocess.run(
            ["git", "clone", "--quiet", clone_url, str(repo_dir)],
            capture_output=True, text=True
        )

    if result.returncode != 0:
        print(f"    ✗ Error en {repo['name']}: {result.stderr.strip()}", file=sys.stderr)
    else:
        print(f"    ✓ {repo['name']}")


def backup_account(token: str, account: str, is_user: bool) -> None:
    print(f"\n[{account}] Obteniendo repositorios...")
    repos = list_repos(token, account, is_user)
    if not repos:
        print(f"  Sin repositorios.")
        return
    print(f"  {len(repos)} repositorio(s) encontrado(s).")

    dest_dir = DATA_DIR / account
    dest_dir.mkdir(parents=True, exist_ok=True)

    for repo in repos:
        clone_or_pull(token, repo, dest_dir)


def main():
    token = load_token()
    user = get_current_user(token)
    orgs = list_organizations(token)

    user_label = user["login"] + " (usuario)"
    choices = [user_label] + [org["login"] for org in orgs]

    selected = questionary.checkbox(
        "Selecciona las cuentas (↑↓ para navegar, espacio para marcar, Enter para confirmar):",
        choices=choices,
    ).ask()

    if selected is None:
        print("Operación cancelada.")
        return

    if not selected:
        print("No se seleccionó ninguna cuenta.")
        return

    print(f"\nIniciando backup de {len(selected)} cuenta(s)...")
    for label in selected:
        is_user = label == user_label
        account = user["login"] if is_user else label
        backup_account(token, account, is_user)

    print("\n¡Backup completado!")


if __name__ == "__main__":
    main()
