from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate


async def get_example(db: AsyncSession, example_id: int):
    """
    根据示例ID获取示例信息
    :param db: 数据库会话
    :param example_id: 示例ID
    :return: 示例对象，如果未找到则返回 None
    """
    result = await db.execute(select(Example).filter(Example.id == example_id))
    return result.scalars().first()


async def get_examples(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    获取示例列表
    :param db: 数据库会话
    :param skip: 跳过的记录数
    :param limit: 返回的记录数
    :return: 示例列表
    """
    result = await db.execute(select(Example).offset(skip).limit(limit))
    return result.scalars().all()


async def create_example(db: AsyncSession, example: ExampleCreate):
    """
    创建新示例
    :param db: 数据库会话
    :param example: 示例创建模型
    :return: 创建的示例对象
    """
    db_example = Example(
        name=example.name,
        description=example.description,
    )
    db.add(db_example)
    await db.commit()
    await db.refresh(db_example)
    return db_example


async def update_example(db: AsyncSession, example_id: int, example: ExampleUpdate):
    """
    更新示例信息
    :param db: 数据库会话
    :param example_id: 示例ID
    :param example: 示例更新模型
    :return: 更新后的示例对象，如果未找到则返回 None
    """
    db_example = await get_example(db, example_id)
    if not db_example:
        return None
    db_example.name = example.name
    db_example.description = example.description
    await db.commit()
    await db.refresh(db_example)
    return db_example


async def delete_example(db: AsyncSession, example_id: int):
    """
    删除示例
    :param db: 数据库会话
    :param example_id: 示例ID
    :return: 删除的示例对象，如果未找到则返回 None
    """
    db_example = await get_example(db, example_id)
    if not db_example:
        return None
    await db.delete(db_example)
    await db.commit()
    return db_example
