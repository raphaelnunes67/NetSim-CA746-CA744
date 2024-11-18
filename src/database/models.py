from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class BulkSimulation(Base):
    __tablename__ = 'bulk_simulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    circuit_name = Column(String(20), nullable=False)
    pl_ev = Column(Integer)
    pl_pv = Column(Integer)
    loops_quantity = Column(Integer)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    simulations = relationship("Simulation", back_populates="bulk_simulation")


class Simulation(Base):
    __tablename__ = 'simulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bulk_simulation_id = Column(Integer, ForeignKey('bulk_simulations.id'))
    control_mode = Column(String(12), nullable=False)

    bulk_simulation = relationship("BulkSimulation", back_populates="simulations")
    voltages = relationship("VoltageData", back_populates="simulation")
    energy_meters = relationship("EnergyMeter", back_populates="simulation")
    compensations = relationship("Compensation", back_populates="simulation")
    losses = relationship("Loss", back_populates="simulation")


class VoltageData(Base):
    __tablename__ = 'voltages_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    n_res = Column(Integer)
    n_day = Column(Integer)
    v1 = Column(Float)
    v2 = Column(Float)
    v3 = Column(Float)

    simulation = relationship("Simulation", back_populates="voltages")


class EnergyMeter(Base):
    __tablename__ = 'energy_meters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    n_day = Column(Integer)
    n_res = Column(Integer)
    bus = Column(String(2), nullable=False)
    energy = Column(Float)

    simulation = relationship("Simulation", back_populates="energy_meters")


class Compensation(Base):
    __tablename__ = 'compensations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    compensation = Column(Float)

    simulation = relationship("Simulation", back_populates="compensations")


class Loss(Base):
    __tablename__ = 'losses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    n_day = Column(Integer)
    loss = Column(Float)

    simulation = relationship("Simulation", back_populates="losses")


# Database engine and session setup
engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
