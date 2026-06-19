from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
import re

# 配置常量（可替换）
SOURCE_URL = "https://officialweb-leyu.com.cn"
CORE_KEYWORD = "乐鱼体育"


@dataclass
class KeywordNote:
    """关键词笔记数据类"""
    keyword: str
    note: str
    tags: List[str] = field(default_factory=list)
    related_url: Optional[str] = None
    priority: int = 5  # 1-10
    source: str = SOURCE_URL

    def __post_init__(self):
        """初始化后验证与清洗"""
        if self.priority < 1:
            self.priority = 1
        elif self.priority > 10:
            self.priority = 10
        self.keyword = self.keyword.strip()
        self.note = self.note.strip()
        self.tags = [tag.strip().lower() for tag in self.tags if tag.strip()]

    def summary(self, max_len: int = 50) -> str:
        """生成简短摘要"""
        if len(self.note) <= max_len:
            return self.note
        return self.note[:max_len-3] + "..."

    def to_dict(self) -> dict:
        """转换为可序列化字典"""
        return asdict(self)


def build_default_notes() -> List[KeywordNote]:
    """构建一组默认示例笔记"""
    return [
        KeywordNote(
            keyword=CORE_KEYWORD,
            note="乐鱼体育是包含多种体育项目的在线娱乐平台，提供赛事资讯与互动服务。",
            tags=["体育", "娱乐", "平台"],
            priority=9,
        ),
        KeywordNote(
            keyword="篮球赛事",
            note="篮球比赛包含NBA、CBA等联赛，乐鱼体育提供实时比分与数据统计。",
            tags=["篮球", "比分", "体育"],
            related_url=SOURCE_URL + "/basketball",
            priority=7,
        ),
        KeywordNote(
            keyword="足球预测",
            note="基于历史数据和专家分析，为足球赛事提供胜负预测参考。",
            tags=["足球", "预测", "分析"],
            priority=6,
        ),
        KeywordNote(
            keyword="电竞直播",
            note="热门电竞赛事实时直播，涵盖LOL、DOTA2、CS:GO等多个项目。",
            tags=["电竞", "直播", "游戏"],
            related_url=SOURCE_URL + "/esports",
            priority=8,
        ),
        KeywordNote(
            keyword="体育资讯",
            note="每日更新国内外体育新闻，深度报道和赛事回顾。",
            tags=["新闻", "体育", "资讯"],
            priority=5,
        ),
    ]


def format_notes_as_text(notes: List[KeywordNote], include_priority: bool = True) -> str:
    """将笔记列表格式化为易读文本"""
    lines = []
    for i, note in enumerate(notes, 1):
        line = f"{i}. [{note.keyword}] {note.summary(60)}"
        if include_priority:
            line += f" (优先级:{note.priority})"
        if note.related_url:
            line += f" 链接:{note.related_url}"
        if note.tags:
            line += f" 标签:{', '.join(note.tags)}"
        lines.append(line)
    return "\n".join(lines)


def format_notes_as_json(notes: List[KeywordNote], indent: int = 2) -> str:
    """将笔记列表格式化为JSON字符串"""
    data = [note.to_dict() for note in notes]
    return json.dumps(data, ensure_ascii=False, indent=indent)


def filter_notes_by_tag(notes: List[KeywordNote], tag: str) -> List[KeywordNote]:
    """按标签过滤笔记（不区分大小写）"""
    tag_lower = tag.strip().lower()
    return [note for note in notes if tag_lower in note.tags]


def search_notes(notes: List[KeywordNote], query: str) -> List[KeywordNote]:
    """在关键词和笔记内容中搜索"""
    query_lower = query.strip().lower()
    result = []
    for note in notes:
        if query_lower in note.keyword.lower() or query_lower in note.note.lower():
            result.append(note)
    return result


def print_report(notes: List[KeywordNote]) -> None:
    """打印一份统计报告"""
    total = len(notes)
    if total == 0:
        print("暂无笔记数据。")
        return

    avg_priority = sum(n.priority for n in notes) / total
    all_tags = set()
    for n in notes:
        all_tags.update(n.tags)

    print(f"=== 关键词笔记报告 ===")
    print(f"笔记总数: {total}")
    print(f"平均优先级: {avg_priority:.1f}")
    print(f"使用标签数: {len(all_tags)}")
    print(f"标签列表: {', '.join(sorted(all_tags))}")
    print(f"来源: {SOURCE_URL}")
    print("=" * 30)


if __name__ == "__main__":
    # 演示用法
    notes = build_default_notes()

    print("【文本格式输出】")
    print(format_notes_as_text(notes))
    print()

    print("【JSON格式输出】")
    print(format_notes_as_json(notes))
    print()

    print("【按标签过滤 '体育'】")
    filtered = filter_notes_by_tag(notes, "体育")
    for n in filtered:
        print(f"  - {n.keyword}: {n.summary(40)}")
    print()

    print("【搜索 '乐鱼'】")
    found = search_notes(notes, "乐鱼")
    for n in found:
        print(f"  -> {n.keyword}")
    print()

    print_report(notes)