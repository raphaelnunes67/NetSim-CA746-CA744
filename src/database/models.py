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

    loop_simulations = relationship("LoopSimulation", back_populates="bulk_simulation") # One to many


class LoopSimulation(Base):
    __tablename__ = 'loop_simulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bulk_simulation_id = Column(Integer, ForeignKey('bulk_simulations.id'))

    bulk_simulation = relationship("BulkSimulation", back_populates="loop_simulations") # Many to One
    simulations = relationship("Simulation", back_populates="loop_simulation") # One to many


class Simulation(Base):
    __tablename__ = 'simulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    control_mode = Column(String(12), nullable=False)
    loop_simulation_id = Column(Integer, ForeignKey('loop_simulations.id'))
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    loop_simulation = relationship("LoopSimulation", back_populates="simulations") # Many to one
    # One to many
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

