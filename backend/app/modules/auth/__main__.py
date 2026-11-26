"""创建管理员账号的命令行工具（decisions.md D12：管理员不能通过接口注册）。

用法（backend/ 目录，main 环境）：
    python -m app.modules.auth create-admin <用户名>
密码在终端里交互输入，不出现在命令行参数和 shell 历史中。
"""

import argparse
import getpass
import sys

from pydantic import ValidationError

from app.config import load_settings
from app.core.errors import ConfigError, UsernameTakenError
from app.db.session import make_engine, make_session_factory
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.service import create_user


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.modules.auth")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create-admin", help="创建一个管理员账号")
    create.add_argument("username")
    args = parser.parse_args(argv)

    password = getpass.getpass("密码：")
    if getpass.getpass("再输入一次：") != password:
        print("两次输入的密码不一致", file=sys.stderr)
        return 1

    try:
        # 与注册接口用同一套用户名、密码规则
        RegisterRequest(username=args.username, password=password)
    except ValidationError as exc:
        fields = "、".join(str(err["loc"][0]) for err in exc.errors())
        print(
            f"不符合要求：{fields}（用户名 3–32 位字母数字 _ . -，密码 8–128 位）", file=sys.stderr
        )
        return 1

    try:
        settings = load_settings()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    engine = make_engine(
        settings.database_url, connect_timeout_seconds=settings.database_connect_timeout_seconds
    )
    try:
        with make_session_factory(engine)() as session:
            user = create_user(session, args.username, password, role="admin")
    except UsernameTakenError:
        print(f"用户名 {args.username} 已存在", file=sys.stderr)
        return 1
    finally:
        engine.dispose()

    print(f"已创建管理员 {user.username}（id={user.id}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
