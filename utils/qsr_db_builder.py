import json
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(String)
    nutrition = relationship("NutritionFacts", back_populates="item", uselist=False)

class NutritionFacts(Base):
    __tablename__ = 'nutrition_facts'

    item_id = Column(Integer, ForeignKey('menu.id'), primary_key=True)
    calories = Column(Integer)
    protein_g = Column(Float)
    fat_g = Column(Float)
    carbs_g = Column(Float)
    sodium_mg = Column(Integer)
    item = relationship("MenuItem", back_populates="nutrition")

def build_qsr_menu_database(json_path: str = "./data/menu.json", db_path: str = "sqlite:///./data/qsr_menu.db"):
    """Creates and populates the QSR menu database from a JSON file."""
    with open(json_path, 'r') as file:
        menu_data = json.load(file)

    engine = create_engine(db_path)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        for item in menu_data:
            menu_item = MenuItem(
                name=item["name"],
                category=item["category"],
                price=item["price"],
                ingredients=item["ingredients"]
            )
            nutrition = NutritionFacts(
                calories=item["nutrition"]["calories"],
                protein_g=item["nutrition"]["protein_g"],
                fat_g=item["nutrition"]["fat_g"],
                carbs_g=item["nutrition"]["carbs_g"],
                sodium_mg=item["nutrition"]["sodium_mg"],
                item=menu_item
            )
            session.add(menu_item)
            session.add(nutrition)

        session.commit()

    print(f"Database created and populated from {json_path}")
    return engine
    