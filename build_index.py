#!/usr/bin/env python3
# Build a self-contained index.html that embeds bms-deep.md and renders it
# with an enhanced markdown renderer (supports #/##/###, >, |tables, - lists,
# `code`, **bold**, and ``` fenced code blocks).
import io, os

MD = open(os.path.join(os.path.dirname(__file__), "bms-deep.md"), encoding="utf-8").read()
assert "</script" not in MD.lower(), "markdown contains </script -> would break HTML embedding"

TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BMS 核心算法与 Simulink 建模深度解析</title>
<style>
  :root{--bg:#0f1115;--fg:#e6e6e6;--muted:#9aa4b2;--accent:#4ea1ff;--code:#1b2030;--border:#2a2f3a;--quote:#1a2230;}
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.75;}
  .wrap{max-width:980px;margin:0 auto;padding:36px 20px 90px;}
  h1{font-size:30px;border-bottom:2px solid var(--border);padding-bottom:14px;margin-bottom:6px;}
  h2{font-size:23px;margin-top:42px;border-left:4px solid var(--accent);padding-left:12px;color:#eaf2ff;}
  h3{font-size:18px;margin-top:28px;color:#cfe3ff;}
  p{margin:12px 0;}
  code{background:var(--code);padding:2px 6px;border-radius:4px;font-family:"SFMono-Regular",Consolas,monospace;font-size:13px;color:#ffd479;}
  pre{background:var(--code);border:1px solid var(--border);border-radius:8px;padding:14px;overflow:auto;}
  pre code{background:none;padding:0;color:#d6e2f0;font-size:13px;line-height:1.55;}
  table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px;}
  th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top;}
  th{background:#161b26;color:#cfe3ff;}
  tr:nth-child(even) td{background:#12161f;}
  blockquote{background:var(--quote);border-left:4px solid var(--accent);margin:14px 0;padding:10px 16px;color:var(--muted);border-radius:0 8px 8px 0;}
  ul{margin:10px 0;padding-left:24px;}
  li{margin:6px 0;}
  .meta{color:var(--muted);font-size:13px;margin:4px 0 18px;}
  a{color:var(--accent);}
</style>
</head>
<body>
<div class="wrap">
  <div class="meta">独立仓库 bms-algorithms-notes · 离线可读 · 与 GitHub 上 bms-deep.md 同源</div>
  <div id="out"></div>
</div>
<script type="text/markdown" id="doc">
{{CONTENT}}
</script>
<script>
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function renderInline(s){
  s=escapeHtml(s);
  s=s.replace(/`([^`]+)`/g,function(m,c){return '<code>'+c+'</code>';});
  s=s.replace(/\*\*([^*]+)\*\*/g,function(m,c){return '<strong>'+c+'</strong>';});
  return s;
}
function parseTable(rows){
  function cells(r){return r.replace(/^\||\|$/g,'').split('|').map(function(x){return x.trim();});}
  var hc=cells(rows[0]);
  var html='<table><thead><tr>'+hc.map(function(c){return '<th>'+renderInline(c)+'</th>';}).join('')+'</tr></thead><tbody>';
  rows.slice(2).forEach(function(r){ if(r.trim()==='')return; var c=cells(r); html+='<tr>'+c.map(function(x){return '<td>'+renderInline(x)+'</td>';}).join('')+'</tr>'; });
  html+='</tbody></table>';
  return html;
}
function mdToHtml(md){
  var lines=md.split('\n'); var out=[]; var i=0;
  var inCode=false, codeBuf=[], para=[];
  function flushPara(){ if(para.length){ out.push('<p>'+renderInline(para.join(' '))+'</p>'); para=[]; } }
  while(i<lines.length){
    var line=lines[i];
    if(line.indexOf('```')===0){
      flushPara();
      if(!inCode){ inCode=true; codeBuf=[]; }
      else { out.push('<pre><code>'+escapeHtml(codeBuf.join('\n'))+'</code></pre>'); inCode=false; }
      i++; continue;
    }
    if(inCode){ codeBuf.push(line); i++; continue; }
    if(line.indexOf('### ')===0){ flushPara(); out.push('<h3>'+renderInline(line.slice(4))+'</h3>'); i++; continue; }
    if(line.indexOf('## ')===0){ flushPara(); out.push('<h2>'+renderInline(line.slice(3))+'</h2>'); i++; continue; }
    if(line.indexOf('# ')===0){ flushPara(); out.push('<h1>'+renderInline(line.slice(2))+'</h1>'); i++; continue; }
    if(line.indexOf('|')===0){
      flushPara();
      var tbl=[];
      while(i<lines.length && lines[i].indexOf('|')===0){ tbl.push(lines[i]); i++; }
      out.push(parseTable(tbl));
      continue;
    }
    if(line.indexOf('>')===0){
      flushPara();
      var bq=[];
      while(i<lines.length && lines[i].indexOf('>')===0){ bq.push(lines[i].replace(/^>\s?/,'')); i++; }
      out.push('<blockquote>'+renderInline(bq.join('<br>'))+'</blockquote>');
      continue;
    }
    if(line.indexOf('- ')===0){
      flushPara();
      var lis=[];
      while(i<lines.length && lines[i].indexOf('- ')===0){ lis.push('<li>'+renderInline(lines[i].slice(2))+'</li>'); i++; }
      out.push('<ul>'+lis.join('')+'</ul>');
      continue;
    }
    if(line.trim()===''){ flushPara(); i++; continue; }
    para.push(line); i++;
  }
  flushPara();
  if(inCode){ out.push('<pre><code>'+escapeHtml(codeBuf.join('\n'))+'</code></pre>'); }
  return out.join('\n');
}
var md = document.getElementById('doc').textContent;
document.getElementById('out').innerHTML = mdToHtml(md);
</script>
</body>
</html>
"""

html = TEMPLATE.replace("{{CONTENT}}", MD)
with open(os.path.join(os.path.dirname(__file__), "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("index.html written, bytes=", len(html.encode("utf-8")))
