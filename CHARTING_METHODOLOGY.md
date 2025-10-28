# 리듬게임 노트 제작 방법론

## 목차

1. [개요](#개요)
2. [음악 이론 기초](#음악-이론-기초)
3. [오디오 분석 기술](#오디오-분석-기술)
4. [패턴 디자인 원칙](#패턴-디자인-원칙)
5. [난이도 설계](#난이도-설계)
6. [매핑 스타일](#매핑-스타일)
7. [품질 보증](#품질-보증)
8. [실전 워크플로우](#실전-워크플로우)
9. [고급 기법](#고급-기법)
10. [참고 자료](#참고-자료)

---

## 개요

리듬게임 차트 제작(Charting/Mapping)은 음악을 게임플레이로 변환하는 예술이자 과학입니다. 단순히 비트에 노트를 배치하는 것을 넘어, 음악의 감정과 에너지를 플레이어에게 전달하는 것이 목표입니다.

### 차트의 3가지 핵심 요소

1. **음악성 (Musicality)**: 실제 음악의 리듬, 멜로디, 하모니를 반영
2. **플레이성 (Playability)**: 손의 움직임이 자연스럽고 편안함
3. **재미 (Fun Factor)**: 플레이어에게 만족감과 성취감 제공

### 차트 제작의 철학

```
좋은 차트 = 음악의 정확한 표현 + 플레이어 경험 고려 + 난이도 균형
```

---

## 음악 이론 기초

### 1. 박자(Beat)와 BPM

**BPM (Beats Per Minute)**
- 1분에 몇 개의 박자가 있는지 나타내는 수치
- 일반적인 범위:
  - Ballad: 60-80 BPM
  - Pop: 100-130 BPM
  - Dance/EDM: 120-140 BPM
  - Drum & Bass: 160-180 BPM
  - Hardcore: 180-200+ BPM

**박자 간격 계산**
```javascript
// 1박자 간격 (초)
const beatInterval = 60 / bpm;

// 1/4 박자 간격
const quarterBeatInterval = beatInterval / 4;

// 예: 120 BPM
// 1박자 = 60/120 = 0.5초
// 1/4박자 = 0.125초 = 125ms
```

### 2. 박자 분할 (Beat Snap Divisor)

노트를 배치할 수 있는 시간 그리드:

| 분할 | 설명 | 사용 예시 |
|------|------|-----------|
| 1/1 | 1박자 단위 | 느린 곡, 초급 난이도 |
| 1/2 | 2분음표 (반박자) | 일반적인 드럼 패턴 |
| 1/3 | 3연음 | 셔플(Shuffle) 리듬 |
| 1/4 | 4분음표 | 가장 흔한 단위 |
| 1/6 | 6연음 | 빠른 3연음 |
| 1/8 | 8분음표 | 빠른 스트림 |
| 1/12 | 12연음 | 매우 빠른 3연음 트릴 |
| 1/16 | 16분음표 | 극도로 빠른 패턴 |

**박자 분할 선택 기준**
```
음악을 듣고 자연스럽게 손이 움직이는 리듬을 따라가세요.
- 규칙적이면 1/4 또는 1/8
- 스윙감이 있으면 1/3 또는 1/6
- 트리플렛(세잇단음표)은 1/3, 1/6, 1/12
```

### 3. 음악 구조

대부분의 곡은 다음 구조를 따릅니다:

```
Intro → Verse → Pre-Chorus → Chorus →
Verse → Pre-Chorus → Chorus →
Bridge → Final Chorus → Outro
```

**구간별 매핑 전략**
- **Intro**: 간단한 패턴, 플레이어 워밍업
- **Verse**: 중간 밀도, 멜로디 따라가기
- **Pre-Chorus**: 점진적 강도 증가
- **Chorus**: 최고 밀도, 강렬한 패턴
- **Bridge**: 대비를 위해 밀도 낮추기
- **Final Chorus**: 가장 어려운 패턴
- **Outro**: 점진적 감소

### 4. 음악 레이어

음악은 여러 레이어로 구성됩니다:

```
┌─────────────┐
│   Vocals    │ ← 가장 높은 우선순위
├─────────────┤
│   Melody    │ ← 리드 악기 (신스, 기타 등)
├─────────────┤
│   Harmony   │ ← 코드, 패드
├─────────────┤
│   Bass      │ ← 베이스 라인
├─────────────┤
│   Drums     │ ← 리듬 기반
└─────────────┘
```

**레이어별 매핑 우선순위**

1. **Kick (킥 드럼)**: 가장 중요, 왼손/낮은 레인
2. **Snare (스네어)**: 두 번째 중요, 중앙/오른손
3. **Hi-hat (하이햇)**: 리듬 필, 오른손/높은 레인
4. **Melody (멜로디)**: 보컬이나 리드 악기
5. **Synth/FX**: 강조 포인트

---

## 오디오 분석 기술

### 1. 주파수 대역 분류

음악의 주파수 스펙트럼을 분리하여 각 악기를 감지:

```javascript
const frequencyBands = {
    subBass:    { range: '20-60 Hz',    instruments: '서브베이스' },
    bass:       { range: '60-250 Hz',   instruments: '킥드럼, 베이스기타' },
    lowMid:     { range: '250-500 Hz',  instruments: '스네어, 탐' },
    mid:        { range: '500-2k Hz',   instruments: '보컬, 기타' },
    upperMid:   { range: '2k-4k Hz',    instruments: '클랩, 심벌' },
    presence:   { range: '4k-6k Hz',    instruments: '하이햇 (개방)' },
    brilliance: { range: '6k-20k Hz',   instruments: '크래쉬, 라이드 심벌' }
};
```

### 2. Onset Detection (음 시작점 감지)

**Spectral Flux 방법**

음의 시작점을 감지하는 가장 일반적인 방법:

```javascript
// 1. 스펙트럼 차이 계산
function spectralFlux(spectrum1, spectrum2) {
    let flux = 0;
    for (let i = 0; i < spectrum1.length; i++) {
        // 에너지 증가만 고려 (Half-Wave Rectification)
        flux += Math.max(0, spectrum2[i] - spectrum1[i]);
    }
    return flux;
}

// 2. Peak Picking (피크 선택)
function detectOnset(flux, threshold, localWindow) {
    const isPeak = flux[i] > flux[i-1] && flux[i] > flux[i+1];
    const aboveThreshold = flux[i] > threshold;
    const localMaximum = flux[i] == Math.max(...flux.slice(i-localWindow, i+localWindow));

    return isPeak && aboveThreshold && localMaximum;
}
```

**다른 Onset Detection 방법들**

1. **Energy-based**: RMS 에너지 급증 감지
2. **Phase-based**: 위상 변화 감지
3. **Complex Domain**: 복소수 스펙트럼 차이
4. **High Frequency Content**: 고주파 에너지 비율

### 3. Beat Tracking

**Dynamic Programming 방식**

```python
# madmom 라이브러리 사용 예제
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor

# 1. RNN으로 비트 활성화 함수 계산
beat_proc = RNNBeatProcessor()
activations = beat_proc('song.wav')

# 2. Dynamic Bayesian Network로 비트 타이밍 추정
beat_tracker = DBNBeatTrackingProcessor(fps=100)
beats = beat_tracker(activations)

# beats = [(0.5, 120), (1.0, 120), (1.5, 120), ...]
#         ↑ 시간    ↑ BPM
```

**비트 트래킹 정확도 향상**

1. **Multi-agent 방식**: 다양한 BPM 가설 동시 추적
2. **Tempo Induction**: 전체 곡의 템포 먼저 추정
3. **Downbeat Tracking**: 소절 첫 박자 감지

### 4. Tempo Estimation

```javascript
// Autocorrelation 방법
function estimateTempo(onsetTimes) {
    const intervals = [];

    // 모든 onset 간격 계산
    for (let i = 0; i < onsetTimes.length - 1; i++) {
        intervals.push(onsetTimes[i + 1] - onsetTimes[i]);
    }

    // 히스토그램으로 가장 흔한 간격 찾기
    const histogram = {};
    intervals.forEach(interval => {
        const rounded = Math.round(interval * 100) / 100;
        histogram[rounded] = (histogram[rounded] || 0) + 1;
    });

    // 가장 많이 나온 간격을 BPM으로 변환
    const mostCommonInterval = Object.keys(histogram).reduce((a, b) =>
        histogram[a] > histogram[b] ? a : b
    );

    return 60 / parseFloat(mostCommonInterval);
}
```

### 5. 적응형 임계값 (Adaptive Thresholding)

고정된 임계값 대신 로컬 평균을 사용:

```javascript
function adaptiveThreshold(signal, windowSize, multiplier) {
    const peaks = [];

    for (let i = windowSize; i < signal.length - windowSize; i++) {
        // 로컬 윈도우의 평균 계산
        let localSum = 0;
        for (let j = -windowSize; j <= windowSize; j++) {
            localSum += signal[i + j];
        }
        const localMean = localSum / (2 * windowSize + 1);

        // 동적 임계값 적용
        const threshold = localMean * multiplier;

        // 피크 감지
        if (signal[i] > threshold &&
            signal[i] > signal[i - 1] &&
            signal[i] > signal[i + 1]) {
            peaks.push({
                index: i,
                value: signal[i],
                threshold: threshold
            });
        }
    }

    return peaks;
}
```

**장점**
- 조용한 구간에서도 약한 비트 감지 가능
- 시끄러운 구간에서 과도한 감지 방지
- 다이나믹 레인지가 큰 곡에 효과적

---

## 패턴 디자인 원칙

### 1. 레인 매핑 전략

**5-Key 레이아웃 (DJMAX/EZ2DJ 스타일)**

```
D    F    Space    J    K
│    │       │      │    │
└────┴───────┴──────┴────┘
 왼손   가운데    오른손
```

**음악 요소별 레인 할당**

| 악기/음 | 추천 레인 | 이유 |
|---------|----------|------|
| 킥 드럼 | 0-2 (왼손) | 저음, 강한 임팩트 → 왼손 |
| 베이스 | 0-2 | 킥과 같은 저음역 |
| 스네어 | 1-3 (중앙) | 중음, 양손 모두 가능 |
| 클랩 | 2-4 (중앙-오른손) | 스네어와 유사 |
| 하이햇 (닫힘) | 3-4 (오른손) | 고음, 빠른 리듬 |
| 하이햇 (열림) | 4 (오른손) | 가장 밝은 고음 |
| 심벌즈 | 2-4 | 강조, 중앙에서 오른쪽 |
| 보컬 | 2 (스페이스) | 가장 중요한 중앙 레인 |
| 멜로디 | 1-3 | 음정에 따라 좌우 배치 |

### 2. 패턴 타입

**A. 단타 (Single Notes)**

가장 기본적인 노트:

```
시간축 →
레인0: ─○───────○──
레인1: ───○───────○
레인2: ─────○───────
레인3: ───────○─────
레인4: ─────────○───
```

**사용 시기**: 멜로디 라인, 보컬, 개별 악기 음

**B. 코드 (Chords)**

동시에 눌러야 하는 2개 이상의 노트:

```
레인0: ─○─────────○─
레인1: ─○─────────○─  ← 2-chord
레인2: ───────────────
레인3: ─────○─────○─
레인4: ─────○─────○─  ← 2-chord
```

**사용 시기**:
- 강한 악센트
- 여러 악기의 동시 발음
- 코드 진행
- 클라이맥스

**코드 설계 가이드**
```javascript
// 강도에 따른 코드 크기
const chordSize = {
    subtle:     1,           // 단타
    normal:     2,           // 약한 악센트
    accent:     2-3,         // 중간 악센트
    strong:     3-4,         // 강한 악센트
    climax:     4-5          // 클라이맥스
};
```

**C. 스트림 (Streams)**

빠르게 연속되는 노트:

```
레인0: ○─○─○─○─○─○─
레인1: ─○─○─○─○─○─○
레인2: ○─○─○─○─○─○─  ← 1/8 또는 1/16 스트림
레인3: ─○─○─○─○─○─○
레인4: ○─○─○─○─○─○─
```

**스트림 변형**

1. **Jumpstream**: 2-chord가 섞인 스트림
```
○ ─ ○ ○ ─ ○ ○ ─
─ ○ ○ ─ ○ ─ ─ ○
```

2. **Handstream**: 3-chord가 섞인 스트림
```
○ ○ ○ ─ ○ ○ ○
○ ─ ○ ○ ○ ─ ○
○ ○ ─ ○ ─ ○ ○
```

3. **Chordstream**: 다양한 크기의 코드 스트림
```
○ ○ ○ ○ ○ ─ ○
○ ─ ○ ○ ─ ○ ○
○ ○ ─ ○ ○ ○ ─
```

**D. 롱노트 (Long Notes / Hold Notes)**

누르고 있어야 하는 노트:

```
레인0: ─╥═══╨─────
레인1: ─────○─○─○─
레인2: ───╥═════╨──
레인3: ─────────○──
레인4: ──────────○─
```

**사용 시기**:
- 지속음 (신스 패드, 현악기)
- 긴 보컬
- 베이스 라인
- 타악기 여운

**롱노트 디자인 규칙**
```
1. 최소 길이: 250ms (읽기 가능)
2. 최대 길이: 악기 실제 길이에 맞춤
3. 다른 노트와 겹칠 때: 플레이 가능성 고려
4. 릴리즈 타이밍: 실제 음 끝과 일치
```

**E. 잭 (Jacks)**

같은 레인의 연속 노트:

```
레인0: ─────────────
레인1: ─────────────
레인2: ○○○○○○○─────  ← Jack (같은 손가락 연타)
레인3: ─────────────
레인4: ─────────────
```

**사용 주의**:
- 물리적으로 피로함
- 초보자에게 어려움
- 특정 패턴 강조에만 사용
- 4개 이상 연속은 피하기 (고급 차트 제외)

**F. 트릴 (Trills)**

두 레인을 빠르게 교대:

```
레인1: ○─○─○─○─○─○─
레인2: ─○─○─○─○─○─○  ← 1/8 트릴
```

**사용 시기**: 롤링 스네어, 트레몰로, 빠른 스케일

### 3. 손 배치 고려사항

**자연스러운 손 움직임**

```javascript
// 나쁜 패턴: 손이 계속 교차
시간 0.0: 레인 4 (오른손)
시간 0.1: 레인 0 (왼손으로 가야 하는데 너무 빠름)
시간 0.2: 레인 4 (오른손)

// 좋은 패턴: 손이 자연스럽게 움직임
시간 0.0: 레인 0 (왼손)
시간 0.1: 레인 1 (왼손)
시간 0.2: 레인 2 (왼손 또는 오른손)
시간 0.3: 레인 3 (오른손)
시간 0.4: 레인 4 (오른손)
```

**BMS/IIDX 7Key 손 배치 참고**

```
1 2 3 4 5 6 7 (SC)
└─왼손─┘ └─오른손─┘
```

프로 플레이어 스타일:
- **1048 스타일**: 1,2,3,4 왼손 / 5,6,7 오른손
- **1548 스타일**: 1,2,3 왼손 / 5,6,7 오른손, 4는 양손

### 4. 밀도 관리 (Density Management)

**NPS (Notes Per Second) 기준**

| 난이도 | NPS | 설명 |
|--------|-----|------|
| Beginner | 1-2 | 박자당 1개 정도 |
| Easy | 2-4 | 1/2 박자 간격 |
| Normal | 4-6 | 1/4 박자 + 가끔 1/8 |
| Hard | 6-8 | 지속적인 1/4, 짧은 1/8 스트림 |
| Expert | 8-12 | 빈번한 1/8 스트림 |
| Master | 12+ | 1/16 스트림, 복잡한 패턴 |

**밀도 계산 예제**

```javascript
function calculateNPS(notes, startTime, endTime) {
    const notesInRange = notes.filter(n =>
        n.time >= startTime && n.time < endTime
    );
    return notesInRange.length / (endTime - startTime);
}

// 8초 구간의 평균 NPS
const avgNPS = calculateNPS(notes, 10, 18);
console.log(`Average NPS: ${avgNPS.toFixed(2)}`);

// 피크 NPS 찾기 (1초 윈도우)
let peakNPS = 0;
for (let t = 0; t < duration; t += 0.1) {
    const nps = calculateNPS(notes, t, t + 1);
    peakNPS = Math.max(peakNPS, nps);
}
```

**밀도 곡선 설계**

```
NPS ↑
 12 │              ╱╲                    ╱╲
 10 │         ╱───╯  ╲              ╱───╯  ╲
  8 │        ╱         ╲            ╱        ╲___
  6 │   ╱───╯           ╲      ╱───╯             ╲
  4 │  ╱                 ╲    ╱                    ╲
  2 │ ╱                   ╲──╯                      ╲
  0 └─────────────────────────────────────────────────→ Time
    Intro  Verse  Chorus  Verse  Bridge  Final   Outro
```

### 5. 가독성 (Readability)

**시각적 명확성**

```javascript
// 최소 간격 권장사항
const readabilityGuidelines = {
    minNoteSpacing: 100,      // ms, 같은 레인
    minChordSpacing: 150,     // ms, 코드 간
    minJackSpacing: 120,      // ms, 잭 내부
    minStreamNoteSpacing: 80, // ms, 스트림 내부
    minLNGap: 200             // ms, 롱노트 사이
};

// 판정선 도달 시간 (Approach Rate)
const approachTime = {
    beginner: 1500,  // ms
    normal: 1000,
    hard: 800,
    expert: 600
};
```

**시각적 혼란 방지**

```
나쁜 예 - 읽기 어려움:
○ ─ ○ ○ ─ ○ ○ ─ ○ ○
○ ○ ─ ○ ○ ─ ○ ○ ─ ○
─ ○ ○ ─ ○ ○ ─ ○ ○ ─
○ ─ ○ ○ ─ ○ ○ ─ ○ ○
○ ○ ─ ○ ○ ─ ○ ○ ─ ○

좋은 예 - 읽기 쉬움:
○ ─ ─ ─ ─ ○ ─ ─ ─ ─
─ ○ ─ ─ ─ ─ ○ ─ ─ ─
─ ─ ○ ─ ─ ─ ─ ○ ─ ─
─ ─ ─ ○ ─ ─ ─ ─ ○ ─
─ ─ ─ ─ ○ ─ ─ ─ ─ ○
```

---

## 난이도 설계

### 1. 난이도 곡선

**점진적 난이도 상승**

```
Difficulty ↑
  10 │                                    ████
   9 │                              ██████
   8 │                         █████
   7 │                   ██████
   6 │              █████
   5 │        ██████
   4 │   █████
   3 │ ██
   2 │█
   1 │
   0 └────────────────────────────────────────→
     0%   20%   40%   60%   80%   100%
                Song Progress
```

**난이도 스파이크 관리**

```javascript
// 난이도 스파이크 감지
function detectDifficultySpikes(notes, windowSize = 2) {
    const densities = [];

    for (let t = 0; t < maxTime; t += 0.5) {
        const nps = calculateNPS(notes, t, t + windowSize);
        densities.push({ time: t, nps });
    }

    // 평균의 2배 이상이면 스파이크
    const avgNPS = densities.reduce((sum, d) => sum + d.nps, 0) / densities.length;
    const spikes = densities.filter(d => d.nps > avgNPS * 2);

    return spikes;
}
```

**스파이크 사용 시나리오**
- ✅ 클라이맥스에서 극적 효과
- ✅ 음악에 실제로 난이도 변화가 있을 때
- ❌ 초반 10초 이내
- ❌ 플레이어가 준비되지 않은 상태

### 2. 난이도별 특성

**Beginner (입문)**

```javascript
const beginnerCharacteristics = {
    nps: '1-2',
    maxCombo: 8,
    patterns: ['단타만 사용'],
    snaps: ['1/1', '1/2'],
    features: [
        '노트 간격 넉넉',
        '같은 손 연속 사용 최소화',
        '롱노트 없음 또는 매우 간단',
        '시각적으로 명확'
    ],
    avoid: [
        '코드',
        '잭',
        '스트림',
        '복잡한 패턴'
    ]
};
```

예시 패턴:
```
BPM 120, 1/2 박자
○ ─ ─ ─ ○ ─ ─ ─ ○ ─ ─ ─ ○ ─ ─ ─
─ ─ ○ ─ ─ ─ ○ ─ ─ ─ ○ ─ ─ ─ ○ ─
```

**Normal (초급)**

```javascript
const normalCharacteristics = {
    nps: '2-4',
    maxCombo: 12,
    patterns: ['단타 위주', '간단한 2-chord'],
    snaps: ['1/2', '1/4'],
    features: [
        '킥-스네어 기본 패턴',
        '2-chord 사용 (강조용)',
        '짧은 롱노트 (500ms 이상)',
        '예측 가능한 패턴'
    ],
    avoid: [
        '3개 이상 코드',
        '잭',
        '빠른 스트림',
        '복잡한 리듬'
    ]
};
```

**Hard (중급)**

```javascript
const hardCharacteristics = {
    nps: '4-6',
    maxCombo: 16,
    patterns: ['1/4 리듬', '2-3 코드', '짧은 1/8 스트림'],
    snaps: ['1/4', '1/8 (짧게)'],
    features: [
        '드럼 레이어 완전 표현',
        '멜로디 레이어 추가',
        '다양한 코드 크기',
        '짧은 스트림 (4-8노트)',
        '롱노트 + 단타 조합'
    ],
    avoid: [
        '지속적인 1/8 스트림',
        '4개 이상 잭',
        '읽기 어려운 패턴'
    ]
};
```

**Expert (고급)**

```javascript
const expertCharacteristics = {
    nps: '6-10',
    patterns: ['지속적인 1/8', 'jumpstream', 'handstream'],
    snaps: ['1/8', '1/16 (짧게)'],
    features: [
        '모든 레이어 표현',
        '복잡한 코드 진행',
        '긴 스트림 (16+ 노트)',
        '트릴과 잭 사용',
        '롱노트 동시 다중',
        '손 교차 패턴'
    ]
};
```

**Master (최상급)**

```javascript
const masterCharacteristics = {
    nps: '10+',
    patterns: ['chordstream', '1/16 stream', 'complex jacks'],
    snaps: ['모든 분할 사용'],
    features: [
        '극한의 물리적 난이도',
        '복잡한 리듬 구조',
        '빠른 손 이동',
        '읽기 난이도 고려',
        '체력 소모 관리'
    ]
};
```

### 3. 난이도 밸런싱

**다중 난이도 제작 시 고려사항**

```javascript
// 난이도 간 노트 수 비율
const noteDensityRatio = {
    'Beginner -> Normal': 1.5,
    'Normal -> Hard': 1.3,
    'Hard -> Expert': 1.2,
    'Expert -> Master': 1.1
};

// 예: Easy에 100개 노트가 있다면
// Normal: 150개
// Hard: 195개
// Expert: 234개
// Master: 257개
```

**난이도별 핵심 차이**

| 요소 | Beginner | Normal | Hard | Expert | Master |
|------|----------|--------|------|--------|--------|
| 레이어 | 드럼만 | 드럼+베이스 | 드럼+멜로디 | 모든 레이어 | 모든 레이어+디테일 |
| 코드 | 없음 | 2-chord | 2-3 chord | 3-4 chord | 모든 크기 |
| 롱노트 | 없음/간단 | 단순 | 복합 | 복잡 | 극한 |
| 스트림 | 없음 | 없음 | 짧음 | 중간 | 긴 스트림 |
| 특수패턴 | 없음 | 없음 | 제한적 | 보통 | 자유롭게 |

---

## 매핑 스타일

### 1. 오스 (osu!mania) 스타일 분류

**A. Rice-based 스타일**

단타 중심의 매핑:

```javascript
const riceStyles = {
    'Jumpstream': {
        description: '2-chord가 섞인 스트림',
        difficulty: 'Hard~Expert',
        example: `
        ○ ─ ○ ○ ─ ○ ○ ─
        ─ ○ ○ ─ ○ ─ ─ ○
        `
    },
    'Handstream': {
        description: '3-chord가 섞인 스트림',
        difficulty: 'Expert~Master',
        example: `
        ○ ○ ○ ─ ○ ○ ○
        ○ ─ ○ ○ ○ ─ ○
        ○ ○ ─ ○ ─ ○ ○
        `
    },
    'Chordstream': {
        description: '다양한 크기의 코드 스트림',
        difficulty: 'Master',
        example: `
        ○ ○ ○ ○ ○ ─ ○
        ○ ─ ○ ○ ─ ○ ○
        ○ ○ ─ ○ ○ ○ ─
        ─ ○ ○ ─ ○ ○ ○
        `
    },
    'Chordjack': {
        description: '같은 레인에 코드가 연속',
        difficulty: 'Expert+',
        stamina: 'Very High'
    }
};
```

**B. LN-based 스타일**

롱노트 중심의 매핑:

```javascript
const lnStyles = {
    'LN Coordination': {
        description: '여러 롱노트를 동시에 누르면서 다른 노트 처리',
        example: `
        ╥═══════════╨ ─ ─ ─
        ─ ○ ─ ○ ─ ○ ─ ○ ─
        ─ ─ ╥═════╨ ─ ─ ─
        `
    },
    'LN Release': {
        description: '롱노트 끝나는 타이밍이 중요',
        focus: '릴리즈 정확도'
    },
    'LN Density': {
        description: '롱노트 스트림',
        example: `
        ╥═╨╥═╨╥═╨╥═╨
        ╥═╨╥═╨╥═╨╥═╨
        ╥═╨╥═╨╥═╨╥═╨
        `
    },
    'Hybrid LN': {
        description: '롱노트와 단타의 균형잡힌 믹스'
    }
};
```

**C. 비주얼 스타일**

```javascript
const visualStyles = {
    'Clean': {
        description: '시각적으로 깔끔하고 정돈됨',
        features: ['균등한 간격', '오버랩 최소화', '대칭적 배치']
    },
    'Geometric': {
        description: '기하학적 형태 사용',
        features: ['지그재그', '사선', '파도 패턴']
    },
    'Symmetrical': {
        description: '좌우 대칭',
        features: ['미러링', '중심축 기준 대칭']
    },
    'Messy': {
        description: '의도적으로 복잡하고 혼란스러움',
        features: ['많은 오버랩', '불규칙한 간격'],
        difficulty: 'High reading difficulty'
    }
};
```

### 2. DJMAX 스타일

```javascript
const djmaxStyle = {
    characteristics: [
        '보컬 중심 매핑',
        '멜로디 라인 강조',
        '세련된 패턴 디자인',
        '음악성 우선'
    ],
    techniques: {
        'Melody Mapping': '보컬/멜로디를 정확히 따라가기',
        'Build-up': '점진적 강도 증가',
        'Call and Response': '패턴 간 대화하듯 배치',
        'Accent Chords': '강조 부분에 코드 사용'
    }
};
```

### 3. BMS/IIDX 스타일

```javascript
const bmsStyle = {
    characteristics: [
        '드럼 레이어 정밀 표현',
        '키음(Keysound) 사용',
        '높은 기술적 난이도',
        '복잡한 리듬'
    ],
    patterns: {
        'Scratch': '스크래치 레인 (7번 또는 1번)',
        'Dense Chords': '조밀한 코드 패턴',
        'Technical Jacks': '잭을 기술적 요소로 사용',
        'Trill Sections': '긴 트릴 구간'
    }
};
```

### 4. 커스텀 스타일 개발

자신만의 스타일을 만들 때:

```javascript
function developMappingStyle(influences, goals) {
    return {
        // 1. 영향받은 스타일들
        influences: influences,

        // 2. 목표하는 플레이 경험
        targetExperience: goals.experience,

        // 3. 특징적 패턴
        signaturePatterns: goals.patterns,

        // 4. 우선순위
        priorities: {
            musicality: goals.musicality,
            playability: goals.playability,
            difficulty: goals.difficulty,
            creativity: goals.creativity
        }
    };
}

// 예시
const myStyle = developMappingStyle(
    ['DJMAX', 'osu!mania'],
    {
        experience: 'Melodic and satisfying',
        patterns: ['Flowing streams', 'Accent chords'],
        musicality: 9,
        playability: 8,
        difficulty: 7,
        creativity: 8
    }
);
```

---

## 품질 보증

### 1. 테스트 플레이

**필수 테스트 항목**

```javascript
const testChecklist = {
    playability: [
        '[ ] 모든 노트가 정확한 타이밍에 배치되었는가?',
        '[ ] 손 이동이 자연스러운가?',
        '[ ] 불가능한 패턴은 없는가?',
        '[ ] 체력 소모가 적절한가?'
    ],
    musicality: [
        '[ ] 음악의 중요한 요소들이 표현되었는가?',
        '[ ] 강약이 잘 표현되었는가?',
        '[ ] 구간별 분위기가 맞는가?'
    ],
    readability: [
        '[ ] 노트를 읽기 쉬운가?',
        '[ ] 갑작스러운 난이도 변화는 없는가?',
        '[ ] 시각적으로 혼란스럽지 않은가?'
    ],
    technical: [
        '[ ] 타이밍이 정확한가? (±5ms)',
        '[ ] 오디오 싱크가 맞는가?',
        '[ ] BPM 설정이 정확한가?',
        '[ ] 파일이 올바르게 저장되는가?'
    ]
};
```

**테스트 난이도**

```
1차: 작성자 본인
2차: 동일 레벨 플레이어
3차: 한 단계 낮은 레벨 플레이어
4차: 한 단계 높은 레벨 플레이어
```

### 2. 일반적인 실수

**타이밍 관련**

```javascript
const timingMistakes = {
    'Off-sync': {
        problem: '노트가 음악과 맞지 않음',
        solution: '오디오 오프셋 조정, BPM 재확인'
    },
    'Wrong Snap': {
        problem: '잘못된 박자 분할 사용',
        solution: '음악을 천천히 들으며 정확한 리듬 파악',
        example: '3연음을 1/4로 표현 (X) → 1/3 사용 (O)'
    },
    'Inconsistent Timing': {
        problem: '비슷한 소리를 다르게 타이밍',
        solution: '일관성 유지, 같은 악기는 같은 방식으로'
    }
};
```

**패턴 관련**

```javascript
const patternMistakes = {
    'Overmapping': {
        problem: '없는 소리에 노트 배치',
        solution: '음악에 실제로 있는 소리만 매핑',
        severity: 'Critical'
    },
    'Undermapping': {
        problem: '중요한 소리를 빠뜨림',
        solution: '모든 레이어를 주의깊게 청취',
        severity: 'Major'
    },
    'Inconsistent Layering': {
        problem: '같은 악기를 때때로만 표현',
        solution: '레이어 선택 후 일관되게 적용',
        example: '킥을 때로는 표현하고 때로는 안 함'
    },
    'Uncomfortable Patterns': {
        problem: '물리적으로 치기 불편한 패턴',
        solution: '실제로 플레이해보고 조정',
        examples: [
            '빠른 손 교차',
            '부자연스러운 손가락 배치',
            '무리한 스트레칭'
        ]
    }
};
```

**난이도 관련**

```javascript
const difficultyMistakes = {
    'Difficulty Spikes': {
        problem: '갑작스러운 난이도 급등',
        solution: '점진적 증가, 음악적 정당성 확보'
    },
    'Inconsistent Difficulty': {
        problem: '난이도가 들쭉날쭉',
        solution: '전체 차트의 난이도 곡선 확인'
    },
    'Wrong Difficulty Label': {
        problem: '난이도 표시가 실제와 다름',
        solution: 'NPS, 패턴 복잡도 재계산'
    }
};
```

### 3. 피드백 수집

**효과적인 피드백 질문**

```javascript
const feedbackQuestions = [
    // 전반적 인상
    "차트가 음악을 잘 표현했나요?",
    "플레이하며 즐거웠나요?",
    "난이도가 적절했나요?",

    // 구체적 문제
    "불편한 패턴이 있었나요? (시간 지점 명시)",
    "타이밍이 안 맞는 부분이 있었나요?",
    "읽기 어려운 구간이 있었나요?",

    // 개선 제안
    "어떤 점을 개선하면 좋을까요?",
    "다른 비슷한 차트와 비교하면 어떤가요?"
];
```

### 4. 반복 개선

```javascript
function iterativeImprovement(chart, feedback) {
    let version = 1;

    while (hasIssues(feedback)) {
        console.log(`=== Version ${version} ===`);

        // 1. 주요 문제 식별
        const criticalIssues = feedback.filter(f => f.severity === 'critical');

        // 2. 수정
        criticalIssues.forEach(issue => {
            chart = fixIssue(chart, issue);
        });

        // 3. 재테스트
        feedback = testChart(chart);

        // 4. 다음 버전
        version++;

        if (version > 10) {
            console.log('Too many iterations, consider major redesign');
            break;
        }
    }

    return chart;
}
```

---

## 실전 워크플로우

### 1. 사전 준비

**음원 분석**

```javascript
async function analyzeSong(audioFile) {
    // 1. 기본 정보
    const basicInfo = {
        duration: await getAudioDuration(audioFile),
        sampleRate: 44100,
        channels: 2
    };

    // 2. BPM 추정
    const bpm = await estimateBPM(audioFile);
    console.log(`Estimated BPM: ${bpm}`);

    // 3. 구조 분석
    const structure = analyzeStructure(audioFile);
    console.log('Song Structure:', structure);
    // { intro: [0, 8], verse1: [8, 24], chorus: [24, 40], ... }

    // 4. 비트 감지
    const beats = await detectBeats(audioFile);
    console.log(`Detected ${beats.length} beats`);

    // 5. 주파수 분석
    const spectrum = await analyzeSpectrum(audioFile);
    console.log('Dominant Frequencies:', spectrum.peaks);

    return {
        basicInfo,
        bpm,
        structure,
        beats,
        spectrum
    };
}
```

**목표 설정**

```javascript
const chartGoals = {
    targetAudience: 'Intermediate players',
    difficulty: 'Hard (NPS 6-8)',
    style: 'Melodic with drum emphasis',
    specialFeatures: [
        'Vocal mapping in chorus',
        'Build-up sections',
        'Climax at final chorus'
    ],
    constraints: [
        'No LN (for beginners)',
        'Limit jacks to 3 consecutive',
        'Maximum 3-chord'
    ]
};
```

### 2. 초안 작성

**Step 1: 타이밍 설정**

```javascript
// 1. 오디오 로드
loadAudio('song.mp3');

// 2. 첫 박자 찾기 (수동)
// 여러 번 들으며 정확한 첫 비트 타이밍 측정
const firstBeatTime = 0.234; // 초

// 3. BPM 확정
const confirmedBPM = 128;

// 4. 비트 그리드 생성
function generateBeatGrid(firstBeat, bpm, duration) {
    const beats = [];
    const interval = 60 / bpm;

    for (let time = firstBeat; time < duration; time += interval) {
        beats.push(time);
    }

    return beats;
}

const beatGrid = generateBeatGrid(firstBeatTime, confirmedBPM, audioDuration);
```

**Step 2: 기본 레이어 (킥+스네어)**

```javascript
function mapBasicDrums(beatGrid) {
    const notes = [];

    beatGrid.forEach((time, index) => {
        // 4/4 박자 가정
        const beatInMeasure = index % 4;

        if (beatInMeasure === 0 || beatInMeasure === 2) {
            // 1, 3박: 킥드럼 → 왼쪽 레인
            notes.push({ time, lane: 0, type: 'kick' });
        }

        if (beatInMeasure === 1 || beatInMeasure === 3) {
            // 2, 4박: 스네어 → 중앙 레인
            notes.push({ time, lane: 2, type: 'snare' });
        }
    });

    return notes;
}
```

**Step 3: 하이햇 추가**

```javascript
function addHihats(notes, beatGrid, style = '1/4') {
    beatGrid.forEach((time, index) => {
        let hihatTimes = [];

        if (style === '1/4') {
            // 각 1/4박마다
            hihatTimes = [time, time + 0.125, time + 0.25, time + 0.375];
        } else if (style === '1/8') {
            // 각 1/8박마다 (더 빠름)
            for (let i = 0; i < 8; i++) {
                hihatTimes.push(time + i * 0.0625);
            }
        }

        hihatTimes.forEach(t => {
            // 하이햇 → 오른쪽 레인
            notes.push({ time: t, lane: 4, type: 'hihat' });
        });
    });

    return notes;
}
```

**Step 4: 멜로디/보컬 추가**

```javascript
function addMelody(notes, melody, structure) {
    // 코러스에서만 멜로디 매핑
    const chorusSections = structure.filter(s => s.type === 'chorus');

    chorusSections.forEach(section => {
        const melodyNotes = melody.filter(n =>
            n.time >= section.start && n.time < section.end
        );

        melodyNotes.forEach(melodyNote => {
            // 음정에 따라 레인 매핑
            const lane = mapPitchToLane(melodyNote.pitch);
            notes.push({
                time: melodyNote.time,
                lane: lane,
                type: 'melody'
            });
        });
    });

    return notes;
}

function mapPitchToLane(pitch) {
    // 낮은 음 → 왼쪽, 높은 음 → 오른쪽
    if (pitch < 60) return 0;       // C4 미만
    if (pitch < 65) return 1;       // F4 미만
    if (pitch < 70) return 2;       // A4 미만
    if (pitch < 75) return 3;       // D5 미만
    return 4;                        // D5 이상
}
```

**Step 5: 악센트와 코드**

```javascript
function addAccents(notes, beats, intensity) {
    beats.forEach(beat => {
        if (beat.intensity > 0.8) {
            // 강한 비트 → 코드 추가
            const existingNotes = notes.filter(n =>
                Math.abs(n.time - beat.time) < 0.01
            );

            if (existingNotes.length === 1) {
                // 단타를 코드로 변경
                const lane1 = existingNotes[0].lane;
                const lane2 = getComplementaryLane(lane1);

                notes.push({
                    time: beat.time,
                    lane: lane2,
                    type: 'accent'
                });
            }
        }
    });

    return notes;
}

function getComplementaryLane(lane) {
    // 보완적인 레인 선택 (손 배치 고려)
    const complements = {
        0: 1,  // 레인 0 → 1
        1: 0,  // 레인 1 → 0
        2: 3,  // 레인 2 → 3 (스페이스와 함께)
        3: 2,
        4: 3
    };
    return complements[lane];
}
```

### 3. 다듬기

**중복 제거**

```javascript
function removeDuplicates(notes) {
    const threshold = 0.05; // 50ms 이내는 중복으로 간주
    const filtered = [];

    // 시간순 정렬
    notes.sort((a, b) => a.time - b.time);

    notes.forEach(note => {
        const duplicate = filtered.find(f =>
            Math.abs(f.time - note.time) < threshold &&
            f.lane === note.lane
        );

        if (!duplicate) {
            filtered.push(note);
        }
    });

    return filtered;
}
```

**스무딩 (부드러운 흐름)**

```javascript
function smoothPatterns(notes) {
    for (let i = 1; i < notes.length - 1; i++) {
        const prev = notes[i - 1];
        const curr = notes[i];
        const next = notes[i + 1];

        // 지그재그 패턴 감지 및 수정
        // 예: 0 → 4 → 0 (X) → 0 → 2 → 4 (O)
        if (Math.abs(curr.lane - prev.lane) > 2 &&
            Math.abs(next.lane - curr.lane) > 2) {
            // 중간 레인으로 조정
            curr.lane = Math.round((prev.lane + next.lane) / 2);
        }
    }

    return notes;
}
```

**가독성 개선**

```javascript
function improveReadability(notes) {
    const minSpacing = 0.1; // 100ms

    for (let i = 1; i < notes.length; i++) {
        const prev = notes[i - 1];
        const curr = notes[i];

        // 같은 레인에서 너무 가까운 노트
        if (curr.lane === prev.lane &&
            curr.time - prev.time < minSpacing) {
            // 다른 레인으로 이동
            curr.lane = findNearbyEmptyLane(notes, i, curr.time);
        }
    }

    return notes;
}

function findNearbyEmptyLane(notes, currentIndex, time) {
    const currentLane = notes[currentIndex].lane;
    const radius = 1;

    for (let r = 1; r <= radius; r++) {
        const candidates = [currentLane - r, currentLane + r];

        for (const lane of candidates) {
            if (lane >= 0 && lane < 5) {
                const occupied = notes.some(n =>
                    n.lane === lane &&
                    Math.abs(n.time - time) < 0.05
                );

                if (!occupied) return lane;
            }
        }
    }

    return currentLane; // 찾지 못하면 원래 레인 유지
}
```

### 4. 테스트 및 반복

```javascript
async function testAndRefine(chart) {
    let iteration = 1;
    const maxIterations = 5;

    while (iteration <= maxIterations) {
        console.log(`\n=== Test Iteration ${iteration} ===`);

        // 1. 자동 검증
        const autoIssues = validateChart(chart);
        console.log(`Auto-detected issues: ${autoIssues.length}`);

        // 2. 플레이 테스트
        console.log('Play test...');
        const playIssues = await playTestChart(chart);

        // 3. 이슈가 없으면 완료
        if (autoIssues.length === 0 && playIssues.length === 0) {
            console.log('Chart is ready!');
            break;
        }

        // 4. 이슈 수정
        chart = fixIssues(chart, [...autoIssues, ...playIssues]);

        iteration++;
    }

    return chart;
}

function validateChart(chart) {
    const issues = [];

    // 타이밍 검증
    chart.notes.forEach((note, i) => {
        if (note.time < 0) {
            issues.push({ type: 'negative_time', index: i });
        }

        if (i > 0 && note.time < chart.notes[i-1].time) {
            issues.push({ type: 'wrong_order', index: i });
        }
    });

    // 밀도 검증
    const peakNPS = calculatePeakNPS(chart.notes);
    if (peakNPS > chart.targetNPS * 2) {
        issues.push({ type: 'excessive_density', value: peakNPS });
    }

    // 가독성 검증
    const readabilityScore = calculateReadability(chart.notes);
    if (readabilityScore < 0.6) {
        issues.push({ type: 'poor_readability', score: readabilityScore });
    }

    return issues;
}
```

---

## 고급 기법

### 1. 레이어 믹싱

여러 음악 레이어를 효과적으로 조합:

```javascript
function advancedLayering(audioData, difficulty) {
    const layers = {
        drums: extractDrumLayer(audioData),
        bass: extractBassLayer(audioData),
        melody: extractMelodyLayer(audioData),
        vocal: extractVocalLayer(audioData),
        fx: extractFXLayer(audioData)
    };

    let notes = [];

    if (difficulty === 'Easy') {
        // 드럼만
        notes = mapLayer(layers.drums);
    } else if (difficulty === 'Normal') {
        // 드럼 + 베이스
        notes = [...mapLayer(layers.drums), ...mapLayer(layers.bass)];
    } else if (difficulty === 'Hard') {
        // 드럼 + 멜로디
        notes = [...mapLayer(layers.drums), ...mapLayer(layers.melody)];
    } else if (difficulty === 'Expert') {
        // 모든 레이어
        for (const [name, layer] of Object.entries(layers)) {
            notes = [...notes, ...mapLayer(layer)];
        }
    }

    return deduplicateAndOptimize(notes);
}
```

### 2. 다이나믹 난이도 조정

구간별로 난이도를 세밀하게 조정:

```javascript
function dynamicDifficultyMapping(beats, structure, targetDifficulty) {
    const notes = [];
    const difficultyMap = {
        'intro': targetDifficulty * 0.6,
        'verse': targetDifficulty * 0.8,
        'pre-chorus': targetDifficulty * 0.9,
        'chorus': targetDifficulty * 1.0,
        'bridge': targetDifficulty * 0.7,
        'final-chorus': targetDifficulty * 1.2,
        'outro': targetDifficulty * 0.5
    };

    structure.forEach(section => {
        const sectionDifficulty = difficultyMap[section.type];
        const sectionBeats = beats.filter(b =>
            b.time >= section.start && b.time < section.end
        );

        // 난이도에 맞게 비트 선택
        const selectedBeats = selectBeats(sectionBeats, sectionDifficulty);

        // 노트 생성
        selectedBeats.forEach(beat => {
            notes.push(...generatePattern(beat, sectionDifficulty));
        });
    });

    return notes;
}

function selectBeats(beats, difficulty) {
    // 난이도가 높을수록 더 많은 비트 선택
    const ratio = Math.min(1.0, difficulty / 10);
    return beats.filter(() => Math.random() < ratio);
}
```

### 3. 폴리리듬 처리

여러 리듬이 동시에 진행되는 복잡한 음악:

```javascript
function mapPolyrhythm(audioData) {
    // 여러 리듬 레이어 감지
    const rhythm1 = detectRhythm(audioData, { division: '1/4' }); // 4비트
    const rhythm2 = detectRhythm(audioData, { division: '1/3' }); // 3비트

    const notes = [];

    // 각 리듬을 다른 손에 할당
    rhythm1.forEach(beat => {
        // 왼손 (레인 0-1)
        notes.push({ time: beat.time, lane: beat.intensity > 0.7 ? 0 : 1 });
    });

    rhythm2.forEach(beat => {
        // 오른손 (레인 3-4)
        notes.push({ time: beat.time, lane: beat.intensity > 0.7 ? 4 : 3 });
    });

    return notes;
}
```

### 4. SVT (Scroll Velocity) 효과

스크롤 속도 변화로 특수 효과 (고급 에디터에서):

```javascript
function addScrollVelocityEffects(chart, structure) {
    const svChanges = [];

    structure.forEach(section => {
        if (section.type === 'breakdown') {
            // 브레이크다운: 느린 스크롤
            svChanges.push({
                time: section.start,
                multiplier: 0.5
            });
            svChanges.push({
                time: section.end,
                multiplier: 1.0
            });
        } else if (section.type === 'buildup') {
            // 빌드업: 점진적 가속
            const steps = 10;
            for (let i = 0; i < steps; i++) {
                svChanges.push({
                    time: section.start + (section.end - section.start) * i / steps,
                    multiplier: 0.8 + 0.4 * i / steps
                });
            }
        }
    });

    chart.svChanges = svChanges;
    return chart;
}
```

### 5. 키사운드 (Keysound)

노트를 칠 때 소리가 나는 기법 (BMS 스타일):

```javascript
function addKeysounds(notes, audioSamples) {
    notes.forEach(note => {
        // 악기 타입에 따라 샘플 할당
        if (note.type === 'kick') {
            note.keysound = audioSamples.kick;
        } else if (note.type === 'snare') {
            note.keysound = audioSamples.snare;
        } else if (note.type === 'hihat') {
            note.keysound = audioSamples.hihat;
        } else if (note.type === 'melody') {
            // 멜로디는 음정에 맞는 샘플
            note.keysound = audioSamples.melody[note.pitch];
        }
    });

    return notes;
}
```

### 6. 머신러닝 활용

AI를 활용한 자동 매핑 보조:

```javascript
// TensorFlow.js 예시 (개념적)
async function aiAssistedMapping(audioFile) {
    // 1. 오디오 특징 추출
    const features = await extractAudioFeatures(audioFile);

    // 2. 사전 학습된 모델 로드
    const model = await tf.loadLayersModel('beatmap-model.json');

    // 3. 예측
    const predictions = model.predict(features);

    // 4. 예측 결과를 노트로 변환
    const notes = predictionsToNotes(predictions);

    // 5. 후처리 (사람의 개입)
    const refined = manuallyRefine(notes);

    return refined;
}

// 실제 구현은 복잡하지만, 가능한 접근 방법:
// - onset detection → RNN/CNN
// - genre classification → CNN
// - difficulty prediction → regression model
// - pattern generation → GAN/VAE
```

---

## 참고 자료

### 학술 논문

**Onset Detection**
- Bello, J. P., et al. (2005). "A tutorial on onset detection in music signals"
- Dixon, S. (2006). "Onset detection revisited"
- Böck, S., & Widmer, G. (2013). "Maximum filter vibrato suppression for onset detection"

**Beat Tracking**
- Ellis, D. P. (2007). "Beat tracking by dynamic programming"
- Böck, S., et al. (2016). "madmom: a new Python Audio and Music Signal Processing Library"
- Davies, M. E., & Plumbley, M. D. (2007). "Context-dependent beat tracking of musical audio"

**Tempo Estimation**
- Scheirer, E. D. (1998). "Tempo and beat analysis of acoustic musical signals"
- Grosche, P., & Müller, M. (2011). "Extracting predominant local pulse information from music recordings"

### 오픈소스 라이브러리

**Python**
```bash
# madmom - 음악 정보 검색
pip install madmom

# librosa - 오디오 분석
pip install librosa

# essentia - 음악 분석 툴킷
pip install essentia
```

**JavaScript**
```bash
# Meyda - 오디오 특징 추출
npm install meyda

# Tone.js - Web Audio 프레임워크
npm install tone

# peaks.js - 파형 시각화
npm install peaks.js
```

### 차트 제작 도구

| 도구 | 게임 | 특징 |
|------|------|------|
| osu! Editor | osu!mania | 강력한 내장 에디터 |
| BMSEdit | BMS/IIDX | 키사운드 지원 |
| ArrowVortex | StepMania | 다양한 키 설정 |
| Quaver Editor | Quaver | 모던 UI |
| Malody Editor | Malody | 멀티 모드 지원 |

### 커뮤니티 리소스

**포럼 & 위키**
- [osu! wiki - Beatmapping](https://osu.ppy.sh/wiki/en/Beatmapping)
- [Etterna Discord](https://discord.gg/etterna)
- [StepMania Community](https://www.stepmania.com/)

**튜토리얼 영상**
- YouTube: "osu!mania mapping tutorial"
- YouTube: "BMS charting guide"
- Twitch: 프로 차터들의 라이브 스트림

**차트 저장소**
- [osu! Beatmap Listing](https://osu.ppy.sh/beatmapsets)
- [BMS Search](https://www.bmssearch.net/)
- [Quaver Maps](https://quavergame.com/maps)

### 추천 도서

- **"The Computer Music Tutorial" by Curtis Roads**: 음악 신호 처리 기초
- **"Game Feel" by Steve Swink**: 게임 느낌과 타이밍의 중요성
- **"The Art of Game Design" by Jesse Schell**: 게임 디자인 원칙

---

## 결론

리듬게임 차트 제작은 기술적 지식, 음악적 감각, 그리고 플레이어에 대한 이해가 모두 필요한 복합적인 작업입니다.

**핵심 원칙 요약**

1. **음악을 먼저 이해하라**
   - 여러 번 들어라
   - 구조를 파악하라
   - 중요한 요소를 식별하라

2. **플레이어를 존중하라**
   - 플레이 가능성을 최우선으로
   - 공정한 난이도 설정
   - 명확한 피드백

3. **반복하고 개선하라**
   - 완벽한 첫 시도는 없다
   - 테스트와 피드백 수집
   - 지속적인 개선

4. **자신만의 스타일을 개발하라**
   - 다양한 차트 연구
   - 실험하기
   - 일관성 유지

**마지막 조언**

```
"완벽한 차트는 없다. 하지만 플레이어가 즐겁게 플레이하고,
 음악을 더 깊이 느낄 수 있다면, 그것이 좋은 차트다."
```

행운을 빕니다! 🎮🎵

---

**문서 버전**: 1.0
**작성일**: 2025-10-28
**작성자**: AI-Diver BookJam Team
**기반**: osu! wiki, madmom, 실무 경험
