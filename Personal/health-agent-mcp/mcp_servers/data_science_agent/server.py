#!/usr/bin/env python3
"""
Data Science Agent MCP Server
Handles health data analysis, trend detection, and statistical insights.
"""

from fastmcp import FastMCP
from typing import Dict, Any, List
import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal, WearableData
from sqlalchemy import func

mcp = FastMCP("Data Science Agent")


@mcp.tool()
def analyze_health_trend(
    user_id: int,
    metric: str,
    time_range: str = "last_30_days"
) -> Dict[str, Any]:
    """
    Analyze trends in user's health data.
    
    Args:
        user_id: User ID
        metric: Metric to analyze (heart_rate, steps, sleep_hours, hrv, calories)
        time_range: Time range (last_7_days, last_30_days, last_90_days)
    
    Returns:
        Statistical analysis and insights
    """
    db = SessionLocal()
    try:
        # Calculate date range
        days_map = {
            "last_7_days": 7,
            "last_30_days": 30,
            "last_90_days": 90
        }
        days = days_map.get(time_range, 30)
        start_date = datetime.now() - timedelta(days=days)
        
        # Query data
        query = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).order_by(WearableData.date)
        
        data = query.all()
        
        if not data:
            return {
                "error": f"No data found for user {user_id}",
                "metric": metric,
                "time_range": time_range
            }
        
        # Extract metric values
        values = [getattr(d, metric) for d in data if getattr(d, metric) is not None]
        dates = [d.date for d in data if getattr(d, metric) is not None]
        
        if not values:
            return {
                "error": f"No {metric} data available",
                "metric": metric,
                "time_range": time_range
            }
        
        # Statistical analysis
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        
        # Split into two periods for comparison
        mid_point = len(df) // 2
        early_values = df['value'].iloc[:mid_point]
        recent_values = df['value'].iloc[mid_point:]
        
        # Calculate trend
        if len(df) > 1:
            trend_direction = "improving" if recent_values.mean() < early_values.mean() else "stable"
            if metric in ['steps', 'sleep_hours', 'hrv', 'calories']:
                trend_direction = "improving" if recent_values.mean() > early_values.mean() else "stable"
        else:
            trend_direction = "insufficient_data"
        
        analysis = {
            "metric": metric,
            "time_range": time_range,
            "total_data_points": len(values),
            "average": round(df['value'].mean(), 2),
            "median": round(df['value'].median(), 2),
            "std_dev": round(df['value'].std(), 2),
            "min": round(df['value'].min(), 2),
            "max": round(df['value'].max(), 2),
            "latest_value": round(df['value'].iloc[-1], 2),
            "trend": trend_direction,
            "early_period_avg": round(early_values.mean(), 2) if len(early_values) > 0 else None,
            "recent_period_avg": round(recent_values.mean(), 2) if len(recent_values) > 0 else None,
            "change": round(recent_values.mean() - early_values.mean(), 2) if len(early_values) > 0 and len(recent_values) > 0 else None,
            "percent_change": round(((recent_values.mean() - early_values.mean()) / early_values.mean() * 100), 2) if len(early_values) > 0 and len(recent_values) > 0 and early_values.mean() != 0 else None,
        }
        
        return analysis
        
    finally:
        db.close()


@mcp.tool()
def compare_metrics(
    user_id: int,
    metric1: str,
    metric2: str,
    time_range: str = "last_30_days"
) -> Dict[str, Any]:
    """
    Compare correlation between two health metrics.
    
    Args:
        user_id: User ID
        metric1: First metric
        metric2: Second metric
        time_range: Time range for analysis
    
    Returns:
        Correlation analysis
    """
    db = SessionLocal()
    try:
        days_map = {
            "last_7_days": 7,
            "last_30_days": 30,
            "last_90_days": 90
        }
        days = days_map.get(time_range, 30)
        start_date = datetime.now() - timedelta(days=days)
        
        data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).all()
        
        if not data:
            return {"error": "No data found"}
        
        # Create DataFrame
        df = pd.DataFrame([{
            'date': d.date,
            metric1: getattr(d, metric1),
            metric2: getattr(d, metric2)
        } for d in data])
        
        # Remove rows with missing values
        df = df.dropna(subset=[metric1, metric2])
        
        if len(df) < 2:
            return {"error": "Insufficient data for correlation"}
        
        # Calculate correlation
        correlation = df[metric1].corr(df[metric2])
        
        return {
            "metric1": metric1,
            "metric2": metric2,
            "correlation": round(correlation, 3),
            "interpretation": (
                "strong positive" if correlation > 0.7 else
                "moderate positive" if correlation > 0.3 else
                "weak positive" if correlation > 0 else
                "weak negative" if correlation > -0.3 else
                "moderate negative" if correlation > -0.7 else
                "strong negative"
            ),
            "data_points": len(df)
        }
        
    finally:
        db.close()


@mcp.tool()
def get_weekly_summary(user_id: int) -> Dict[str, Any]:
    """
    Get weekly summary of all health metrics.
    
    Args:
        user_id: User ID
    
    Returns:
        Weekly summary statistics
    """
    db = SessionLocal()
    try:
        start_date = datetime.now() - timedelta(days=7)
        
        data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).all()
        
        if not data:
            return {"error": "No data found for the last week"}
        
        df = pd.DataFrame([{
            'heart_rate': d.heart_rate,
            'steps': d.steps,
            'sleep_hours': d.sleep_hours,
            'hrv': d.hrv,
            'calories': d.calories
        } for d in data])
        
        summary = {}
        for col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                summary[col] = {
                    "average": round(col_data.mean(), 2),
                    "min": round(col_data.min(), 2),
                    "max": round(col_data.max(), 2),
                    "days_recorded": len(col_data)
                }
        
        return {
            "period": "last_7_days",
            "summary": summary,
            "total_entries": len(data)
        }
        
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
