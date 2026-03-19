#!/usr/bin/env python3
from __future__ import annotations

from enum import Enum
from typing import Any, Dict


class RiskFactor(Enum):
    BASE_SEVERITY = "base_severity"
    CONFIDENCE = "confidence"
    EXPLOITABILITY = "exploitability"
    IMPACT = "impact"
    DATA_FLOW_LENGTH = "data_flow_length"
    SANITIZER_PRESENT = "sanitizer_present"
    TEST_CODE = "test_code"


class RiskCalculator:
    BASE_SEVERITY_MAP: Dict[str, float] = {
        "严重漏洞": 10.0,
        "高危": 8.0,
        "中危": 6.0,
        "低危": 4.0,
    }

    EXPLOITABILITY_MAP: Dict[str, float] = {
        "容易利用": 1.0,
        "需要条件": 0.7,
        "困难": 0.4,
    }

    IMPACT_MAP: Dict[str, float] = {
        "严重": 1.0,
        "中等": 0.7,
        "轻微": 0.4,
    }

    def calculate_risk_score(
        self,
        base_severity: float,
        confidence: float,
        exploitability: float,
        impact: float,
        data_flow_length: int,
        has_sanitizer: bool,
        is_test_code: bool,
    ) -> float:
        normalized_confidence = self._clamp(confidence, 0.0, 1.0)
        normalized_exploitability = self._clamp(exploitability, 0.0, 1.0)
        normalized_impact = self._clamp(impact, 0.0, 1.0)

        score = base_severity * normalized_confidence
        score *= 0.5 + normalized_exploitability * 0.5
        score *= 0.5 + normalized_impact * 0.5

        if data_flow_length > 3:
            score *= 0.8
        if has_sanitizer:
            score *= 0.7
        if is_test_code:
            score *= 0.3

        return round(self._clamp(score, 0.0, 10.0), 2)

    def score_to_severity(self, score: float) -> str:
        if score >= 9.0:
            return "严重"
        if score >= 7.0:
            return "高危"
        if score >= 4.0:
            return "中危"
        if score >= 1.0:
            return "低危"
        return "信息"

    def get_risk_factors(
        self,
        severity_label: str,
        confidence: float,
        exploitability_label: str,
        impact_label: str,
        data_flow_length: int,
        has_sanitizer: bool,
        is_test_code: bool,
    ) -> Dict[str, Any]:
        base_severity = self.BASE_SEVERITY_MAP.get(severity_label)
        if base_severity is None:
            raise ValueError(f"不支持的基础严重等级: {severity_label}")

        exploitability = self.EXPLOITABILITY_MAP.get(exploitability_label)
        if exploitability is None:
            raise ValueError(f"不支持的可利用性等级: {exploitability_label}")

        impact = self.IMPACT_MAP.get(impact_label)
        if impact is None:
            raise ValueError(f"不支持的影响等级: {impact_label}")

        score = self.calculate_risk_score(
            base_severity=base_severity,
            confidence=confidence,
            exploitability=exploitability,
            impact=impact,
            data_flow_length=data_flow_length,
            has_sanitizer=has_sanitizer,
            is_test_code=is_test_code,
        )

        return {
            RiskFactor.BASE_SEVERITY.value: base_severity,
            RiskFactor.CONFIDENCE.value: self._clamp(confidence, 0.0, 1.0),
            RiskFactor.EXPLOITABILITY.value: exploitability,
            RiskFactor.IMPACT.value: impact,
            RiskFactor.DATA_FLOW_LENGTH.value: data_flow_length,
            RiskFactor.SANITIZER_PRESENT.value: has_sanitizer,
            RiskFactor.TEST_CODE.value: is_test_code,
            "score": score,
            "severity": self.score_to_severity(score),
        }

    def calculate_confidence(
        self,
        evidence_quality: float,
        has_source: bool,
        has_sink: bool,
        has_data_flow: bool,
        manual_verified: bool = False,
    ) -> float:
        score = self._clamp(evidence_quality, 0.0, 1.0) * 0.6
        if has_source:
            score += 0.1
        if has_sink:
            score += 0.1
        if has_data_flow:
            score += 0.15
        if manual_verified:
            score += 0.15
        return round(self._clamp(score, 0.0, 1.0), 2)

    @staticmethod
    def _clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(max_value, value))


def main() -> int:
    calculator = RiskCalculator()
    confidence = calculator.calculate_confidence(
        evidence_quality=0.9,
        has_source=True,
        has_sink=True,
        has_data_flow=True,
        manual_verified=False,
    )

    factors = calculator.get_risk_factors(
        severity_label="高危",
        confidence=confidence,
        exploitability_label="需要条件",
        impact_label="中等",
        data_flow_length=5,
        has_sanitizer=True,
        is_test_code=False,
    )

    print("风险评分结果:", factors)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
