"""
Módulo para la creación de vistas de Cubo (Tablas Pivote).

Este archivo toma el DataFrame crudo y genera las
visualizaciones principales del cubo.
"""
import pandas as pd

def cubo_base(df: pd.DataFrame) -> pd.DataFrame:
    """Cubo: Producto x Región x (Año, Trimestre), medida = sum(Ventas)."""
    return pd.pivot_table(
        df,
        values="Ventas",
        index=["Producto", "Región"],
        columns=["Año", "Trimestre"],
        aggfunc="sum",
        margins=True,        # Totales tipo "ALL"
        margins_name="Total"
    )
    
    """
    Crea el Cubo Base principal: Producto x Región vs. (Año, Trimestre).

    La medida principal es la suma de "Ventas". Incluye totales
    generales para filas y columnas.

    Args:
        df (pd.DataFrame): El DataFrame de datos crudos.

    Returns:
        pd.DataFrame: Una tabla pivote que representa el cubo OLAP.
    """

def pivot_multimedidas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot con múltiples medidas (Ventas y Cantidad),
    agregando por Producto x Región x Año.
    """
    return pd.pivot_table(
        df,
        values=["Ventas", "Cantidad"],
        index=["Producto", "Región"],
        columns=["Año"],
        aggfunc={"Ventas": "sum", "Cantidad": "sum"},
        margins=True
    )