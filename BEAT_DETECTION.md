# 고급 비트 감지 알고리즘 문서

## 개요

에디터의 "스마트 생성" 기능은 실제 음악의 비트를 분석하여 노트를 자동으로 생성합니다. 단순한 BPM 기반 생성이 아닌, 음악의 실제 드럼 패턴과 리듬을 감지합니다.

## 알고리즘 구조

### 1. 다중 주파수 대역 분석 (Multi-Band Analysis)

음악을 3개의 주파수 대역으로 분리하여 각 드럼 악기를 개별적으로 감지합니다.

```javascript
const bands = [
    { name: 'kick',  low: 20,   high: 150,   threshold: 0.8 },  // Kick drum
    { name: 'snare', low: 150,  high: 4000,  threshold: 0.7 },  // Snare/clap
    { name: 'hihat', low: 4000, high: 20000, threshold: 0.6 }   // Hi-hat/cymbal
];
```

#### 주파수 대역별 설명

| 대역 | 주파수 범위 | 타겟 악기 | 임계값 |
|------|------------|----------|--------|
| Kick | 20-150 Hz | 킥드럼, 베이스드럼 | 0.8 |
| Snare | 150-4000 Hz | 스네어, 클랩, 탐 | 0.7 |
| Hi-hat | 4000-20000 Hz | 하이햇, 심벌즈 | 0.6 |

### 2. Bandpass 필터링

각 주파수 대역에 대해 Web Audio API의 BiquadFilter를 사용합니다.

```javascript
const bandpass = offlineContext.createBiquadFilter();
bandpass.type = 'bandpass';
bandpass.frequency.value = (band.low + band.high) / 2;
bandpass.Q.value = 1.0;
```

**파라미터:**
- **Center Frequency**: 대역의 중심 주파수
- **Q Factor**: 1.0 (적당한 대역폭)

### 3. 에너지 계산 (RMS)

50ms 윈도우 단위로 오디오의 에너지를 계산합니다.

```javascript
const windowSize = Math.floor(sampleRate * 0.05); // 50ms
const hopSize = Math.floor(windowSize / 2);       // 50% overlap

for (let i = 0; i < filteredData.length - windowSize; i += hopSize) {
    let sum = 0;
    for (let j = 0; j < windowSize; j++) {
        sum += filteredData[i + j] ** 2;
    }
    const rms = Math.sqrt(sum / windowSize);
    energies.push({ time: i / sampleRate, energy: rms });
}
```

**원리:**
- **윈도우 크기**: 50ms (약 20 frames/sec)
- **Hop Size**: 25ms (50% 오버랩으로 더 정밀한 감지)
- **RMS**: Root Mean Square (에너지의 제곱근)

### 4. Spectral Flux (스펙트럼 변화율)

에너지의 변화량을 계산하여 음의 시작점(onset)을 감지합니다.

```javascript
for (let i = 1; i < energies.length; i++) {
    const flux = Math.max(0, energies[i].energy - energies[i - 1].energy);
    fluxes.push({ time: energies[i].time, flux: flux, band: band.name });
}
```

**Spectral Flux란?**
- 현재 프레임과 이전 프레임의 에너지 차이
- 양수 값만 사용 (에너지 증가만 감지)
- 급격한 에너지 증가 = 새로운 음의 시작

### 5. 적응형 임계값 (Adaptive Thresholding)

로컬 평균을 기반으로 동적으로 임계값을 조정합니다.

```javascript
const localAvgWindow = 10;
for (let i = localAvgWindow; i < fluxes.length - localAvgWindow; i++) {
    let localSum = 0;
    for (let j = -localAvgWindow; j <= localAvgWindow; j++) {
        localSum += fluxes[i + j].flux;
    }
    const localAvg = localSum / (2 * localAvgWindow + 1);

    // Peak detection
    if (fluxes[i].flux > localAvg * band.threshold &&
        fluxes[i].flux > fluxes[i - 1].flux &&
        fluxes[i].flux > fluxes[i + 1].flux) {
        // Beat detected!
    }
}
```

**적응형 임계값의 장점:**
- 조용한 구간: 낮은 임계값 → 약한 비트도 감지
- 시끄러운 구간: 높은 임계값 → 강한 비트만 감지
- 음악의 다이나믹 레인지에 자동 적응

### 6. Peak Picking (피크 선택)

3가지 조건을 모두 만족해야 비트로 인정:

```
1. 로컬 평균의 threshold 배 이상
2. 이전 프레임보다 큼 (상승 중)
3. 다음 프레임보다 큼 (하강 시작)
```

### 7. 중복 제거

```javascript
const lastBeat = allBeats[allBeats.length - 1];
if (!lastBeat || fluxes[i].time - lastBeat.time > 0.1) {
    allBeats.push({ time: fluxes[i].time, intensity: fluxes[i].flux, band: band.name });
}
```

- 최소 100ms 간격 유지
- 너무 가까운 비트는 하나로 합침

## 노트 생성 로직

### 1. 강도 기반 노트 수 결정

```javascript
const intensityRatio = beat.intensity / maxIntensity;

if (intensityRatio > 0.8) {
    numNotes = Math.random() < 0.5 ? 2 : 3; // 강한 비트 → 2-3개
} else if (intensityRatio > 0.5) {
    numNotes = Math.random() < 0.3 ? 2 : 1; // 중간 비트 → 1-2개
} else {
    numNotes = 1;                            // 약한 비트 → 1개
}
```

### 2. 주파수 대역별 레인 매핑

