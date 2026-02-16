from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI(title="Founderskorea Blog")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 샘플 블로그 포스트 데이터
POSTS = [
    {
        "id": 1,
        "title": "Founderskorea에 오신 것을 환영합니다",
        "summary": "창업자들을 위한 커뮤니티, Founderskorea의 첫 번째 이야기입니다.",
        "content": """
            <p>안녕하세요! Founderskorea에 오신 것을 환영합니다.</p>
            <p>우리는 한국의 창업자들이 서로 연결되고, 배우고, 성장할 수 있는 플랫폼을 만들고 있습니다.</p>
            <p>이 블로그에서는 스타트업 생태계의 최신 소식, 창업 노하우, 그리고 성공 사례들을 공유할 예정입니다.</p>
            <p>함께 성장해 나가요!</p>
        """,
        "author": "Founderskorea Team",
        "date": "2026-02-17",
        "tag": "공지",
    },
    {
        "id": 2,
        "title": "2026년 스타트업 트렌드 전망",
        "summary": "올해 주목해야 할 스타트업 트렌드와 기회를 살펴봅니다.",
        "content": """
            <p>2026년은 AI와 자동화가 더욱 깊숙이 우리 생활에 들어오는 해가 될 것입니다.</p>
            <h3>주요 트렌드</h3>
            <ul>
                <li><strong>AI 에이전트</strong> - 단순 챗봇을 넘어 실제 업무를 수행하는 AI</li>
                <li><strong>기후테크</strong> - 탄소 중립을 위한 기술 솔루션</li>
                <li><strong>헬스케어 AI</strong> - 개인 맞춤형 건강 관리</li>
                <li><strong>크리에이터 이코노미</strong> - 1인 창업의 새로운 물결</li>
            </ul>
            <p>이 트렌드들을 잘 파악하고 준비하는 창업자가 성공할 것입니다.</p>
        """,
        "author": "Founderskorea Team",
        "date": "2026-02-15",
        "tag": "트렌드",
    },
    {
        "id": 3,
        "title": "초기 스타트업을 위한 MVP 전략",
        "summary": "최소 기능 제품(MVP)을 효과적으로 만드는 방법을 알아봅니다.",
        "content": """
            <p>MVP(Minimum Viable Product)는 스타트업의 첫 걸음입니다.</p>
            <h3>MVP 성공 원칙</h3>
            <ol>
                <li><strong>핵심 가치에 집중</strong> - 하나의 문제를 완벽하게 해결하세요</li>
                <li><strong>빠르게 출시</strong> - 완벽함보다 속도가 중요합니다</li>
                <li><strong>사용자 피드백</strong> - 데이터 기반으로 개선하세요</li>
                <li><strong>반복 개선</strong> - 작은 개선을 빠르게 반복하세요</li>
            </ol>
            <p>기억하세요: 완벽한 제품보다 빠른 학습이 더 중요합니다.</p>
        """,
        "author": "Founderskorea Team",
        "date": "2026-02-10",
        "tag": "전략",
    },
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": POSTS, "year": datetime.now().year},
    )


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: int):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        return templates.TemplateResponse(
            "404.html", {"request": request, "year": datetime.now().year}, status_code=404
        )
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post, "year": datetime.now().year},
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html", {"request": request, "year": datetime.now().year}
    )
