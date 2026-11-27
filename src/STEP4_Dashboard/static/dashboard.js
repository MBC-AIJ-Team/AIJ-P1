// AI 기사 조회 요청 ID
let articleRequestId = 0;

// 개표 데이터 조회 요청 ID
let electionRequestId = 0;
let regionRequestId = 0;
let chartRequestId = 0;

async function loadElectionResults() {

    const requestId = ++electionRequestId;

    const finalStep = Number(
        document.getElementById("step-select").value
    );

    if (finalStep === 0) {
        return;
    }

    const container = document.getElementById("candidate-results");

    try {
        // FastAPI에서 가상 선거 데이터 가져오기
        const response = await fetch("/api/election-results");

        if (!response.ok) {
            throw new Error("서버 응답 오류: " + response.status);
        }

        const result = await response.json();

// 이전 요청 또는 변경된 개표 단계의 응답 무시
if (
    requestId !== electionRequestId ||
    finalStep !== Number(
        document.getElementById("step-select").value
    )
) {
    return;
}

// 개표 현황 갱신
updateCountingStatus(result.data, finalStep);

// 선택된 단계의 후보별 데이터 합산
const finalRows = result.data.filter(
    row => Number(row.step) === finalStep
);


        const candidates = {};

        finalRows.forEach(row => {
            const name = row.candidate_name;

            if (!candidates[name]) {
                candidates[name] = 0;
            }

            candidates[name] += Number(row.votes);
        });

        const totalVotes = Object.values(candidates)
            .reduce((sum, votes) => sum + votes, 0);

        // 득표수가 많은 순서로 정렬
        const ranking = Object.entries(candidates)
            .sort((a, b) => b[1] - a[1]);

        const colors = {
            "이몽룡": "#3b82f6",
            "심청": "#ef4444",
            "홍길동": "#22c55e"
        };

        // HTML 화면에 결과 출력
        container.innerHTML = ranking.map(([name, votes], index) => {
            const percentage = totalVotes > 0
                ? (votes / totalVotes * 100).toFixed(2)
                : "0.00";

            const color = colors[name] || "#94a3b8";

            return `
                <div class="candidate-item">
                    <div class="candidate-line">
                        <strong>${index + 1}위 · ${name}</strong>
                        <span class="candidate-votes">${votes.toLocaleString("ko-KR")}표</span>
                        <strong style="color:${color};">${percentage}%</strong>
                    </div>
                    <div class="candidate-track">
                        <div class="candidate-fill" style="width:${percentage}%; background:${color};"></div>
                    </div>
                </div>
            `;
        }).join("");

        console.log("후보별 개표 데이터 로드 완료");

    } catch (error) {

    if (
        requestId !== electionRequestId ||
        finalStep !== Number(
            document.getElementById("step-select").value
        )
    ) {
        return;
    }

    console.error(error);
    container.textContent = "개표 데이터를 불러오지 못했습니다.";
}
}



async function loadRegionResults() {

    const requestId = ++regionRequestId;

    const finalStep = Number(
        document.getElementById("step-select").value
    );

    if (finalStep === 0) {
        return;
    }

    const container = document.getElementById("region-results");

    try {
        const response = await fetch("/api/election-results");

        if (!response.ok) {
            throw new Error("서버 응답 오류: " + response.status);
        }

        const result = await response.json();

// 이전 요청 또는 변경된 개표 단계의 응답 무시
if (
    requestId !== regionRequestId ||
    finalStep !== Number(
        document.getElementById("step-select").value
    )
) {
    return;
}

        const finalRows = result.data.filter(
            row => Number(row.step) === finalStep
        );

        // 지역별, 후보별 득표수 정리
        const regions = {};

        finalRows.forEach(row => {
            const region = row.region;
            const candidate = row.candidate_name;

            if (!regions[region]) {
                regions[region] = {};
            }

            regions[region][candidate] =
                (regions[region][candidate] || 0) + Number(row.votes);
        });

        const regionOrder = [
            "중앙구", "동부구", "서부구", "남부구", "북부구"
        ];

        const candidateOrder = ["이몽룡", "심청", "홍길동"];

        // HTML 표 생성
        const tableRows = regionOrder.map(region => {
            const votes = regions[region] || {};

            const cells = candidateOrder.map(candidate => {
                const count = votes[candidate] || 0;
                return `<td>${count.toLocaleString("ko-KR")}</td>`;
            }).join("");

            return `<tr><th scope="row">${region}</th>${cells}</tr>`;
        }).join("");

        container.innerHTML = `
            <div style="overflow-x:auto;">
                <table class="election-table">
                    <thead>
                        <tr>
                            <th>지역</th>
                            <th>이몽룡</th>
                            <th>심청</th>
                            <th>홍길동</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            </div>
        `;

        console.log("지역별 개표 현황 로드 완료");

    } catch (error) {

    if (
        requestId !== regionRequestId ||
        finalStep !== Number(
            document.getElementById("step-select").value
        )
    ) {
        return;
    }

    console.error(error);
    container.textContent = "지역별 데이터를 불러오지 못했습니다.";
}
}



