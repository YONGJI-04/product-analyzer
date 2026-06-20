# product-analyzer

제품 이미지 → Claude Vision 상세 분석

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 http://localhost:8000/docs 접속
