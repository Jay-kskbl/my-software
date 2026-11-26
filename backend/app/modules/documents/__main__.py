"""把失败的任务成批放回队列的命令行工具（T24ae）。

用法（backend/ 目录，main 环境）：
    python -m app.modules.documents requeue-failed --type embed          # 演练：只列出
    python -m app.modules.documents requeue-failed --type embed --yes    # 执行
--type 可以是 embed（图片向量）或 ocr（文字识别）。先解决失败的原因（例如启动 CLIP 服务）再执行。

退出码：0 正常（包括没有需要处理的任务、演练）；1 配置有问题或连不上数据库；2 参数不对。
"""

import argparse
import sys

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.config import load_settings
from app.core.errors import ConfigError
from app.db.session import make_engine, make_session_factory
from app.modules.documents.requeue import REQUEUE_TYPES, load_failed_tasks, plan_requeue, requeue


def cmd_requeue_failed(session: Session, task_type: str, *, yes: bool) -> int:
    plan = plan_requeue(load_failed_tasks(session, task_type))
    if plan.skipped_deleted:
        print(f"跳过 {plan.skipped_deleted} 个：文档已删除。")
    if plan.skipped_old_version:
        print(f"跳过 {plan.skipped_old_version} 个：属于旧的解析版本，重做也会被跳过。")
    if not plan.tasks:
        print(f"没有需要放回队列的 {task_type} 任务。")
        return 0

    print(f"{plan.document_count} 个文档的 {len(plan.tasks)} 个失败的 {task_type} 任务，原因：")
    for reason, count in plan.reasons():
        print(f"- {count} 个：{reason}")
    if not yes:
        print("这是演练，没有改动任何数据。解决失败的原因之后，加 --yes 执行。")
        return 0

    count = requeue(session, plan)
    worker = "OCR Worker" if task_type == "ocr" else "通用 Worker（需要 CLIP 服务已启动）"
    print(f"已放回队列 {count} 个 {task_type} 任务，由{worker}处理。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.modules.documents")
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("requeue-failed", help="把失败的任务成批放回队列")
    command.add_argument("--type", required=True, choices=REQUEUE_TYPES, help="任务类型")
    command.add_argument("--yes", action="store_true", help="真正执行；不加时只列出")
    args = parser.parse_args(argv)

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
            return cmd_requeue_failed(session, args.type, yes=args.yes)
    except OperationalError as exc:
        # 只输出异常类型：异常文本里可能带主机、端口和数据库用户名
        print(f"无法连接数据库（{type(exc).__name__}），没有改动任何数据", file=sys.stderr)
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    sys.exit(main())
