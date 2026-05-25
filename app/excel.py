from datetime import date
from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from .models import Gasto

EXPECTED_COLUMNS = {"secretaria", "valor", "categoria", "descricao", "data"}


def read_financial_file(content: bytes, filename: str) -> pd.DataFrame:
    normalized_name = filename.lower().strip()
    if normalized_name.endswith(".xlsx"):
        return pd.read_excel(BytesIO(content))
    if normalized_name.endswith(".csv"):
        return pd.read_csv(BytesIO(content))
    raise ValueError("Formato invalido. Envie um arquivo .xlsx ou .csv")


def import_gastos_from_file(db: Session, content: bytes, filename: str) -> int:
    dataframe = read_financial_file(content, filename)
    dataframe.columns = [str(column).strip().lower() for column in dataframe.columns]

    missing = EXPECTED_COLUMNS - set(dataframe.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Colunas obrigatorias ausentes: {missing_list}")

    imported = 0
    for _, row in dataframe.iterrows():
        if pd.isna(row["valor"]) or pd.isna(row["data"]):
            continue

        raw_date = pd.to_datetime(row["data"]).date()
        if not isinstance(raw_date, date):
            continue

        gasto = Gasto(
            secretaria=str(row["secretaria"]).strip(),
            valor=float(row["valor"]),
            categoria=str(row["categoria"]).strip(),
            descricao=str(row["descricao"]).strip(),
            data=raw_date,
        )
        db.add(gasto)
        imported += 1

    db.commit()
    return imported


def import_gastos_from_excel(db: Session, content: bytes) -> int:
    return import_gastos_from_file(db, content, "arquivo.xlsx")
