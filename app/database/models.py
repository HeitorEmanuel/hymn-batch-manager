from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.domain.enums import ItemStatus, MediaType, RepertoireStatus


def now() -> datetime:
    return datetime.now().astimezone()


class Repertoire(Base):
    __tablename__ = "repertoires"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    event_date: Mapped[date | None] = mapped_column(Date)
    church: Mapped[str | None] = mapped_column(String(200))
    event: Mapped[str | None] = mapped_column(String(200))
    destination_path: Mapped[str] = mapped_column(Text)
    default_format: Mapped[str] = mapped_column(String(20), default="mp3")
    default_quality: Mapped[str] = mapped_column(String(40), default="192 kbps")
    default_media_type: Mapped[str] = mapped_column(
        String(30), default=MediaType.KEEP_ORIGINAL.value
    )
    numbering_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    starting_number: Mapped[int] = mapped_column(Integer, default=1)
    generate_zip: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(40), default=RepertoireStatus.DRAFT.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    items: Mapped[list[RepertoireItem]] = relationship(
        back_populates="repertoire",
        cascade="all, delete-orphan",
        order_by="RepertoireItem.position",
    )


class RepertoireItem(Base):
    __tablename__ = "repertoire_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    repertoire_id: Mapped[int] = mapped_column(ForeignKey("repertoires.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(Integer)
    original_name: Mapped[str] = mapped_column(String(500))
    normalized_name: Mapped[str] = mapped_column(String(500), index=True)
    artist: Mapped[str | None] = mapped_column(String(250))
    album: Mapped[str | None] = mapped_column(String(250))
    hymn_number: Mapped[str | None] = mapped_column(String(40))
    desired_version: Mapped[str | None] = mapped_column(String(100))
    media_type: Mapped[str] = mapped_column(String(30), default=MediaType.KEEP_ORIGINAL.value)
    desired_format: Mapped[str] = mapped_column(String(20), default="mp3")
    source_type: Mapped[str | None] = mapped_column(String(100))
    source_reference: Mapped[str | None] = mapped_column(Text)
    selected_result_id: Mapped[int | None] = mapped_column(Integer)
    output_path: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(40), default=ItemStatus.WAITING.value)
    error_message: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    repertoire: Mapped[Repertoire] = relationship(back_populates="items")


class LibraryFolder(Base):
    __tablename__ = "library_folders"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(Text, unique=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    recursive: Mapped[bool] = mapped_column(Boolean, default=True)
    last_indexed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class LibraryFile(Base):
    __tablename__ = "library_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    folder_id: Mapped[int] = mapped_column(ForeignKey("library_folders.id", ondelete="CASCADE"))
    path: Mapped[str] = mapped_column(Text, unique=True)
    filename: Mapped[str] = mapped_column(String(500))
    normalized_name: Mapped[str] = mapped_column(String(500), index=True)
    extension: Mapped[str] = mapped_column(String(20))
    media_type: Mapped[str] = mapped_column(String(20))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(Integer)
    duration: Mapped[float | None] = mapped_column(Float)
    bitrate: Mapped[int | None] = mapped_column(Integer)
    codec: Mapped[str | None] = mapped_column(String(80))
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    fps: Mapped[float | None] = mapped_column(Float)
    artist: Mapped[str | None] = mapped_column(String(250))
    album: Mapped[str | None] = mapped_column(String(250))
    title: Mapped[str | None] = mapped_column(String(500))
    file_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    exists: Mapped[bool] = mapped_column(Boolean, default=True)
    preferred: Mapped[bool] = mapped_column(Boolean, default=False)


class SearchResult(Base):
    __tablename__ = "search_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("repertoire_items.id", ondelete="CASCADE"))
    provider: Mapped[str] = mapped_column(String(100))
    external_id: Mapped[str | None] = mapped_column(String(250))
    title: Mapped[str] = mapped_column(String(500))
    artist: Mapped[str | None] = mapped_column(String(250))
    album: Mapped[str | None] = mapped_column(String(250))
    reference: Mapped[str] = mapped_column(Text)
    page_url: Mapped[str | None] = mapped_column(Text)
    preview_url: Mapped[str | None] = mapped_column(Text)
    download_url: Mapped[str | None] = mapped_column(Text)
    can_download: Mapped[bool] = mapped_column(Boolean, default=False)
    duration: Mapped[float | None] = mapped_column(Float)
    format: Mapped[str | None] = mapped_column(String(20))
    quality: Mapped[str | None] = mapped_column(String(100))
    file_size: Mapped[int | None] = mapped_column(Integer)
    license: Mapped[str | None] = mapped_column(String(250))
    confidence: Mapped[float] = mapped_column(Float, default=0)
    selected: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("repertoire_items.id", ondelete="CASCADE"))
    job_type: Mapped[str] = mapped_column(String(50))
    priority: Mapped[int] = mapped_column(Integer, default=0)
    progress: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(40), default=ItemStatus.WAITING.value)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    input_path: Mapped[str | None] = mapped_column(Text)
    output_path: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[str | None] = mapped_column(Text)


class DownloadRecord(Base):
    __tablename__ = "download_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(100))
    source_url: Mapped[str] = mapped_column(Text)
    page_url: Mapped[str | None] = mapped_column(Text)
    destination: Mapped[str] = mapped_column(Text)
    file_size: Mapped[int | None] = mapped_column(Integer)
    mime_type: Mapped[str | None] = mapped_column(String(100))
    hash: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(150), primary_key=True)
    value: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


MODEL_TYPES: tuple[type[Any], ...] = (
    Repertoire,
    RepertoireItem,
    LibraryFolder,
    LibraryFile,
    SearchResult,
    ProcessingJob,
    DownloadRecord,
    AppSetting,
)
