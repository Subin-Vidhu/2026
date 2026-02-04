#!/usr/bin/env python3
"""
Domain Expert Agent MCP Server
Provides medical knowledge and interprets health metrics.
"""

from fastmcp import FastMCP
from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal, User, MedicalRecord, WearableData
from datetime import datetime, timedelta

mcp = FastMCP("Domain Expert Agent")


# Medical knowledge base
NORMAL_RANGES = {
    "heart_rate": {
        "adult": (60, 100),
        "athletic": (40, 60),
        "description": "Resting heart rate in beats per minute"
    },
    "hrv": {
        "good": (50, 100),
        "excellent": (100, 200),
        "description": "Heart rate variability in milliseconds"
    },
    "sleep_hours": {
        "adult": (7, 9),
        "description": "Recommended sleep duration"
    },
    "steps": {
        "minimum": 5000,
        "recommended": 10000,
        "description": "Daily step count"
    },
    "cholesterol": {
        "desirable": (0, 200),
        "borderline": (200, 239),
        "high": (240, 999),
        "description": "Total cholesterol in mg/dL"
    },
    "glucose": {
        "normal": (70, 99),
        "prediabetes": (100, 125),
        "diabetes": (126, 999),
        "description": "Fasting blood glucose in mg/dL"
    }
}


