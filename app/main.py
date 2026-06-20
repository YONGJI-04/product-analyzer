import os
import base64
import json
import anthropic
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

app = FastAPI(title="Product Analyzer API", description="제품 이미지를 분석하여 상세 정보를 추출합니다", version="1.1.0")

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

ANALYSIS_PROMPT = """이 제품 이미지를 분석하여 다음 정보를 JSON 형식으로 반환해주세요:
{
  "product_name": "제품명",
  "category": "카테고리",
  "brand": "브랜드명 (확인 가능한 경우)",
  "features": ["특징1", "특징2", "특징3"],
  "estimated_price_range": "예상 가격대",
  "target_audience": "타겟 고객층",
  "pros": ["장점1", "장점2"],
  "cons": ["단점1", "단점2"],
  "overall_rating": "5점 만점 예상 평점 (숫자만)",
  "short_description": "한 문장 설명"
}
JSON만 반환하고 다른 텍스트는 포함하지 마세요."""

@app.get("/")
def root():
    return {"status": "running", "message": "Product Analyzer API"}

async def analyze_single(file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_TYPES:
        return {"filename": file.filename, "error": "지원하지 않는 파일 형식"}
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        return {"filename": file.filename, "error": "파일 크기 초과 (5MB 이하)"}
    b64 = base64.standard_b64encode(contents).decode("utf-8")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": file.content_type, "data": b64}},
            {"type": "text", "text": ANALYSIS_PROMPT}
        ]}]
    )
    try:
        analysis = json.loads(response.content[0].text)
    except json.JSONDecodeError:
        analysis = {"raw": response.content[0].text}
    return {"filename": file.filename, **analysis}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return await analyze_single(file)

@app.post("/analyze/batch")
async def analyze_batch(files: List[UploadFile] = File(...)):
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="한 번에 최대 5개 이미지까지 분석 가능합니다")
    results = []
    for file in files:
        result = await analyze_single(file)
        results.append(result)
    return {"count": len(results), "results": results}
