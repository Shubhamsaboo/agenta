import os
import uuid
import traceback
from typing import Optional


import click
from sqlalchemy.future import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from agenta_backend.models.db_models import (
    AppDB,
    EvaluatorConfigDB,
)


BATCH_SIZE = 1000


def get_app_db(session: Session, app_id: str) -> Optional[AppDB]:
    query = session.execute(select(AppDB).filter_by(id=uuid.UUID(app_id)))
    return query.scalars().first()


def update_evaluators_with_app_name():
    engine = create_engine(os.getenv("POSTGRES_URI"))
    sync_session = sessionmaker(engine, expire_on_commit=False)

    with sync_session() as session:
        try:
            offset = 0
            while True:
                records = (
                    session.execute(
                        select(EvaluatorConfigDB).offset(offset).limit(BATCH_SIZE)
                    )
                    .scalars()
                    .all()
                )
                if not records:
                    break

                # Update records with app_name as prefix
                for record in records:
                    evaluator_config_app = get_app_db(
                        session=session, app_id=str(record.app_id)
                    )
                    if evaluator_config_app:
                        record.name = f"{record.name} ({evaluator_config_app.app_name})"

                session.commit()
                offset += BATCH_SIZE

        except Exception as e:
            session.rollback()
            click.echo(
                click.style(
                    f"ERROR updating evaluator config names: {traceback.format_exc()}",
                    fg="red",
                )
            )
            raise e