async function loadVoteChart() {

    const requestId = ++chartRequestId;

    const currentStep = Number(
        document.getElementById("step-select").value
    );

    if (currentStep === 0) {
        return;
    }

    const container = document.getElementById("vote-chart");

    try {
        const response = await fetch("/api/election-results");

        if (!response.ok) {
            throw new Error("서버 응답 오류: " + response.status);
        }

        const result = await response.json();

// 이전 요청 또는 변경된 개표 단계의 응답 무시
if (
    requestId !== chartRequestId ||
    currentStep !== Number(
        document.getElementById("step-select").value
    )
) {
    return;
}

        const candidateNames = ["이몽룡", "심청", "홍길동"];

        const colors = {
            "이몽룡": "#3b82f6",
            "심청": "#ef4444",
            "홍길동": "#22c55e"
        };

               
        
        // 현재 단계까지의 개표 데이터만 표시
        const steps = [...new Set(
            result.data
                .map(row => Number(row.step))
                .filter(step => step <= currentStep)
        )].sort((a, b) => a - b);


        // 개표 단계별 후보 득표수 합산
        const traces = candidateNames.map(name => {
            const percentages = steps.map(step => {
                const stepRows = result.data.filter(
                    row => Number(row.step) === step
                );

                const totalVotes = stepRows.reduce(
                    (sum, row) => sum + Number(row.votes), 0
                );

                const candidateVotes = stepRows
                    .filter(row => row.candidate_name === name)
                    .reduce(
                        (sum, row) => sum + Number(row.votes), 0
                    );

                return totalVotes > 0
                    ? candidateVotes / totalVotes * 100
                    : 0;
            });

            return {
                x: steps,
                y: percentages,
                mode: "lines+markers",
                name: name,
                line: {
                    color: colors[name],
                    width: 3
                },
                marker: {
                    size: 7
                },
                hovertemplate:
                    "개표 %{x}단계<br>" +
                    name + ": %{y:.2f}%<extra></extra>"
            };
        });

        const layout = {
            paper_bgcolor: "#0f1d30",
            plot_bgcolor: "#0f1d30",
            font: { color: "#cbd5e1" },
            xaxis: {
                title: { text: "개표 단계", standoff: 5 },
                tickmode: "array",
                tickvals: steps,
                gridcolor: "#334155"
            },
            yaxis: {
                title: { text: "득표율", standoff: 5 },
                ticksuffix: "%",
                gridcolor: "#334155",
                rangemode: "tozero"
            },
            legend: {
                orientation: "h",
                x: 0,
                y: 1.02,
                yanchor: "bottom"
            },
            margin: {
                l: 52, r: 12, t: 32, b: 42
            },
            autosize: true
        };

        await Plotly.newPlot(
            container,
            traces,
            layout,
            {
                responsive: true,
                displaylogo: false
            }
        );

        console.log("득표율 변화 그래프 표시 완료");

    } catch (error) {

    if (
        requestId !== chartRequestId ||
        currentStep !== Number(
            document.getElementById("step-select").value
        )
    ) {
        return;
    }

    console.error(error);
    container.textContent = "그래프를 표시하지 못했습니다.";
}
}



