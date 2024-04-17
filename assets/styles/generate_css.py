import os
import subprocess

styles = [
  "base16",
  "base16.dark",
  "base16.light",
  "base16.monokai",
  "base16.monokai.dark",
  "base16.monokai.light",
  "base16.solarized",
  "base16.solarized.dark",
  "base16.solarized.light",
  "bw",
  "colorful",
  "github",
  "github.dark",
  "github.light",
  "gruvbox",
  "gruvbox.dark",
  "gruvbox.light",
  "igorpro",
  "magritte",
  "molokai",
  "monokai",
  "monokai.sublime",
  "pastie",
  "thankful_eyes",
  "tulip",
]

def generate_css(style_name):
  css_file = "assets/css/" + style_name + ".css"

  # 创建 CSS 文件
  os.makedirs(os.path.dirname(css_file), exist_ok=True)
  with open(css_file, "w"):
    pass

  # 生成 CSS 内容
  command = ["rougify", "style", style_name, ">", css_file]
  subprocess.run(command)

for style_name in styles:
  generate_css(style_name)
