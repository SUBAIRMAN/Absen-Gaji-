
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from datetime import datetime, timedelta
import calendar
import json
import pandas as pd
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./rekap.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RekapKehadiran(Base):
    __tablename__ = "rekap_kehadiran"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    nama = Column(String)
    bulan = Column(String)
    tahun = Column(Integer)
    hadir = Column(Integer)
    izin = Column(Integer)
    sakit = Column(Integer)
    alpha = Column(Integer)
    gaji = Column(Integer)

class KehadiranHarian(Base):
    __tablename__ = "kehadiran_harian"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    nama = Column(String)
    tanggal = Column(Date)
    status = Column(String)  # HADIR, IZIN, SAKIT, ALPHA

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MASTER_KARYAWAN = {
    "14049": {"nama": "SUBAIRMAN", "gaji": 196199},
    "14056": {"nama": "NASRUM", "gaji": 246199},
    "140065": {"nama": "EMIL KURNIA", "gaji": 246199},
    "14058": {"nama": "ICHSAN", "gaji": 196199},
    "14050": {"nama": "REMI SETYAWAN", "gaji": 196199},
    "140070": {"nama": "DHEA SARI RAMADHIAN ABDULLAH", "gaji": 246199},
    "140066": {"nama": "GUSTI PETRA ARRUAN", "gaji": 246199},
    "14059": {"nama": "RONALD", "gaji": 246199},
    "140068": {"nama": "ANDI NURFAHMI", "gaji": 246199},
    "140069": {"nama": "WIRA SUNARYA", "gaji": 246199},
    "140067": {"nama": "VARIAN VALIANT ERVIC MANGUMA", "gaji": 246199},
}

# Fungsi lainnya di sini...