document.addEventListener("DOMContentLoaded", () => {
    const stepSelect = document.getElementById("step-select");
    const stepInfo = document.getElementById("selected-step-info");

    
stepSelect.addEventListener("change", () => {
    const selectedStep = stepSelect.value;

    // STEP 10 - 개표 대기 선택 시 화면 초기화
    if (Number(selectedStep) === 0) {
        resetDashboard();
        return;
    }

    // 현재 선택한 개표 단계 표시
    stepInfo.textContent =
        `현재 조회 단계: ${selectedStep}단계`;


        // 선택한 단계의 후보별 개표 데이터 다시 계산
        loadElectionResults();

        // 선택한 단계의 지역별 개표 데이터 다시 계산
        loadRegionResults();

        loadVoteChart().then(highlightSelectedStep);

// AI 뉴스 기사 자동 갱신
loadAIArticle();

console.log(`개표 ${selectedStep}단계 조회 완료`);

        console.log(`개표 ${selectedStep}단계 조회 완료`);
    });
});


function highlightSelectedStep() {
    const chart = document.getElementById("vote-chart");
    const step = Number(
        document.getElementById("step-select").value
    );

    // Plotly 그래프가 생성되었는지 확인
    if (!chart || !chart.data) {
        return;
    }

    // 선택한 개표 단계에 노란색 세로선 표시
    Plotly.relayout(chart, {
        shapes: [{
            type: "line",
            xref: "x",
            yref: "paper",
            x0: step,
            x1: step,
            y0: 0,
            y1: 1,
            line: {
                color: "#facc15",
                width: 2,
                dash: "dash"
            }
        }]
    });
}



/* ==========================================
   STEP 5-21: WebSocket 개표 제어 기능
   ========================================== */

let electionWS = null;

// 상태 표시 함수

function updateWSStatus(id, message) {

    const element = document.getElementById(id);

    if (!element) {
        return;
    }

    element.textContent = message;

    // 연결 상태와 개표 진행 상태에만 색상 적용
    if (
        id !== "ws-connection-status" &&
        id !== "ws-playback-status"
    ) {
        return;
    }

    // 이전 상태 색상 제거
    element.classList.remove(
        "status-success",
        "status-active",
        "status-warning",
        "status-error",
        "status-idle"
    );

    // 상태별 CSS 클래스 설정
    const statusClasses = {
        "연결됨": "status-success",
        "개표 완료": "status-success",
        "개표 진행 중": "status-active",
        "일시정지": "status-warning",
        "연결 시도 중": "status-warning",
        "연결 종료 · 재연결 시도 중": "status-warning",
        "연결 종료": "status-error",
        "연결 오류": "status-error",
        "대기 중": "status-idle"
    };

    const statusClass = statusClasses[message];

    if (statusClass) {
    element.classList.add(statusClass);
}

// 개표 제어 버튼 상태 갱신
updateControlButtons();
}