```javascript
const lanePref = {
    'kick':  [0, 1, 2],      // 킥 → 왼쪽/중앙 레인
    'snare': [2, 3, 4],      // 스네어 → 중앙/오른쪽 레인
    'hihat': [3, 4]          // 하이햇 → 오른쪽 레인
};
```

**디자인 원칙:**
- 저음(킥) → 왼손 담당
- 고음(하이햇) → 오른손 담당
- 스네어 → 양손 모두 사용 가능

### 3. 스마트 레인 선택

```javascript
for (let i = 0; i < numNotes; i++) {
    // 처음 5번은 선호 레인에서 선택
    if (attempts < 5) {
        lane = preferredLanes[Math.floor(Math.random() * preferredLanes.length)];
    } else {
        // 실패 시 모든 레인에서 선택
        lane = Math.floor(Math.random() * LANES.length);
    }
}
```

## 성능 최적화

### 시간 복잡도

- **필터링**: O(n) × 3 bands = O(3n)
- **RMS 계산**: O(n / hopSize) = O(n)
- **Flux 계산**: O(n / hopSize) = O(n)
- **Peak Detection**: O(n / hopSize) = O(n)
- **전체**: **O(n)** (선형 시간)

### 공간 복잡도

- AudioBuffer: n samples
- Energies: n / hopSize
- Fluxes: n / hopSize
- Beats: ~duration × avg_bpm / 60
- **전체**: **O(n)**

### 실제 성능

**3분 곡 (180초, 44.1kHz 샘플레이트):**
- 샘플 수: 180 × 44100 = 7,938,000
- 예상 처리 시간: **1-3초** (브라우저/CPU 성능에 따라)
- 메모리 사용: **~30-50MB**

## 비교: 기존 vs 스마트 생성

### 기존 (BPM 기반)

```javascript
for (let time = 1; time < duration; time += beatInterval) {
    // 고정 간격으로 노트 생성
    const lane = Math.floor(Math.random() * LANES.length);
    notes.push({ time, lane });
}
```

**문제점:**
- ❌ 실제 음악과 무관
- ❌ 모든 비트가 동일한 강도
- ❌ 드럼 악기 구분 없음
- ❌ 단조로운 패턴

### 스마트 생성 (비트 감지)

```javascript
for (const beat of detectedBeats) {
    // 실제 비트 위치
    // 강도에 따른 노트 수
    // 악기별 레인 매핑
    notes.push({ time: beat.time, lane: smartLane });
}
```

**장점:**
- ✅ 실제 음악의 리듬 반영
- ✅ 강약 표현 (다이나믹스)
- ✅ 드럼 패턴 인식
- ✅ 자연스러운 플레이 경험

## 한계와 개선 방안

### 현재 한계

1. **전자음악 최적화**
   - 어쿠스틱 드럼이 아닌 신스 비트 감지 어려움
   - 해결: 추가 주파수 대역, 다른 임계값 적용

2. **템포 변화**
   - BPM이 중간에 바뀌는 곡 대응 불가
   - 해결: 슬라이딩 윈도우로 로컬 BPM 추정

3. **복잡한 폴리리듬**
   - 다양한 리듬이 겹치면 오감지
   - 해결: 다중 에이전트 방식 (각 리듬 독립 추적)

### 개선 방안

#### 1. Machine Learning 통합

```javascript
// TensorFlow.js 사용
const model = await tf.loadLayersModel('beat-detection-model.json');
const predictions = model.predict(audioFeatures);
```

#### 2. 사용자 피드백 반영

```javascript
// 사용자가 수동으로 추가한 노트를 학습
function learnFromUser(userNotes, detectedBeats) {
    // 사용자 선호도 분석
    // 임계값 자동 조정
}
```

#### 3. 장르별 프리셋

```javascript
const genrePresets = {
    'edm': { kick: 0.9, snare: 0.8, hihat: 0.7 },
    'rock': { kick: 0.7, snare: 0.9, hihat: 0.6 },
    'hiphop': { kick: 0.85, snare: 0.95, hihat: 0.5 }
};
```

## 사용 팁

### 1. BPM 입력 권장

자동 감지가 어려운 경우 수동으로 BPM을 입력하세요:
- 느린 발라드: 60-80 BPM
- 보통 템포: 100-120 BPM
- 빠른 댄스: 130-150 BPM
- 매우 빠른 곡: 160-200 BPM

### 2. 분석 전 확인

"🔍 비트 분석" 버튼으로 먼저 분석 품질을 확인:
- 전체 비트 수가 적절한지
- 주파수 대역별 분포가 자연스러운지

### 3. 수동 조정

자동 생성 후 수동으로 노트 추가/삭제 가능:
- 재생하며 키 입력으로 노트 추가
- Delete 키로 마지막 노트 삭제

## 참고 자료

### 논문
- **Onset Detection**: Dixon, S. (2006). "Onset detection revisited"
- **Beat Tracking**: Ellis, D. P. (2007). "Beat tracking by dynamic programming"
- **Spectral Flux**: Bello, J. P., et al. (2005). "A tutorial on onset detection in music signals"

### 라이브러리
- [web-audio-beat-detector](https://github.com/chrisguttandin/web-audio-beat-detector)
- [Meyda](https://meyda.js.org/) - Audio feature extraction
- [Essentia.js](https://mtg.github.io/essentia.js/) - Music analysis

### Web Audio API
- [MDN Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [BiquadFilterNode](https://developer.mozilla.org/en-US/docs/Web/API/BiquadFilterNode)
- [OfflineAudioContext](https://developer.mozilla.org/en-US/docs/Web/API/OfflineAudioContext)

---

**작성일**: 2025-10-28
**버전**: 1.0
**저자**: AI-Diver BookJam Team
