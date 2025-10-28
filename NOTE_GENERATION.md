# 노트 생성 시스템 상세 문서

## 목차
1. [전체 프로세스 개요](#전체-프로세스-개요)
2. [BPM 자동 감지 알고리즘](#bpm-자동-감지-알고리즘)
3. [노트 생성 알고리즘](#노트-생성-알고리즘)
4. [난이도별 로직](#난이도별-로직)
5. [노트 객체 구조](#노트-객체-구조)
6. [최적화 및 성능](#최적화-및-성능)

---

## 전체 프로세스 개요

노트 생성은 다음 단계로 진행됩니다:

```
MP3 파일 로드
    ↓
Web Audio API로 디코딩
    ↓
BPM 감지 (또는 수동 입력)
    ↓
노트 패턴 생성
    ↓
시간순 정렬
    ↓
게임 시작
```

### 주요 함수
- `loadAudioFile()`: 파일 로드 및 전체 프로세스 조율
- `detectBPM()`: 자동 BPM 감지
- `generateNotes()`: 노트 패턴 생성

---

## BPM 자동 감지 알고리즘

### 개요
Web Audio API의 OfflineAudioContext를 사용하여 오디오 파일의 BPM을 자동으로 감지합니다.

### 알고리즘 단계

#### 1. OfflineAudioContext 생성
```javascript
const offlineContext = new OfflineAudioContext(1, buffer.length, buffer.sampleRate);
```
- **채널 수**: 1 (모노)
- **길이**: 원본 오디오 버퍼 길이
- **샘플레이트**: 원본과 동일 (일반적으로 44100Hz 또는 48000Hz)

#### 2. 오디오 필터링 체인 구성
```
BufferSource → LowpassFilter → Analyser → Destination
```

**Lowpass Filter (저역 통과 필터)**
- **주파수**: 150Hz
- **목적**: 킥드럼, 베이스 같은 저음역 비트만 추출
- **이유**: 리듬의 비트는 주로 저음역에 존재

**Analyser**
- **FFT Size**: 2048
- **목적**: 오디오 데이터 분석 (실제로는 사용 안 함, 호환성)

#### 3. 오디오 렌더링 및 피크 감지
```javascript
const renderedBuffer = await offlineContext.startRendering();
const data = renderedBuffer.getChannelData(0);
```

**피크 감지 파라미터**
- **Threshold**: 0.9 (진폭의 90% 이상만 피크로 인식)
- **Min Distance**: sampleRate × 0.2 = 약 8820 샘플 (44.1kHz 기준)
  - 시간으로 환산: 0.2초 = 200ms
  - 의미: 200ms 이내의 피크는 같은 비트로 간주

**피크 감지 로직**
```javascript
for (let i = 0; i < data.length; i++) {
    if (Math.abs(data[i]) > threshold) {
        if (peaks.length === 0 || i - peaks[peaks.length - 1] > minDistance) {
            peaks.push(i);
        }
    }
}
```

#### 4. BPM 계산

**평균 간격 계산**
```javascript
let totalInterval = 0;
for (let i = 1; i < peaks.length; i++) {
    totalInterval += peaks[i] - peaks[i - 1];
}
const avgInterval = totalInterval / (peaks.length - 1);
```

**BPM 변환 공식**
```
BPM = 60 / (avgInterval / sampleRate)
```

**예시 계산**
- 샘플레이트: 44100 Hz
- 평균 간격: 22050 샘플
- 초로 환산: 22050 / 44100 = 0.5초
- BPM: 60 / 0.5 = **120 BPM**

**BPM 범위 제한**
```javascript
return Math.max(60, Math.min(240, bpm));
```
- **최소**: 60 BPM (느린 발라드)
- **최대**: 240 BPM (초고속 전자음악)

### BPM 감지 한계점

#### 장점
- 사용자 입력 없이 자동으로 BPM 추정
- 실시간 처리 불필요 (OfflineContext 사용)

#### 한계
- **단순한 알고리즘**: 복잡한 리듬 패턴 감지 어려움
- **템포 변화**: 곡 중간에 BPM이 바뀌는 경우 평균값만 반환
- **Threshold 의존**: 0.9라는 고정값이 모든 음악에 적합하지 않음
- **오차 가능성**: ±5-10 BPM 정도의 오차 발생 가능

#### 개선 방안
사용자가 직접 BPM을 입력할 수 있도록 UI 제공:
```html
<input type="number" id="bpm-input" placeholder="BPM (자동 감지)" min="60" max="240">
```

---

## 노트 생성 알고리즘

### 기본 원리
BPM을 기반으로 비트 간격을 계산하고, 각 비트마다 노트를 생성합니다.

### 1. 비트 간격 계산

```javascript
const beatInterval = 60 / gameState.bpm;
```

**예시**
- BPM 120: `60 / 120 = 0.5초` (500ms)
- BPM 140: `60 / 140 = 0.428초` (428ms)
- BPM 180: `60 / 180 = 0.333초` (333ms)

### 2. 타임라인 순회

```javascript
for (let time = 1; time < duration; time += beatInterval) {
    // 노트 생성
}
```

- **시작 시간**: 1초 (인트로 여유 제공)
- **종료 시간**: 오디오 파일 전체 길이
- **증가량**: beatInterval (한 비트씩)

**예시 타임라인 (BPM 120, 10초 곡)**
```
시간:   1.0s  1.5s  2.0s  2.5s  3.0s  3.5s  ...  9.5s  10.0s
비트:   1     2     3     4     5     6     ...   18    19
```

### 3. 난이도별 노트 수 결정

```javascript
const numNotes = Math.random() < density ? (Math.random() < 0.3 ? 2 : 1) : 1;
```

#### 로직 분해

**Step 1: 난이도 확률 체크**
```
Math.random() < density
```
- Easy (0.5): 50% 확률로 노트 생성
- Normal (1.0): 100% 확률로 노트 생성
- Hard (1.5): 100% 확률로 노트 생성 (1.0 초과는 항상 true)

**Step 2: 멀티 노트 확률**
```
Math.random() < 0.3 ? 2 : 1
```
- 30% 확률로 2개 노트 (동시 치기)
- 70% 확률로 1개 노트

**확률 표**

| 난이도 | 노트 없음 | 1개 노트 | 2개 노트 |
|--------|-----------|----------|----------|
| Easy   | 50%       | 35%      | 15%      |
| Normal | 0%        | 70%      | 30%      |
| Hard   | 0%        | 70%      | 30%      |

### 4. 레인 선택 알고리즘

```javascript
const selectedLanes = [];

for (let i = 0; i < numNotes; i++) {
    let lane;
    do {
        lane = Math.floor(Math.random() * LANES.length);
    } while (selectedLanes.includes(lane));
    selectedLanes.push(lane);

    gameState.notes.push({
        time: time,
        lane: lane,
        hit: false,
        missed: false
    });
}
```

#### 중복 방지 로직
- **do-while 루프**: 이미 선택된 레인이 나올 때까지 반복
- **selectedLanes 배열**: 같은 타이밍에 선택된 레인 추적
- **결과**: 동시에 같은 레인에 2개 노트가 생성되지 않음

**예시**
```
비트 1 (2개 노트):
  랜덤 → 3번 레인 선택 → selectedLanes = [3]
  랜덤 → 3번 레인 (중복!) → 다시 랜덤
  랜덤 → 5번 레인 선택 → selectedLanes = [3, 5]
```

### 5. Hard 난이도 전용: 8분 노트 추가

```javascript
if (gameState.difficulty === 'hard' && Math.random() < 0.3) {
    const lane = Math.floor(Math.random() * LANES.length);
    gameState.notes.push({
        time: time + beatInterval / 2,
        lane: lane,
        hit: false,
        missed: false
    });
}
```

#### 8분 노트란?
- **4분 노트**: 정박 (beatInterval)
- **8분 노트**: 정박 사이 (beatInterval / 2)

**타임라인 비교**
```
Normal (4분 노트만):
시간:  1.0    1.5    2.0    2.5    3.0
노트:  ●      ●      ●      ●      ●

Hard (8분 노트 추가):
시간:  1.0  1.25  1.5  1.75  2.0  2.25  2.5
노트:  ●          ●    ●     ●          ●
           ↑ 8분 노트 (30% 확률)
```

#### Hard 난이도 특징
- 기본 4분 노트 (100% 생성)
- 동시치기 30% 확률
- 8분 노트 30% 추가 확률
- **평균 노트 밀도**: Normal의 약 1.6배

### 6. 노트 정렬

```javascript
gameState.notes.sort((a, b) => a.time - b.time);
```

- **정렬 기준**: 시간 (time) 오름차순
- **이유**: 게임 루프에서 순차적으로 처리하기 위함
- **복잡도**: O(n log n)

---

## 난이도별 로직

### Easy
```javascript
density: 0.5
```

**특징**
- 노트 생성 확률 50%
- 비트마다 노트가 없을 수 있음 (여유로운 플레이)
- 8분 노트 없음
- 동시치기 15% 확률

**예상 노트 수** (BPM 120, 3분 곡)
- 총 비트 수: (180초 - 1초) / 0.5초 = 358 비트
- 예상 노트: 358 × 0.5 × 1.15 ≈ **206개**

### Normal
```javascript
density: 1.0
```

**특징**
- 모든 비트마다 노트 생성
- 8분 노트 없음
- 동시치기 30% 확률

**예상 노트 수** (BPM 120, 3분 곡)
- 총 비트 수: 358 비트
- 예상 노트: 358 × 1.0 × 1.3 ≈ **465개**

### Hard
```javascript
density: 1.5 (실제로는 1.0과 동일하게 100% 생성)
```

**특징**
- 모든 비트마다 노트 생성
- **8분 노트 30% 추가**
- 동시치기 30% 확률

**예상 노트 수** (BPM 120, 3분 곡)
- 기본 노트: 358 × 1.3 ≈ 465개
- 8분 노트: 358 × 0.3 ≈ 107개
- **총합: 약 572개**

### 난이도별 비교표

| 항목 | Easy | Normal | Hard |
|------|------|--------|------|
| 비트당 생성 확률 | 50% | 100% | 100% |
| 동시치기 확률 | 15% | 30% | 30% |
| 8분 노트 | ❌ | ❌ | ✅ 30% |
| 노트 밀도 (3분, BPM 120) | ~206개 | ~465개 | ~572개 |
| 상대 난이도 | 1.0x | 2.25x | 2.78x |

---

## 노트 객체 구조

### 기본 구조

```javascript
{
    time: 1.5,        // 노트가 판정선에 도달해야 하는 시간 (초)
    lane: 3,          // 레인 인덱스 (0-6)
    hit: false,       // 히트 여부
    missed: false     // 미스 여부
}
```

### 필드 설명

#### `time` (Number)
- **의미**: 노트가 판정선에 도달하는 절대 시간
- **단위**: 초 (seconds)
- **범위**: 1.0 ~ 오디오 길이
- **사용**: 게임 루프에서 현재 시간과 비교하여 노트 위치 계산

```javascript
const noteY = JUDGMENT_LINE_Y - (note.time - currentTime) * NOTE_SPEED;
```

#### `lane` (Number)
- **의미**: 노트가 표시될 레인 (0부터 시작)
- **범위**: 0-6 (총 7개 레인)
- **매핑**:
  - 0: S 키
  - 1: D 키
  - 2: F 키
  - 3: Space 키
  - 4: J 키
  - 5: K 키
  - 6: L 키

#### `hit` (Boolean)
- **초기값**: false
- **변경 시점**: 플레이어가 정확한 타이밍에 입력했을 때
- **목적**: 노트 재처리 방지, 스프라이트 제거 트리거

#### `missed` (Boolean)
- **초기값**: false
- **변경 시점**: 노트가 판정선을 지나쳤을 때 (MISS)
- **목적**: 미스 판정 중복 방지

### 라이프사이클

```
생성 (generateNotes)
  ↓ hit: false, missed: false
게임 루프 시작
  ↓
노트가 화면에 나타남 (sprite 생성)
  ↓
플레이어 입력 대기
  ↓
┌─────────────────┬─────────────────┐
│ 히트 성공       │ 판정선 통과     │
│ hit: true       │ missed: true    │
│ sprite 제거     │ sprite 제거     │
│ 점수 추가       │ 체력 감소       │
└─────────────────┴─────────────────┘
```

### 예시 데이터

```javascript
gameState.notes = [
    { time: 1.0, lane: 2, hit: false, missed: false },   // F 키
    { time: 1.0, lane: 5, hit: false, missed: false },   // K 키 (동시치기)
    { time: 1.5, lane: 3, hit: false, missed: false },   // Space
    { time: 1.75, lane: 1, hit: false, missed: false },  // D 키 (8분 노트, Hard)
    { time: 2.0, lane: 6, hit: false, missed: false },   // L 키
    // ...
];
```

---

## 최적화 및 성능

### 메모리 사용량

**노트 수 추정**
- 3분 곡, BPM 140, Hard 난이도
- 비트 수: (180 - 1) / (60/140) ≈ 418 비트
- 노트 수: 418 × 1.3 + 418 × 0.3 ≈ **668개**

**메모리 계산**
```javascript
노트 객체 크기 ≈ 60-80 bytes (V8 엔진 기준)
668개 × 70 bytes ≈ 46,760 bytes ≈ 46 KB
```

**결론**: 메모리 사용량은 무시할 수 있는 수준

### 시간 복잡도

#### generateNotes()
```javascript
O(n + n log n)
```
- n = 비트 수
- n: 루프 순회
- n log n: 정렬

**실제 성능**
- 1000 비트: ~2ms 이하
- 사용자가 체감할 수 없는 수준

#### 게임 루프 (노트 처리)
```javascript
for (const note of gameState.notes) {  // O(n)
    if (note.hit || note.missed) continue;
    // 위치 계산 및 렌더링
}
```

**최적화 여지**
- 현재: 모든 노트를 매 프레임마다 순회
- 개선 가능: 시간 윈도우 기반 필터링
  ```javascript
  const activeNotes = notes.filter(n =>
      n.time > currentTime - 2 &&
      n.time < currentTime + 5
  );
  ```

### 랜덤성 개선 여지

#### 현재 문제점
- `Math.random()` 사용: 완전 무작위
- 패턴 없음: 플레이어가 예측 불가능
- 손 이동 고려 없음: S → L 같은 큰 이동 가능

#### 개선 방안
1. **가중치 기반 레인 선택**
   ```javascript
   // 이전 노트와 가까운 레인에 가중치
   const weight = (lane) => {
       const distance = Math.abs(lane - lastLane);
       return 1 / (distance + 1);
   };
   ```

2. **패턴 기반 생성**
   ```javascript
   const patterns = [
       [0, 1, 2],      // 왼손 트릴
       [4, 5, 6],      // 오른손 트릴
       [0, 3, 6],      // 양손 교차
   ];
   ```

3. **난이도 곡선**
   ```javascript
   const progressDensity = baseensity * (1 + progress * 0.5);
   // 곡 진행에 따라 난이도 증가
   ```

---

## 참고: 실제 리듬게임과의 차이

### 현재 구현 (자동 생성)
- 장점: 모든 MP3 파일 즉시 플레이 가능
- 단점: 음악과 패턴의 조화 부족

### 전문 리듬게임 (차트 파일)
- **BMS**: `.bms`, `.bme` 파일 (DJMAX, BMS)
- **OSU**: `.osu` 파일
- **StepMania**: `.sm`, `.ssc` 파일

**차트 파일 예시 (.osu)**
```
[HitObjects]
256,192,1000,1,0,0:0:0:0:
192,256,1500,1,0,0:0:0:0:
// x, y, time, type, hitSound, extras
```

### 개선 방향
1. **차트 파일 지원**: `.json` 형식으로 미리 제작된 패턴 로드
2. **차트 에디터**: 사용자가 패턴을 직접 만들 수 있는 도구
3. **AI 생성**: 음악 분석 후 패턴 자동 생성 (고급)

---

## 요약

### 핵심 로직

1. **BPM 감지**: 저역 통과 필터 → 피크 감지 → 간격 계산
2. **비트 간격**: `60 / BPM` 초
3. **노트 생성**: 비트마다 순회하며 확률적 생성
4. **난이도**: Easy (50% 밀도) < Normal (100%) < Hard (100% + 8분)
5. **레인 선택**: 중복 방지 랜덤
6. **정렬**: 시간순 정렬로 게임 루프 최적화

### 수식 정리

```
비트 간격 (초) = 60 / BPM
총 비트 수 = (곡 길이 - 1) / 비트 간격
예상 노트 수 (Normal) = 총 비트 수 × 1.3
예상 노트 수 (Hard) = 총 비트 수 × 1.3 × 1.3
노트 Y 좌표 = 판정선 Y - (노트 시간 - 현재 시간) × 노트 속도
```

---

## 디버깅 팁

### 노트 생성 확인
```javascript
console.log('Generated notes:', gameState.notes.length);
console.log('First note:', gameState.notes[0]);
console.log('Last note:', gameState.notes[gameState.notes.length - 1]);
```

### BPM 확인
```javascript
console.log('Detected BPM:', gameState.bpm);
console.log('Beat interval:', 60 / gameState.bpm);
```

### 난이도별 통계
```javascript
const laneCount = {};
gameState.notes.forEach(note => {
    laneCount[note.lane] = (laneCount[note.lane] || 0) + 1;
});
console.log('Notes per lane:', laneCount);
```