// WebSocket 연결
function connectElectionWS() {
    const protocol =
        location.protocol === "https:" ? "wss:" : "ws:";

    const wsUrl = `${protocol}//${location.host}/ws`;

    electionWS = new WebSocket(wsUrl);

    // 연결 성공
    

electionWS.onopen = () => {

    // 최초 연결 및 재연결 시 화면 초기화
    resetDashboard();

    // 실시간 개표 단계 초기화
    updateWSStatus(
        "ws-current-step",
        "0 / 10"
    );

    // 개표 진행 상태 초기화
    updateWSStatus(
        "ws-playback-status",
        "대기 중"
    );

    // 서버 연결 성공 표시
    updateWSStatus(
        "ws-connection-status",
        "연결됨"
    );

    // 이전 연결 오류 메시지 제거
    updateWSStatus(
        "ws-error-message",
        ""
    );

    // 개표 제어 버튼 상태 갱신
    updateControlButtons();

    console.log("WebSocket 연결 성공");
    console.log("WebSocket 연결 후 화면 상태 동기화 완료");
};



    // 서버 데이터 수신
    electionWS.onmessage = (event) => {
        const result = JSON.parse(event.data);

        
if (result.type === "election_update") {

    // 현재 개표 단계 표시
    updateWSStatus(
        "ws-current-step",
        `${result.step} / 10`
    );

    // 재생 상태 표시
    updateWSStatus(
        "ws-playback-status",
        "개표 진행 중"
    );

    // 기존 대시보드의 단계 선택값 변경
    const stepSelect = document.getElementById("step-select");

    
if (stepSelect) {
    stepSelect.value = String(result.step);

    // 현재 선택된 단계 정보 표시
    const stepInfo = document.getElementById(
        "selected-step-info"
    );

    if (stepInfo) {
        stepInfo.textContent =
            `현재 조회 단계: ${result.step}단계`;
    }

    // 기존 대시보드 데이터 갱신
loadElectionResults();
loadRegionResults();

// Plotly 득표율 그래프 갱신
loadVoteChart();

// STEP 10 - 실시간 AI 뉴스 기사 자동 갱신
loadAIArticle();
}


    console.log(
        `개표 ${result.step}/10 단계 수신`,
        result.data
    );
}


        
        else if (result.type === "playback_status") {

            const statusText = {
                paused: "일시정지",
                playing: "개표 진행 중",
                reset: "대기 중"
            };

            updateWSStatus(
                "ws-playback-status",
                statusText[result.status] || result.status
            );

            updateWSStatus(
                "ws-current-step",
                `${result.step} / 10`
            );

            // 개표 초기화 시 공통 초기화 함수 실행
            if (result.status === "reset") {

                resetDashboard();

                console.log("개표 화면 초기화 완료");
            }
        }

        else if (result.type === "election_complete") {

            updateWSStatus(
                "ws-playback-status",
                "개표 완료"
            );
        }

        else if (result.type === "error") {

            updateWSStatus(
                "ws-error-message",
                result.message
            );
        }
    };


    // 연결 오류
    electionWS.onerror = () => {
        updateWSStatus(
            "ws-error-message",
            "WebSocket 연결 오류가 발생했습니다."
        );
    };

    // 연결 종료
    
    // 서버 연결 종료 시 자동 재연결
    electionWS.onclose = () => {
        updateWSStatus(
            "ws-connection-status",
            "연결 종료 · 재연결 시도 중"
        );

        // 3초 후 WebSocket 연결 재시도
        setTimeout(() => {
            // 이미 연결되어 있다면 중복 연결하지 않음
            if (
                !electionWS ||
                electionWS.readyState === WebSocket.CLOSED
            ) {
                console.log("WebSocket 재연결 시도");
                connectElectionWS();
            }
        }, 3000);
    };

}

// 명령 전송
function sendElectionCommand(command) {
    if (!electionWS || electionWS.readyState !== WebSocket.OPEN) {
        updateWSStatus(
            "ws-error-message",
            "WebSocket 서버에 연결되어 있지 않습니다."
        );
        return;
    }

    updateWSStatus("ws-error-message", "");
    electionWS.send(command);
}


// 버튼 이벤트 연결
function initializeElectionControls() {

    const buttons = {
        "ws-start-btn": "start",
        "ws-pause-btn": "pause",
        "ws-resume-btn": "resume",
        "ws-reset-btn": "reset"
    };

    for (const [buttonId, command] of Object.entries(buttons)) {

        const button = document.getElementById(buttonId);

        if (button) {
            button.addEventListener("click", () => {
                sendElectionCommand(command);
            });
        }
    }

    // 버튼 준비 후 WebSocket 연결
    connectElectionWS();

    // 최초 버튼 활성화 상태 설정
    updateControlButtons();
}

// HTML 화면이 준비되면 초기화
if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        initializeElectionControls
    );
} else {
    initializeElectionControls();
}



/* ==========================================
   STEP 6 - RAG 기반 AI 뉴스 기사 표시
   ========================================== */



