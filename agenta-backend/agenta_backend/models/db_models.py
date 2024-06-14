from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import uuid_utils.compat as uuid
from pydantic import BaseModel, Field
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    Float,
    Enum,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB

from agenta_backend.models.shared_models import TemplateType


Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    uid = Column(String, unique=True, index=True, default="0")
    username = Column(String, default="agenta")
    email = Column(String, unique=True, default="demo@agenta.ai")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


# TODO: Rename ImageDB to DockerImageDB ?
class ImageDB(Base):
    __tablename__ = "docker_images"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    type = Column(String, default="image")
    template_uri = Column(String, nullable=True)
    docker_id = Column(String, nullable=True, index=True)
    tags = Column(String, nullable=True)
    deletable = Column(Boolean, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("UserDB")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class AppDB(Base):
    __tablename__ = "app_db"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_name = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")
    variant = relationship("AppVariantDB", cascade="all, delete-orphan", backref="app")
    evaluator_config = relationship(
        "EvaluatorConfigDB", cascade="all, delete-orphan", backref="app"
    )
    testset = relationship("TestSetDB", cascade="all, delete-orphan", backref="app")
    base = relationship("DeploymentDB", cascade="all, delete-orphan", backref="app")
    deployment = relationship(
        "VariantBaseDB", cascade="all, delete-orphan", backref="app"
    )
    evaluation = relationship(
        "EvaluationDB", cascade="all, delete-orphan", backref="app"
    )


class DeploymentDB(Base):
    __tablename__ = "deployments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    container_name = Column(String)
    container_id = Column(String)
    uri = Column(String)
    status = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")


class VariantBaseDB(Base):
    __tablename__ = "bases"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    base_name = Column(String)
    image_id = Column(UUID(as_uuid=True), ForeignKey("docker_images.id"))
    deployment_id = Column(
        UUID(as_uuid=True), ForeignKey("deployments.id", ondelete="SET NULL")
    )
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # app = relationship("AppDB", back_populates="base")
    user = relationship("UserDB")
    image = relationship("ImageDB")
    deployment = relationship("DeploymentDB")


class AppVariantDB(Base):
    __tablename__ = "app_variants"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id", ondelete="CASCADE"))
    variant_name = Column(String)
    revision = Column(Integer)
    image_id = Column(UUID(as_uuid=True), ForeignKey("docker_images.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    modified_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    base_name = Column(String)
    base_id = Column(UUID(as_uuid=True), ForeignKey("bases.id"))
    config_name = Column(String, nullable=False)
    config_parameters = Column(JSONB, nullable=False, default=dict)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    image = relationship("ImageDB")
    user = relationship("UserDB", foreign_keys=[user_id])
    modified_by = relationship("UserDB", foreign_keys=[modified_by_id])
    base = relationship("VariantBaseDB")
    revisions = relationship(
        "AppVariantRevisionsDB", cascade="all, delete-orphan", backref="variant"
    )


class AppVariantRevisionsDB(Base):
    __tablename__ = "app_variant_revisions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    variant_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variants.id", ondelete="CASCADE")
    )
    revision = Column(Integer)
    modified_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    base_id = Column(UUID(as_uuid=True), ForeignKey("bases.id"))
    config_name = Column(String, nullable=False)
    config_parameters = Column(JSONB, nullable=False, default=dict)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    modified_by = relationship("UserDB")
    base = relationship("VariantBaseDB")


class AppEnvironmentDB(Base):
    __tablename__ = "environments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id", ondelete="CASCADE"))
    name = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    revision = Column(Integer)
    deployed_app_variant_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variants.id", ondelete="SET NULL")
    )
    deployed_app_variant_revision_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variant_revisions.id", ondelete="SET NULL")
    )
    deployment_id = Column(
        UUID(as_uuid=True), ForeignKey("deployments.id", ondelete="SET NULL")
    )
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")
    environment_revisions = relationship(
        "AppEnvironmentRevisionDB", cascade="all, delete-orphan", backref="environment"
    )
    deployed_app_variant = relationship("AppVariantDB")
    deployed_app_variant_revision = relationship("AppVariantRevisionsDB")


class AppEnvironmentRevisionDB(Base):
    __tablename__ = "environments_revisions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    environment_id = Column(
        UUID(as_uuid=True), ForeignKey("environments.id", ondelete="CASCADE")
    )
    revision = Column(Integer)
    modified_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    deployed_app_variant_revision_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variant_revisions.id", ondelete="SET NULL")
    )
    deployment_id = Column(
        UUID(as_uuid=True), ForeignKey("deployments.id", ondelete="SET NULL")
    )
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    modified_by = relationship("UserDB")


