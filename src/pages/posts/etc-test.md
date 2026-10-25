---
title: "기타 카테고리 기능 테스트"
description: "코드 블록, 링크와 이미지 렌더링을 확인합니다."
pubDate: 2026-10-22
category: "기타"
tags: ["테스트", "기타", "코드"]
---

# 기타 기능 테스트

이 글에서는 일반적인 본문 외에 코드 블록과 구분선 등 여러 요소를 확인합니다.

## 코드 블록

```javascript
function greeting(name) {
  return `안녕하세요, ${name}님!`;
}

console.log(greeting("방문자"));
```

## 인라인 코드

설정 파일에서 `site` 또는 `base` 항목을 확인하는 상황을 가정한 예시입니다.

## 구분선

위아래 콘텐츠가 구분되는지 확인합니다.

---

## 이미지와 링크

![기타 테스트 이미지](https://img.youtube.com/vi/VGkoaHyVUdg/maxresdefault.jpg)

[Markdown 가이드 참고](https://www.markdownguide.org/)

## 강조 표현

**굵은 글씨**, *기울임 글씨*, ~~취소선~~, <u>밑줄</u>이 각각 구별되어 보이는지 확인합니다.

<span style="color: #2563eb;">파란색 글자 테스트</span>

| 기능 | 테스트 여부 |
|---|---|
| 코드 블록 | 확인용 |
| 이미지 | 확인용 |
| 표 | 확인용 |