// AI 기사 불러오기
async function loadAIArticle() {

    const requestId = ++articleRequestId;

    const button = document.getElementById(
        "ai-article-load-btn"
    );

    const status = document.getElementById(
        "ai-article-status"
    );

    const errorMessage = document.getElementById(
        "ai-article-error"
    );

    // 현재 선택된 개표 단계
const stepSelect = document.getElementById("step-select");
const step = stepSelect ? Number(stepSelect.value) : 0;

// 개표 대기 상태에서는 AI 기사 조회 차단
if (!Number.isInteger(step) || step < 1 || step > 10) {
    resetAIArticle();
    return;
}


// 이전 오류 메시지 초기화
errorMessage.textContent = "";
status.textContent = "불러오는 중";
status.style.color = "#93C5FD";

// AI 기사 조회 단계 표시
document.getElementById("ai-article-step").textContent =
    `${step}단계 조회 중`;

// 이전 승인 정보 초기화
document.getElementById("ai-article-approved-by").textContent = "-";
document.getElementById("ai-article-approved-at").textContent = "-";
document.getElementById("ai-article-approval-reason").textContent = "-";

const approvalNotice = document.getElementById(
    "ai-article-approval-notice"
);

approvalNotice.textContent = "※ 기사 및 승인 상태를 확인하고 있습니다.";
approvalNotice.style.color = "#93C5FD";

button.disabled = true;


    try {
        // FastAPI에서 저장된 AI 기사 가져오기
        const response = await fetch(
            `/api/ai-article?step=${step}`
        );

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error(
                    `${step}단계 AI 기사가 아직 생성되지 않았습니다.`
                );
            }

            throw new Error(
                `기사 조회 오류: HTTP ${response.status}`
            );
        }

        const result = await response.json();

// 최신 요청이 아니면 화면에 표시하지 않음
if (requestId !== articleRequestId) {
    return;
}

const article = result.article;

        if (!article || typeof article.article !== "string") {
            throw new Error("기사 데이터 형식이 올바르지 않습니다.");
        }

        // 첫 줄이 Markdown 제목이면 제목과 본문 분리
        const lines = article.article.trim().split("\n");

        let title = "AI 선거 뉴스 기사";
        let body = article.article.trim();

        if (lines[0].startsWith("# ")) {
            title = lines[0].replace(/^#\s*/, "");
            body = lines.slice(1).join("\n").trim();
        }

        // 기사 제목 및 본문 표시
        document.getElementById(
            "ai-article-title"
        ).textContent = title;

        document.getElementById(
            "ai-article-body"
        ).textContent = body;

        
// 기사 승인 상태
const isApproved = article.status === "승인";

status.textContent = isApproved ? "승인" : "검토 필요";
status.style.color = isApproved ? "#4ADE80" : "#FBBF24";

// 승인자
document.getElementById(
    "ai-article-approved-by"
).textContent = isApproved
    ? (article.approved_by || "-")
    : "-";

// 승인시각
document.getElementById(
    "ai-article-approved-at"
).textContent = isApproved
    ? (article.approved_at || "-")
    : "-";

// 승인 사유
document.getElementById(
    "ai-article-approval-reason"
).textContent = isApproved
    ? (article.approval_reason || "-")
    : "-";

// 승인 상태에 따른 안내 문구
if (isApproved) {
    approvalNotice.textContent =
        "✓ 본 기사는 AI가 생성하고 편집자가 최종 승인한 기사입니다.";

    approvalNotice.style.color = "#4ADE80";
} else {
    approvalNotice.textContent =
        "※ 본 기사는 AI가 생성한 초안이며 편집자의 최종 승인을 받지 않았습니다.";

    approvalNotice.style.color = "#FBBF24";
}


        // 개표 기준시각
        document.getElementById(
            "ai-article-timestamp"
        ).textContent = article.timestamp || "-";

        // RAG 근거 ID
        document.getElementById(
            "ai-article-evidence"
        ).textContent = Array.isArray(article.evidence_ids)
            ? article.evidence_ids.join(", ")
            : "-";

        // AI 모델
        document.getElementById(
            "ai-article-model"
        ).textContent = article.model || "-";

        // 현재 조회 완료된 AI 기사 단계 표시
document.getElementById("ai-article-step").textContent =
    `${step} / 10단계 기사`;

console.log(`AI 기사 ${step}단계 조회 완료`);

    } catch (error) {

    // 이전 요청의 오류는 무시
    if (requestId !== articleRequestId) {
        return;
    }

    console.error("AI 기사 조회 실패:", error);

        
status.textContent = "조회 실패";
status.style.color = "#F87171";

// 기사 조회 실패 단계 표시
document.getElementById("ai-article-step").textContent =
    `${step}단계 조회 실패`;

errorMessage.textContent = error.message;

// 이전 기사 정보 제거
document.getElementById("ai-article-title").textContent =
    "AI 기사 조회 실패";

document.getElementById("ai-article-body").textContent = "";
document.getElementById("ai-article-timestamp").textContent = "-";
document.getElementById("ai-article-evidence").textContent = "-";
document.getElementById("ai-article-model").textContent = "-";

document.getElementById("ai-article-approved-by").textContent = "-";
document.getElementById("ai-article-approved-at").textContent = "-";
document.getElementById("ai-article-approval-reason").textContent = "-";

approvalNotice.textContent =
    "※ 기사를 조회하지 못해 승인 상태를 확인할 수 없습니다.";

approvalNotice.style.color = "#F87171";


    } finally {

    // 최신 요청만 버튼 상태 변경
    if (requestId === articleRequestId) {
        button.disabled = false;
    }
}
}


