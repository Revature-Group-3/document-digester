"""Seed user stories based on the bundled Godot documentation.

Revision ID: b72e1f4a8c90
Revises: a41c9d7e2b63
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "b72e1f4a8c90"
down_revision: Union[str, Sequence[str], None] = "a41c9d7e2b63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


developers = sa.table(
    "developer",
    sa.column("id", sa.Integer()),
    sa.column("email", postgresql.CITEXT()),
)

user_stories = sa.table(
    "user_story",
    sa.column("id", sa.Integer()),
    sa.column("assignee_id", sa.Integer()),
    sa.column("title", sa.Text()),
    sa.column("description", sa.Text()),
)

SEED_STORIES = (
    (
        "casey.nguyen@example.invalid",
        "Build games from reusable scenes",
        "As a Godot developer, I want to compose levels from reusable packed scenes, so I can develop and update game components independently. Acceptance criteria: create multiple instances from a scene, customize an instance without changing its siblings, and propagate source-scene defaults to instances. Source: docs/instancing.txt.",
    ),
    (
        "jordan.lee@example.invalid",
        "Instantiate packed scenes at runtime",
        "As a Godot developer, I want to load a PackedScene, instantiate it, and add the resulting node to the scene tree, so gameplay can spawn reusable entities such as enemies or projectiles. Source: docs/nodes_and_scene_instances.txt.",
    ),
    (
        "riley.patel@example.invalid",
        "Find, create, and safely remove scene nodes",
        "As a Godot developer, I want to retrieve nodes by name or relative path after they enter the scene tree, create children dynamically, and defer deletion with queue_free(), so my scripts manage node lifecycles safely. Source: docs/nodes_and_scene_instances.txt.",
    ),
    (
        "casey.nguyen@example.invalid",
        "Connect signals to react to node events",
        "As a Godot developer, I want to connect a button or timer signal to a receiver in the editor or in code, so one node can react to another without polling. Acceptance criteria: connect code-created nodes after setup and have the callback perform the requested action. Source: docs/signals.txt.",
    ),
    (
        "jordan.lee@example.invalid",
        "Emit projectiles without coupling them to the player",
        "As a Godot developer, I want a player to emit a signal containing a bullet scene and its firing data, so the main scene can spawn the bullet independently of the player's later movement or rotation. Source: docs/instancing_with_signals.txt.",
    ),
    (
        "riley.patel@example.invalid",
        "Keep reusable scenes loosely coupled",
        "As a Godot developer, I want scenes to own their internal dependencies and receive necessary external references through explicit initialization or signals, so scenes remain reusable in different scene trees. Source: docs/scene_organization.txt.",
    ),
    (
        "casey.nguyen@example.invalid",
        "Use typed C# events for Godot signals",
        "As a Godot C# developer, I want to declare custom signals with Signal event-handler delegates and subscribe using C# events, so signal handling is type-safe. Acceptance criteria: emit through EmitSignal and disconnect captured lambdas when their receiver lifecycle requires it. Source: docs/c_sharp_signals.txt.",
    ),
    (
        "jordan.lee@example.invalid",
        "Populate a surface with repeated 3D meshes",
        "As a Godot developer, I want to configure a MultiMeshInstance3D with target and source meshes and control instance count, scale, and rotation, so I can efficiently distribute repeated objects such as trees across a landscape. Source: docs/using_multi_mesh_instance.txt.",
    ),
)


def upgrade() -> None:
    for email, title, description in SEED_STORIES:
        op.execute(
            sa.insert(user_stories).from_select(
                ["assignee_id", "title", "description"],
                sa.select(
                    developers.c.id,
                    sa.literal(title),
                    sa.literal(description),
                ).where(developers.c.email == email),
            )
        )


def downgrade() -> None:
    for email, title, description in reversed(SEED_STORIES):
        op.execute(
            user_stories.delete().where(
                user_stories.c.title == title,
                user_stories.c.description == description,
                user_stories.c.assignee_id.in_(
                    sa.select(developers.c.id).where(developers.c.email == email)
                ),
            )
        )
