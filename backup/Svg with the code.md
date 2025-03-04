[先上svg转png的Website](https://www.svgviewer.dev/)

<img width="1314" alt="Image" src="https://github.com/user-attachments/assets/605fb0ea-41e1-4816-8f5a-14fefbd2c4f1" />

这个svg代码给出的思维导图样式还不错，于是我可以经常沿用这个代码格式，发给AI去做相关的思维导图，把线形的文本转位立体的结构图。

```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800">
  <!-- Background -->
  <rect width="1000" height="800" fill="#f9f9f9" rx="10" ry="10"/>
  
  <!-- Title -->
  <text x="500" y="40" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" font-weight="bold" fill="#333">法语代词 en 的用法</text>
  
  <!-- Center node -->
  <ellipse cx="500" cy="120" rx="120" ry="50" fill="#4e73df" stroke="#3a56c5" stroke-width="2"/>
  <text x="500" y="125" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="white" font-weight="bold">代词 en</text>
  
  <!-- Understanding Branch -->
  <path d="M620 120 L750 120" stroke="#333" stroke-width="2" fill="none"/>
  <ellipse cx="820" cy="120" rx="80" ry="40" fill="#f39c12" stroke="#e67e22" stroke-width="2"/>
  <text x="820" y="125" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" fill="#333" font-weight="bold">理解方法</text>
  
  <!-- Understanding Details -->
  <rect x="740" y="170" width="240" height="100" rx="10" ry="10" fill="#f8c471" stroke="#e67e22" stroke-width="2"/>
  <text x="860" y="195" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">贴士1：理解为 of it / of them</text>
  <text x="860" y="215" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">en 代替 de + 某物</text>
  <text x="860" y="235" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">根据上下文判断指代</text>
  <text x="860" y="255" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">初级/中级适用</text>
  
  <rect x="740" y="280" width="240" height="80" rx="10" ry="10" fill="#f8c471" stroke="#e67e22" stroke-width="2"/>
  <text x="860" y="305" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">贴士2：注意无特殊含义的 en</text>
  <text x="860" y="330" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Je m’en vais</text>
  <text x="860" y="350" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(我离开了)</text>
  
  <!-- Basic Usage Branch -->
  <path d="M380 120 L240 120" stroke="#333" stroke-width="2" fill="none"/>
  <ellipse cx="180" cy="120" rx="80" ry="40" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>
  <text x="180" y="125" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" fill="#333" font-weight="bold">初级用法</text>
  
  <!-- Basic Usage Details -->
  <rect x="60" y="170" width="240" height="110" rx="10" ry="10" fill="#abebc6" stroke="#27ae60" stroke-width="2"/>
  <text x="180" y="195" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替数量 + 名词</text>
  <text x="180" y="215" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Il y a 3 stylos ?</text>
  <text x="180" y="235" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(那儿有三支笔吗？)</text>
  <text x="180" y="255" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Oui, il y en a trois.</text>
  <text x="180" y="275" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(是，那儿有三支)</text>
  
  <rect x="60" y="290" width="240" height="110" rx="10" ry="10" fill="#abebc6" stroke="#27ae60" stroke-width="2"/>
  <text x="180" y="315" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替不定冠词 + 名词</text>
  <text x="180" y="335" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Tu as un stylo ?</text>
  <text x="180" y="355" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(你有一支笔吗？)</text>
  <text x="180" y="375" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Oui, j’en ai un.</text>
  <text x="180" y="395" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(有，我有一支)</text>
  
  <rect x="60" y="410" width="240" height="110" rx="10" ry="10" fill="#abebc6" stroke="#27ae60" stroke-width="2"/>
  <text x="180" y="435" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替数量短语 + 名词</text>
  <text x="180" y="455" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Il y a beaucoup de stylos ?</text>
  <text x="180" y="475" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(那儿有很多笔吗？)</text>
  <text x="180" y="495" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Oui, il y en a beaucoup.</text>
  <text x="180" y="515" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(是，那儿有很多)</text>
  
  <rect x="60" y="530" width="240" height="110" rx="10" ry="10" fill="#abebc6" stroke="#27ae60" stroke-width="2"/>
  <text x="180" y="555" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替部分冠词 + 名词</text>
  <text x="180" y="575" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Tu veux de la bière ?</text>
  <text x="180" y="595" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(你想要啤酒吗？)</text>
  <text x="180" y="615" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Oui, j’en veux bien.</text>
  <text x="180" y="635" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(想，我想要)</text>
  
  <!-- Intermediate Usage Branch -->
  <path d="M500 170 L500 260" stroke="#333" stroke-width="2" fill="none"/>
  <ellipse cx="500" cy="300" rx="100" ry="40" fill="#3498db" stroke="#2980b9" stroke-width="2"/>
  <text x="500" y="305" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" fill="#333" font-weight="bold">中级用法</text>
  
  <!-- Intermediate Usage Details -->
  <rect x="380" y="350" width="240" height="110" rx="10" ry="10" fill="#85c1e9" stroke="#2980b9" stroke-width="2"/>
  <text x="500" y="375" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替与数量无关的 de + 名词</text>
  <text x="500" y="395" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">La qualité de ces images est très bien.</text>
  <text x="500" y="415" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(这些图像的质量很好)</text>
  <text x="500" y="435" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">La qualité en est parfaite.</text>
  <text x="500" y="455" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(它们的质量完美)</text>
  
  <!-- Advanced Usage Branch -->
  <path d="M500 340 L620 400" stroke="#333" stroke-width="2" fill="none"/>
  <ellipse cx="670" cy="440" rx="100" ry="40" fill="#9b59b6" stroke="#8e44ad" stroke-width="2"/>
  <text x="670" y="445" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" fill="#333" font-weight="bold">高级用法</text>
  
  <!-- Advanced Usage Details -->
  <rect x="550" y="490" width="240" height="130" rx="10" ry="10" fill="#d7bde2" stroke="#8e44ad" stroke-width="2"/>
  <text x="670" y="515" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">代替动词 + de + 名词/从句</text>
  <text x="670" y="535" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Vous faites du sport ?</text>
  <text x="670" y="555" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(你做运动吗？)</text>
  <text x="670" y="575" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">Oui, j’en fais souvent.</text>
  <text x="670" y="595" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(是，我经常做)</text>
  <text x="670" y="615" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333" font-style="italic">J’en suis certain.</text>
  <text x="670" y="635" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">(我肯定)</text>
  
  <!-- English equivalent -->
  <path d="M500 60 L500 30" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" fill="none"/>
  <text x="500" y="80" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">常代替 de + 某物 (of it / of them)</text>
</svg>
```
有了这样的模板之后，你把模板先发给AI，之后再发你需要处理的内容即可。
