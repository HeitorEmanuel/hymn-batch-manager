from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.database.models import Repertoire
from app.database.session import SessionFactory


class RepertoireRepository:
    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def save(self, repertoire: Repertoire) -> Repertoire:
        with self._sessions.session() as session:
            session.add(repertoire)
            session.flush()
            session.refresh(repertoire)
            return repertoire

    def list_recent(self, *, limit: int = 20) -> list[Repertoire]:
        statement = (
            select(Repertoire)
            .options(selectinload(Repertoire.items))
            .order_by(Repertoire.updated_at.desc())
            .limit(limit)
        )
        with self._sessions.session() as session:
            return list(session.scalars(statement).all())

    def get(self, repertoire_id: int) -> Repertoire | None:
        statement = (
            select(Repertoire)
            .options(selectinload(Repertoire.items))
            .where(Repertoire.id == repertoire_id)
        )
        with self._sessions.session() as session:
            return session.scalar(statement)

    def count(self) -> int:
        with self._sessions.session() as session:
            return session.scalar(select(func.count()).select_from(Repertoire)) or 0