@mcp.tool()
def interpret_health_metric(
    user_id: int,
    metric: str,
    value: float
) -> Dict[str, Any]:
    """
    Interpret a health metric value in context of user's profile.
    
    Args:
        user_id: User ID
        metric: Metric name
        value: Metric value
    
    Returns:
        Medical interpretation
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return {"error": f"User {user_id} not found"}
        
        interpretation = {
            "metric": metric,
            "value": value,
            "user_age": user.age,
            "user_gender": user.gender
        }
        
        # Get normal range
        if metric in NORMAL_RANGES:
            ranges = NORMAL_RANGES[metric]
            interpretation["description"] = ranges.get("description", "")
            
            if metric == "heart_rate":
                if user.age < 60:
                    normal_range = ranges["adult"]
                else:
                    normal_range = (60, 90)  # Slightly different for seniors
                
                interpretation["normal_range"] = normal_range
                interpretation["status"] = (
                    "normal" if normal_range[0] <= value <= normal_range[1]
                    else "below_normal" if value < normal_range[0]
                    else "above_normal"
                )
                
                if interpretation["status"] == "normal":
                    interpretation["interpretation"] = "Your resting heart rate is within normal range."
                elif interpretation["status"] == "below_normal":
                    if value >= ranges["athletic"][0]:
                        interpretation["interpretation"] = "Lower heart rate, which is common in athletic individuals. This is generally a positive sign of cardiovascular fitness."
                    else:
                        interpretation["interpretation"] = "Heart rate is notably low. Consider consulting a healthcare provider if you experience symptoms."
                else:
                    interpretation["interpretation"] = "Heart rate is elevated. This could be due to stress, caffeine, dehydration, or other factors. Monitor and consult a healthcare provider if persistent."
            
            elif metric == "hrv":
                interpretation["interpretation"] = (
                    "Excellent HRV - indicates good cardiovascular health and stress resilience" if value >= ranges["excellent"][0]
                    else "Good HRV - indicates adequate recovery and health" if value >= ranges["good"][0]
                    else "Lower HRV - may indicate stress, fatigue, or need for recovery"
                )
            
            elif metric == "sleep_hours":
                normal_range = ranges["adult"]
                interpretation["normal_range"] = normal_range
                interpretation["status"] = (
                    "adequate" if normal_range[0] <= value <= normal_range[1]
                    else "insufficient" if value < normal_range[0]
                    else "excessive"
                )
                interpretation["interpretation"] = (
                    "Sleep duration is within recommended range" if interpretation["status"] == "adequate"
                    else "Sleep duration is below recommended levels - may impact health and performance" if interpretation["status"] == "insufficient"
                    else "Sleep duration is above typical range - ensure it's restorative"
                )
            
            elif metric == "cholesterol":
                if value < ranges["desirable"][1]:
                    interpretation["status"] = "desirable"
                    interpretation["interpretation"] = "Total cholesterol is in the desirable range"
                elif value < ranges["borderline"][1]:
                    interpretation["status"] = "borderline_high"
                    interpretation["interpretation"] = "Total cholesterol is borderline high. Consider lifestyle modifications and monitoring."
                else:
                    interpretation["status"] = "high"
                    interpretation["interpretation"] = "Total cholesterol is high. Consult your healthcare provider for management strategies."
        else:
            interpretation["interpretation"] = f"Metric {metric} analysis not available"
        
        return interpretation
        
    finally:
        db.close()


@mcp.tool()
def check_health_concerns(user_id: int) -> Dict[str, Any]:
    """
    Check for potential health concerns based on recent data.
    
    Args:
        user_id: User ID
    
    Returns:
        List of concerns and recommendations
    """
    db = SessionLocal()
    try:
        concerns = []
        recommendations = []
        
        # Get recent data (last 7 days)
        start_date = datetime.now() - timedelta(days=7)
        recent_data = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.date >= start_date
        ).all()
        
        if not recent_data:
            return {"message": "Insufficient recent data for analysis"}
        
        # Calculate averages
        heart_rates = [d.heart_rate for d in recent_data if d.heart_rate]
        sleep_hours = [d.sleep_hours for d in recent_data if d.sleep_hours]
        steps = [d.steps for d in recent_data if d.steps]
        
        # Check heart rate
        if heart_rates:
            avg_hr = sum(heart_rates) / len(heart_rates)
            if avg_hr > 100:
                concerns.append({
                    "type": "elevated_heart_rate",
                    "severity": "moderate",
                    "detail": f"Average resting heart rate is {avg_hr:.1f} bpm, which is above normal range (60-100 bpm)"
                })
                recommendations.append("Monitor heart rate throughout the day and note any patterns or triggers")
                recommendations.append("Consider consulting a healthcare provider if elevated heart rate persists")
        
        # Check sleep
        if sleep_hours:
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            if avg_sleep < 6:
                concerns.append({
                    "type": "insufficient_sleep",
                    "severity": "high",
                    "detail": f"Average sleep duration is {avg_sleep:.1f} hours, below recommended 7-9 hours"
                })
                recommendations.append("Establish a consistent bedtime routine")
                recommendations.append("Limit screen time before bed")
                recommendations.append("Create a sleep-conducive environment (dark, quiet, cool)")
        
        # Check activity
        if steps:
            avg_steps = sum(steps) / len(steps)
            if avg_steps < 5000:
                concerns.append({
                    "type": "low_activity",
                    "severity": "moderate",
                    "detail": f"Average daily steps is {avg_steps:.0f}, below minimum recommendation of 5,000"
                })
                recommendations.append("Gradually increase daily walking")
                recommendations.append("Take short walking breaks throughout the day")
        
        return {
            "concerns": concerns,
            "recommendations": list(set(recommendations)),  # Remove duplicates
            "analysis_period": "last_7_days",
            "disclaimer": "This is educational information, not medical advice. Consult healthcare professionals for medical concerns."
        }
        
    finally:
        db.close()


@mcp.tool()
def get_medical_context(user_id: int) -> Dict[str, Any]:
    """
    Get user's medical context and history.
    
    Args:
        user_id: User ID
    
    Returns:
        Medical history summary
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}
        
        # Get medical records
        records = db.query(MedicalRecord).filter(
            MedicalRecord.user_id == user_id
        ).all()
        
        context = {
            "user_info": {
                "age": user.age,
                "gender": user.gender
            },
            "medical_records": []
        }
        
        for record in records:
            context["medical_records"].append({
                "type": record.record_type,
                "date": record.date.isoformat() if record.date else None,
                "data": record.data,
                "notes": record.notes
            })
        
        return context
        
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