// AI 기사 조회 버튼 이벤트 연결
document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById(
        "ai-article-load-btn"
    );

    if (button) {
        button.addEventListener("click", loadAIArticle);
    }

});


// ============================================
// 개표 단계별 개표 현황 갱신
// ============================================

function updateCountingStatus(rows, step) {

    step = Number(step);

    // 현재 개표 단계의 데이터 추출
    const stepRows = rows.filter(
        row => Number(row.step) === step
    );

    // 지역별 중복 데이터 제거
    const regionMap = new Map();

    for (const row of stepRows) {
        if (!regionMap.has(row.region_id)) {
            regionMap.set(row.region_id, row);
        }
    }

    const regions = [...regionMap.values()];

    // 개표 데이터가 없는 경우
    if (step !== 0 && regions.length !== 5) {
        console.error("개표 현황 데이터 부족:", step);
        return;
    }

    // 지역별 개표 데이터 합산
    const counted = regions.reduce(
        (sum, row) => sum + Number(row.counted_ballots), 0
    );

    const valid = regions.reduce(
        (sum, row) => sum + Number(row.valid_votes), 0
    );

    const invalid = regions.reduce(
        (sum, row) => sum + Number(row.invalid_votes), 0
    );

    // 전체 투표수: 지역별 중복 제거 후 계산
    const totalRegionMap = new Map();

    for (const row of rows) {
        if (!totalRegionMap.has(row.region_id)) {
            totalRegionMap.set(row.region_id, row);
        }
    }

    const total = [...totalRegionMap.values()].reduce(
        (sum, row) => sum + Number(row.total_ballots), 0
    );

    if (!Number.isFinite(total) || total <= 0) {
        console.error("전체 투표수 데이터 오류");
        return;
    }

    const remaining = total - counted;
    const progress = counted / total * 100;

    const timestamp = stepRows.length > 0
        ? stepRows[0].timestamp
        : "-";

    // 화면에 개표 현황 표시
    document.getElementById("counting-step")
        .textContent = step;

    document.getElementById("counting-timestamp")
        .textContent = timestamp;

    document.getElementById("counting-counted-ballots")
        .textContent = counted.toLocaleString("ko-KR") + "표";

    document.getElementById("counting-remaining-ballots")
        .textContent = remaining.toLocaleString("ko-KR") + "표";

    document.getElementById("counting-valid-votes")
        .textContent = valid.toLocaleString("ko-KR") + "표";

    document.getElementById("counting-invalid-votes")
        .textContent = invalid.toLocaleString("ko-KR") + "표";

    document.getElementById("counting-progress-pct")
        .textContent = progress.toFixed(2) + "%";

    document.getElementById("counting-progress-bar")
        .style.width = progress + "%";
}


// ============================================
// 개표 현황 초기화
// ============================================

