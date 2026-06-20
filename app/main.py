import base64
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI(title="Product Analyzer API")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@app.get("/")
def root():
    return {"status": "running", "message": "Product Analyzer API"}


@app.post("/analyze")
async def analyze_product(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="JPG, PNG, GIF, WEBP만 지원합니다")

    image_bytes = await file.read()
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": file.content_type, "data": image_data},
                },
                {
                    "type": "text",
                    "text": """이 제품 이미지를 분석해서 JSON 형식으로 답변해주세요:

{
  "product_name": "제품명 추정",
  "category": "카테고리",
  "features": ["주요 특징 목록"],
  "target_audience": "타겟 고객층",
  "estimated_price_range": "예상 가격대 (원화)",
  "pros": ["장점"],
  "cons": ["단점 추정"],
  "description": "상세 설명 (2-3문장)"
}

JSON만 출력해주세요."""
                },
            ],
        }]
    )

    import json
    try:
        text = message.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        product_info = json.loads(text)
    except Exception:
        product_info = {"raw": message.content[0].text}

    return JSONResponse(content={"analysis": product_info})
