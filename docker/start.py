import os
import sys

PORT = os.environ.get("PORT", "8000").strip() or "8000"


def main():
    os.environ["DJANGO_DEBUG"] = "false"
    os.execvp(
        sys.executable,
        [
            sys.executable,
            "manage.py",
            "runserver",
            f"0.0.0.0:{PORT}",
            "--insecure",
            "--noreload",
        ],
    )


if __name__ == "__main__":
    main()