class TemplateDB(Base):
    __tablename__ = "templates"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    type = Column(Enum(TemplateType), default=TemplateType.IMAGE, nullable=False)
    template_uri = Column(String)
    tag_id = Column(Integer)
    name = Column(String, unique=True)
    repo_name = Column(String)
    title = Column(String)
    description = Column(String)
    size = Column(Integer)
    digest = Column(String)  # sha256 hash of image digest
    last_pushed = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class TestSetDB(Base):
    __tablename__ = "testsets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    name = Column(String)
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id", ondelete="CASCADE"))
    csvdata = Column(JSONB)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")


class EvaluatorConfigDB(Base):
    __tablename__ = "evaluators_configs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )

    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    evaluator_key = Column(String)
    settings_values = Column(JSONB, default=dict)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")


class HumanEvaluationDB(Base):
    __tablename__ = "human_evaluations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id"))
    app = relationship("AppDB")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("UserDB")
    status = Column(String)
    evaluation_type = Column(String)
    variant_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variants.id", ondelete="SET NULL")
    )
    variant = relationship("AppVariantDB")
    variant_revision_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variant_revisions.id", ondelete="SET NULL")
    )
    variant_revision = relationship("AppVariantRevisionsDB")
    testset_id = Column(UUID(as_uuid=True), ForeignKey("testsets.id"))
    testset = relationship("TestSetDB")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class HumanEvaluationScenarioDB(Base):
    __tablename__ = "human_evaluations_scenarios"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("UserDB")
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("human_evaluations.id"))
    evaluation = relationship("HumanEvaluationDB")
    inputs = Column(JSONB)  # List of HumanEvaluationScenarioInput
    outputs = Column(JSONB)  # List of HumanEvaluationScenarioOutput
    vote = Column(String)
    score = Column(JSONB)
    correct_answer = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    is_pinned = Column(Boolean)
    note = Column(String)


class EvaluationAggregatedResultDB(Base):
    __tablename__ = "evaluation_aggregated_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("evaluations.id"))
    evaluator_config_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluators_configs.id")
    )
    result = Column(JSONB)  # Result

    evaluation = relationship("EvaluationDB", back_populates="aggregated_results")
    evaluator_config = relationship("EvaluatorConfigDB", backref="evaluator_config")


class EvaluationScenarioResultDB(Base):
    __tablename__ = "evaluation_scenario_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    evaluation_scenario_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluation_scenarios.id")
    )
    evaluation_scenario = relationship("EvaluationScenarioDB", back_populates="results")
    evaluator_config_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluators_configs.id")
    )
    evaluator_config = relationship("EvaluatorConfigDB")
    result = Column(JSONB)  # Result


class EvaluationDB(Base):
    __tablename__ = "evaluations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    app_id = Column(UUID(as_uuid=True), ForeignKey("app_db.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(JSONB)  # Result
    testset_id = Column(
        UUID(as_uuid=True), ForeignKey("testsets.id", ondelete="SET NULL")
    )
    variant_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variants.id", ondelete="SET NULL")
    )
    variant_revision_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variant_revisions.id", ondelete="SET NULL")
    )
    average_cost = Column(JSONB)  # Result
    total_cost = Column(JSONB)  # Result
    average_latency = Column(JSONB)  # Result
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")
    testset = relationship("TestSetDB")
    variant = relationship("AppVariantDB")
    variant_revision = relationship("AppVariantRevisionsDB")
    aggregated_results = relationship(
        "EvaluationAggregatedResultDB", back_populates="evaluation"
    )
    evaluation_scenarios = relationship(
        "EvaluationScenarioDB", cascade="all, delete-orphan", backref="evaluation"
    )


class EvaluationEvaluatorConfigDB(Base):
    __tablename__ = "evaluation_evaluator_configs"

    evaluation_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluations.id"), primary_key=True
    )
    evaluator_config_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluators_configs.id"), primary_key=True
    )


class EvaluationScenarioDB(Base):
    __tablename__ = "evaluation_scenarios"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    evaluation_id = Column(
        UUID(as_uuid=True), ForeignKey("evaluations.id", ondelete="CASCADE")
    )
    variant_id = Column(
        UUID(as_uuid=True), ForeignKey("app_variants.id", ondelete="SET NULL")
    )
    inputs = Column(JSONB)  # List of EvaluationScenarioInput
    outputs = Column(JSONB)  # List of EvaluationScenarioOutput
    correct_answers = Column(JSONB)  # List of CorrectAnswer
    is_pinned = Column(Boolean)
    note = Column(String)
    latency = Column(Integer)
    cost = Column(Integer)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("UserDB")
    variant = relationship("AppVariantDB")
    results = relationship(
        "EvaluationScenarioResultDB", back_populates="evaluation_scenario"
    )


class IDsMappingDB(Base):
    __tablename__ = "ids_mapping"

    table_name = Column(String, nullable=False)
    objectid = Column(String, primary_key=True)
    uuid = Column(UUID(as_uuid=True), nullable=False)