function resetCountingStatus() {

    document.getElementById("counting-step")
        .textContent = "0";

    document.getElementById("counting-timestamp")
        .textContent = "-";

    document.getElementById("counting-progress-pct")
        .textContent = "0.00%";

    document.getElementById("counting-progress-bar")
        .style.width = "0%";

    document.getElementById("counting-counted-ballots")
        .textContent = "0표";

    document.getElementById("counting-remaining-ballots")
        .textContent = "350,000표";

    document.getElementById("counting-valid-votes")
        .textContent = "0표";

    document.getElementById("counting-invalid-votes")
        .textContent = "0표";
}


 // ============================================
 // STEP 10 - AI 뉴스 기사 초기화
 // ============================================

 function resetAIArticle() {

    // 진행 중인 이전 기사 요청 무효화
    articleRequestId++;

    const button = document.getElementById(
        "ai-article-load-btn"
    );

    if (button) {
    const step = Number(
        document.getElementById("step-select").value
    );

    button.disabled = step === 0;
}

    const resetFields = {
    "ai-article-step": "조회 대기",
    "ai-article-title": "AI 선거 뉴스 기사",
         "ai-article-body": "개표가 시작되면 기사를 조회할 수 있습니다.",
         "ai-article-status": "대기 중",
         "ai-article-timestamp": "-",
         "ai-article-evidence": "-",
         "ai-article-model": "-",
         "ai-article-approved-by": "-",
         "ai-article-approved-at": "-",
         "ai-article-approval-reason": "-",
         "ai-article-error": "",
         "ai-article-approval-notice":
             "※ 개표 시작 전입니다."
     };

     for (const [id, value] of Object.entries(resetFields)) {

         const element = document.getElementById(id);

         if (element) {
             element.textContent = value;
         }
     }

     const status = document.getElementById(
         "ai-article-status"
     );

     if (status) {
         status.style.color = "#94a3b8";
     }

     const notice = document.getElementById(
         "ai-article-approval-notice"
     );

     if (notice) {
         notice.style.color = "#94a3b8";
     }

     console.log("AI 뉴스 기사 초기화 완료");
 }


// ============================================
// STEP 10 - 개표 제어 버튼 활성화 관리
// ============================================

function updateControlButtons() {

    const isConnected =
        electionWS &&
        electionWS.readyState === WebSocket.OPEN;

    const status = document.getElementById(
        "ws-playback-status"
    )?.textContent.trim();

    const buttonStates = {
        "ws-start-btn":
            isConnected &&
            (status === "대기 중" ||
             status === "개표 완료"),

        "ws-pause-btn":
            isConnected &&
            status === "개표 진행 중",

        "ws-resume-btn":
            isConnected &&
            status === "일시정지",

        "ws-reset-btn":
            isConnected
    };

    for (const [id, enabled] of Object.entries(buttonStates)) {

        const button = document.getElementById(id);

        if (button) {
            button.disabled = !enabled;
        }
    }
}



// ============================================
// STEP 10 - 공통 대시보드 초기화 함수
// ============================================

function resetDashboard() {

    // 진행 중인 개표 데이터 요청 무효화
    electionRequestId++;
    regionRequestId++;
    chartRequestId++;

    // 조회 단계 초기화
    document.getElementById("step-select").value = "0";

    document.getElementById("selected-step-info")
        .textContent = "개표 대기 중";

    // 개표 현황 초기화
    resetCountingStatus();

    // AI 뉴스 기사 초기화
    resetAIArticle();

    // 후보별 개표 현황 초기화
    document.getElementById("candidate-results")
        .textContent = "개표 시작 전입니다.";

    // 지역별 개표 현황 초기화
    document.getElementById("region-results")
        .textContent = "개표 시작 전입니다.";

    // Plotly 그래프 초기화
    const chart = document.getElementById("vote-chart");

    if (chart) {

        if (typeof Plotly !== "undefined" && chart.data) {
            Plotly.purge(chart);
        }

        chart.innerHTML =
            "<p style='color:#cbd5e1; padding:20px;'>" +
            "개표가 시작되면 그래프가 표시됩니다." +
            "</p>";
    }

    console.log("대시보드 화면 초기화 완료");
}


// 최초 접속 시 초기화
document.addEventListener("DOMContentLoaded", () => {

    resetDashboard();

    updateWSStatus("ws-current-step", "0 / 10");
    updateWSStatus("ws-playback-status", "대기 중");
});
