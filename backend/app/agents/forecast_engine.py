import math


def analyze_decline(oil_rate_bpd: list[float], days_on_production: list[int]) -> dict:
    if len(oil_rate_bpd) < 2:
        return {"decline_rate": 0, "decline_type": "insufficient_data", "remaining_reserves": 0}

    n = len(oil_rate_bpd)
    qi = oil_rate_bpd[0]
    q_current = oil_rate_bpd[-1]
    total_days = days_on_production[-1] - days_on_production[0] if len(days_on_production) > 1 else 1

    if total_days <= 0 or qi <= 0:
        return {"decline_rate": 0, "decline_type": "exponential", "remaining_reserves": 0}

    nominal_decline = -(math.log(q_current / qi) / total_days) if q_current > 0 and qi > 0 else 0
    monthly_decline = (1 - math.exp(-nominal_decline * 30.5)) * 100 if nominal_decline > 0 else 0

    if nominal_decline > 0 and q_current > 0:
        remaining_reserves = q_current / nominal_decline * 365 / 1e6
    else:
        remaining_reserves = q_current * 365 * 5 / 1e6

    if monthly_decline < 5:
        decline_type = "exponential"
    elif monthly_decline < 15:
        decline_type = "harmonic"
    else:
        decline_type = "hyperbolic"

    return {
        "decline_rate": round(nominal_decline, 6),
        "monthly_decline_pct": round(monthly_decline, 2),
        "decline_type": decline_type,
        "remaining_reserves_mmboe": round(remaining_reserves, 2),
    }


def calculate_recovery(current_cumulative: float, ooip: float) -> dict:
    if ooip <= 0:
        return {"recovery_factor_pct": 0, "remaining_oil_mmboe": 0, "efficiency": "N/A"}
    rf = (current_cumulative / ooip) * 100
    remaining = ooip - current_cumulative
    if rf < 10:
        efficiency = "low"
    elif rf < 30:
        efficiency = "moderate"
    elif rf < 50:
        efficiency = "good"
    else:
        efficiency = "excellent"
    return {
        "recovery_factor_pct": round(rf, 2),
        "remaining_oil_mmboe": round(remaining, 2),
        "efficiency": efficiency,
    }


def detect_water_breakthrough(water_cut_pct: float, water_rate_bpd: float) -> dict:
    detected = water_cut_pct > 50 or water_rate_bpd > 5000
    severity = "low"
    if water_cut_pct > 80 or water_rate_bpd > 20000:
        severity = "critical"
    elif water_cut_pct > 60 or water_rate_bpd > 10000:
        severity = "high"
    elif water_cut_pct > 40 or water_rate_bpd > 5000:
        severity = "medium"

    return {
        "water_breakthrough_detected": detected,
        "severity": severity,
        "water_cut_pct": water_cut_pct,
        "recommendation": "Consider water shut-off or artificial lift optimization" if detected else "Production within normal parameters",
    }


def calculate_forecast_confidence(data_points: int, pressure_support: bool) -> int:
    base = 50
    data_bonus = min(data_points * 5, 30)
    pressure_bonus = 20 if pressure_support else 0
    return min(base + data_bonus + pressure_bonus, 99)


def generate_forecast_report(reservoir_name: str, findings: dict) -> str:
    report = f"# HydroForecast Analysis Report\n\n"
    report += f"## Reservoir: {reservoir_name}\n\n"
    report += f"### Decline Analysis\n"
    decline = findings.get("decline_analysis", {})
    report += f"- Decline Type: {decline.get('decline_type', 'N/A')}\n"
    report += f"- Monthly Decline: {decline.get('monthly_decline_pct', 'N/A')}%\n"
    report += f"- Remaining Reserves: {decline.get('remaining_reserves_mmboe', 'N/A')} MMBOE\n\n"
    report += f"### Recovery Analysis\n"
    recovery = findings.get("recovery_analysis", {})
    report += f"- Recovery Factor: {recovery.get('recovery_factor_pct', 'N/A')}%\n"
    report += f"- Efficiency: {recovery.get('efficiency', 'N/A')}\n\n"
    report += f"### Water Breakthrough\n"
    wb = findings.get("water_breakthrough", {})
    report += f"- Detected: {wb.get('water_breakthrough_detected', 'N/A')}\n"
    report += f"- Severity: {wb.get('severity', 'N/A')}\n"
    report += f"- Recommendation: {wb.get('recommendation', 'N/A')}\n\n"
    report += f"### Forecast Confidence\n"
    report += f"- Confidence: {findings.get('confidence', 0)}%\n"
    return report
