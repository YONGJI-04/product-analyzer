# Product Analyzer

제품 이미지를 업로드하면 **Claude Vision**이 제품명, 카테고리, 특징, 가격대, 장단점을 JSON으로 분석해주는 API

---

## 프로젝트 개요

e커머스, 쇼핑몰, 가격 비교 서비스에 활용 가능한 제품 이미지 자동 분석 API입니다. Claude Vision이 이미지만 보고 제품의 상세 정보를 추출하여 구조화된 JSON으로 반환합니다.

---

## 아키텍처

```
제품 이미지 업로드
            ↓
    Base64 인코딩
            ↓
    [ Claude Vision API ]
    claude-sonnet-4-6
    제품 정보 추출 + JSON 구조화
            ↓
    제품명 / 카테고리 / 특징 / 가격대 / 장단점 반환
```

---

## 분석 항목

| 항목 | 설명 |
|------|------|
| `product_name` | 제품명 추정 |
| `category` | 제품 카테고리 |
| `features` | 주요 특징 목록 |
| `target_audience` | 타겟 고객층 |
| `estimated_price_range` | 예상 가격대 (원화) |
| `pros` | 장점 목록 |
| `cons` | 단점 추정 목록 |
| `description` | 상세 설명 (2-3문장) |

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/analyze` | 제품 이미지 분석 |
| `GET` | `/docs` | Swagger UI |

---

## 요청 / 응답 예시

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@earphones.jpg"
```

**응답:**

```json
{
  "analysis": {
    "product_name": "무선 블루투스 이어폰",
    "category": "전자기기 / 음향기기",
    "features": ["노이즈 캔슬링", "터치 컨트롤", "IPX4 방수"],
    "target_audience": "20-30대 직장인 및 학생",
    "estimated_price_range": "5만원 - 15만원",
    "pros": ["높은 휴대성", "깔끔한 디자인", "편리한 터치 조작"],
    "cons": ["배터리 수명 미확인", "음질은 외관상 판단 어려움"],
    "description": "인이어 타입의 완전 무선 블루투스 이어폰으로 보입니다. 미니멀한 케이스 디자인과 컴팩트한 이어버드 크기가 특징입니다."
  }
}
```

---

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8006
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 |
