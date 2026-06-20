# Product Analyzer

제품 이미지를 업로드하면 Claude Vision이 상세 분석 정보를 JSON으로 반환하는 API

## 아키텍처

```
제품 이미지 업로드
        ↓
Claude Vision (claude-sonnet-4-6)
        ↓
제품명 / 카테고리 / 특징 / 가격대 / 장단점 분석
```

## 분석 항목

- 제품명 추정
- 카테고리
- 주요 특징 목록
- 타겟 고객층
- 예상 가격대 (원화)
- 장점 / 단점
- 상세 설명

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| POST | `/analyze` | 제품 이미지 분석 |
| GET | `/docs` | Swagger UI |

## 요청 예시

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@product.jpg"
```

## 응답 예시

```json
{
  "analysis": {
    "product_name": "무선 블루투스 이어폰",
    "category": "전자기기/음향기기",
    "features": ["노이즈 캔슬링", "터치 컨트롤", "방수 기능"],
    "target_audience": "20-30대 직장인 및 학생",
    "estimated_price_range": "5만원 - 15만원",
    "pros": ["휴대성", "음질"],
    "cons": ["배터리 수명 미확인"],
    "description": "..."
  }
}
```

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8006
```

## 환경 변수

```
ANTHROPIC_API_KEY=   # Anthropic Claude API 키
```
